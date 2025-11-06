from .html_dict import HTMLDict

import os, re, tempfile, requests
import rasterio
from rasterio.mask import mask as rio_mask
from rasterio.plot import plotting_extent
import matplotlib.pyplot as plt
import numpy as np


class WorldPopAsset(HTMLDict):
    ASSET_PROPERTIES = [
        "sex",
        "sex_label",
        "age_group",
        "age_label",
    ]
    ASSET_PROPERTIES_PREFIX = 'agesex'

    def __init__(self, asset_dict):
        if not isinstance(asset_dict, dict):
            raise TypeError(f"Expected dict for asset_dict, got {type(asset_dict)}")
        metadata = {
            "href": asset_dict.get("href"),
            "type": asset_dict.get("type"),
            "title": asset_dict.get("title"),
            "file:size": asset_dict.get("file:size"),
            "description": asset_dict.get("description"),
        }
        for key in WorldPopAsset.ASSET_PROPERTIES:
            key_wprefix = f"{WorldPopAsset.ASSET_PROPERTIES_PREFIX}:{key}"
            metadata[key_wprefix] = asset_dict.get(key_wprefix)
        super().__init__(metadata)

    def download(self, out_dir):
        os.makedirs(out_dir, exist_ok=True)
        local_path = os.path.join(out_dir, os.path.basename(self.href))
        if not os.path.exists(local_path):
            r = requests.get(self.href, stream=True, timeout=60)
            r.raise_for_status()
            with open(local_path, "wb") as f:
                for chunk in r.iter_content(8192):
                    f.write(chunk)
        self.localref = local_path
        return local_path

    def _plot_from_path(self, path, polygon=None):
        with rasterio.open(path) as src:
            if polygon:
                out_image, out_transform = rio_mask(src, [polygon], crop=True)
                band = out_image[0].astype(float)
            else:
                band = src.read(1).astype(float)
                out_transform = src.transform

            nodata = src.nodatavals[0] if src.nodatavals else None
            if nodata is not None:
                band[band == nodata] = np.nan

            extent = plotting_extent(band, out_transform)
            plt.figure(figsize=(8, 6))
            plt.imshow(band, cmap="viridis", extent=extent)
            plt.colorbar(label="Population")
            plt.title(f"{self.title}")
            plt.xlabel("Longitude")
            plt.ylabel("Latitude")
            plt.gca().set_aspect("equal", adjustable="box")
            plt.show()
        
    def plot(self, polygon=None, out_dir=None):
        paths_tried = []
        for path in [self.href, getattr(self, "localref", None)]:
            if path:
                try:
                    self._plot_from_path(path, polygon)
                    return
                except Exception as e:
                    paths_tried.append((path, str(e)))

        if out_dir:
            local_path = self.download(out_dir)
        else:    
            raise RuntimeError(
                "Unable to plot raster directly from remote server.\n"
                f"Tried paths: {paths_tried}\n"
                "Provide an `out_dir` argument to download the raster and plot the local file."
            )
        
        try:
            self._plot_from_path(local_path, polygon)
        except Exception as e:
            raise RuntimeError(
                f"Failed to plot raster. Tried paths: {paths_tried + [(local_path, str(e))]}"
            )
