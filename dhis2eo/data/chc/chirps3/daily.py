import logging
from datetime import date, datetime, timedelta
from typing import Iterable, List, Tuple, Union

import numpy as np
import rasterio
from rasterio.windows import from_bounds
import xarray as xr

from ...utils import netcdf_cache, force_logging

# -----------------------------------------------------------------------------
# Logging setup
# -----------------------------------------------------------------------------
# Use module-level logger and force logging on so progress messages
# are visible when running in notebooks or scripts.
logger = logging.getLogger(__name__)
force_logging(logger)

# -----------------------------------------------------------------------------
# Type aliases and defaults
# -----------------------------------------------------------------------------

# Bounding box type:
# (min_lon, min_lat, max_lon, max_lat) in EPSG:4326 (lon/lat)
BBox = Tuple[float, float, float, float]

# CHIRPS v3 "stage":
# - "final": finalized, stable product (recommended for analysis)
# - "prelim": near-real-time preliminary product
DEFAULT_STAGE = "final"

# CHIRPS v3 "flavor":
# - For final: "rnl" or "sat"
# - For prelim: directory is "sat" but filename tag is "prelim"
DEFAULT_FLAVOR = "rnl"


# -----------------------------------------------------------------------------
# Helper functions: dates and iteration
# -----------------------------------------------------------------------------

def _ensure_date(d: Union[str, date, datetime]) -> date:
    """
    Normalize input into a `date` object.

    Accepts:
    - YYYY-MM-DD strings
    - datetime.datetime
    - datetime.date

    This keeps the public API flexible while ensuring internal consistency.
    """
    if isinstance(d, datetime):
        return d.date()
    if isinstance(d, date):
        return d
    return datetime.strptime(str(d), "%Y-%m-%d").date()


def _iter_days(start: date, end: date) -> Iterable[date]:
    """
    Yield all dates from `start` to `end`, inclusive.

    Used to build the time dimension one day at a time.
    """
    cur = start
    while cur <= end:
        yield cur
        cur = cur + timedelta(days=1)


# -----------------------------------------------------------------------------
# URL construction (provider-specific logic)
# -----------------------------------------------------------------------------

def url_for_day(
    d: Union[str, date, datetime],
    *,
    stage: str = DEFAULT_STAGE,
    flavor: str = DEFAULT_FLAVOR,
) -> str:
    """
    Construct the CHC URL for a single CHIRPS v3 daily GeoTIFF.

    Directory and filename conventions on CHC:

    FINAL:
      /products/CHIRPS/v3.0/daily/final/{rnl|sat}/{YYYY}/
      chirps-v3.0.{rnl|sat}.{YYYY}.{MM}.{DD}.tif

    PRELIM:
      /products/CHIRPS/v3.0/daily/prelim/sat/{YYYY}/
      chirps-v3.0.prelim.{YYYY}.{MM}.{DD}.tif
    """
    dd = _ensure_date(d)

    if stage not in {"final", "prelim"}:
        raise ValueError("stage must be 'final' or 'prelim'")

    # Final products: both rnl and sat exist
    if stage == "final":
        if flavor not in {"rnl", "sat"}:
            raise ValueError("For stage='final', flavor must be 'rnl' or 'sat'")
        return (
            "https://data.chc.ucsb.edu/products/CHIRPS/v3.0/daily/final/"
            f"{flavor}/{dd.year}/chirps-v3.0.{flavor}.{dd.year}.{dd.month:02d}.{dd.day:02d}.tif"
        )

    # Preliminary products: directory is sat/, filename uses "prelim"
    if flavor != "sat":
        raise ValueError("For stage='prelim', flavor must be 'sat'")
    return (
        "https://data.chc.ucsb.edu/products/CHIRPS/v3.0/daily/prelim/sat/"
        f"{dd.year}/chirps-v3.0.prelim.{dd.year}.{dd.month:02d}.{dd.day:02d}.tif"
    )


# -----------------------------------------------------------------------------
# Raster I/O: read only the bbox window into xarray
# -----------------------------------------------------------------------------

def _read_bbox_as_dataarray(
    url: str,
    bbox: BBox,
    var_name: str = "precip",
) -> xr.DataArray:
    """
    Read only the raster window intersecting `bbox` from a remote GeoTIFF
    and return it as an xarray.DataArray.

    Key design choice:
    - Use rasterio windowed reads to avoid loading global rasters.
    """
    minx, miny, maxx, maxy = bbox

    try:
        with rasterio.open(url) as src:
            # Convert lon/lat bounds into pixel window coordinates
            win = from_bounds(minx, miny, maxx, maxy, transform=src.transform)
            win = win.round_offsets().round_lengths()

            # Clamp window to raster extent to avoid edge errors
            full = rasterio.windows.Window(0, 0, src.width, src.height)
            try:
                win = win.intersection(full)
            except Exception as e:
                raise ValueError(
                    f"Requested bbox {bbox} does not intersect raster extent "
                    f"({src.bounds}) for {url}"
                ) from e

            # Read only band 1 for the requested window
            data = src.read(1, window=win, masked=True)
            transform = src.window_transform(win)

            # Convert to float32 and replace masked values with NaN
            arr = data.astype("float32")
            if np.ma.isMaskedArray(arr):
                arr = arr.filled(np.nan)

            # Build coordinate vectors (pixel centers) from affine transform
            height, width = arr.shape
            t = transform  # affine.Affine
            xs = t.c + t.a * (np.arange(width) + 0.5)
            ys = t.f + t.e * (np.arange(height) + 0.5)

            # Assemble metadata, avoiding NetCDF-invalid values (e.g. None)
            attrs = {
                "crs": str(src.crs) if src.crs else "unknown",
                "source_url": url,
            }
            if src.nodata is not None:
                attrs["nodata"] = float(src.nodata)

            return xr.DataArray(
                arr,
                dims=("y", "x"),
                coords={"x": xs, "y": ys},
                name=var_name,
                attrs=attrs,
            )

    except rasterio.errors.RasterioIOError as e:
        # Surface URL explicitly to make debugging 404s easier
        raise rasterio.errors.RasterioIOError(
            f"Failed to open CHIRPS GeoTIFF (likely 404).\n"
            f"URL: {url}\n"
            f"Original error: {e}"
        ) from e


# -----------------------------------------------------------------------------
# Public API: download and stack daily CHIRPS into an xarray Dataset
# -----------------------------------------------------------------------------

@netcdf_cache()
def get(
    start: Union[str, date, datetime],
    end: Union[str, date, datetime],
    bbox: BBox,
    *,
    stage: str = DEFAULT_STAGE,
    flavor: str = DEFAULT_FLAVOR,
    var_name: str = "precip",
) -> xr.Dataset:
    """
    Fetch CHIRPS v3 daily precipitation for the given date range and bbox.

    Returns an xarray.Dataset with:
    - one variable: `var_name` (default: precip)
    - dimensions: (time, y, x)
    """
    start_d = _ensure_date(start)
    end_d = _ensure_date(end)
    if end_d < start_d:
        raise ValueError("end must be on/after start")

    logger.info(f"Fetching CHIRPS v3 daily from {start_d} to {end_d} (inclusive)")
    logger.info(f"Stage/flavor: {stage}/{flavor}")
    logger.info(f"BBox: {bbox}")

    das: List[xr.DataArray] = []
    times: List[np.datetime64] = []

    # Loop over days, read each bbox window, and collect results
    for d in _iter_days(start_d, end_d):
        url = url_for_day(d, stage=stage, flavor=flavor)
        logger.info(f"Reading {d} -> {url}")
        da = _read_bbox_as_dataarray(url, bbox=bbox, var_name=var_name)
        das.append(da)
        times.append(np.datetime64(d))

    # Stack daily slices along the time dimension
    stacked = xr.concat(das, dim=xr.IndexVariable("time", times))
    ds = stacked.to_dataset(name=var_name)

    # Light, CF-ish metadata for downstream use
    ds[var_name].attrs.setdefault("long_name", "Precipitation")
    ds[var_name].attrs.setdefault("units", "mm/day")
    ds.attrs["bbox"] = bbox
    ds.attrs["dataset"] = "CHIRPS v3 (daily)"
    ds.attrs["stage"] = stage
    ds.attrs["flavor"] = flavor

    return ds
