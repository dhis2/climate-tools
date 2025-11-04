import os
import re
import tempfile
from html import escape
from functools import lru_cache

import numpy as np
import requests
import rasterio
import matplotlib.pyplot as plt
from rasterio.mask import mask as rio_mask
from rasterio.plot import plotting_extent
from pystac_client import ItemSearch
from dhis2eo.html.jinja_env import get_jinja_env


class Manager:
    """Base class for STAC helpers."""
    SUPPORTED_SOURCES = ["worldpop", "sentinel"]

    @classmethod
    def list_supported_sources(cls):
        return cls.SUPPORTED_SOURCES


class WorldPop(Manager):
    """STAC helper for WorldPop metadata."""
    BASE_URL = "https://api.stac.worldpop.org/search"
    COLLECTIONS_URL = "https://api.stac.worldpop.org/collections"
    SUPPORTED_PROPERTIES = {
        "years": [str(y) for y in range(2015, 2031)],
        "version": ["v1"],
        "projects": ["Population", "Age and Sex Structures"],
        "resolutions": ["100m", "1km"],
    }

    def list_properties(self):
        return HTMLDict(self.SUPPORTED_PROPERTIES)

    @staticmethod
    @lru_cache(maxsize=1)
    def list_countries():
        response = requests.get(WorldPop.COLLECTIONS_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        countries = {c.get("id", "").upper(): c.get("title", "") for c in data.get("collections", [])}
        return HTMLDict(countries)

    @staticmethod
    def find_country_code(name: str):
        def _norm(s: str) -> str:
            return re.sub(r"[^a-z0-9]+", "", (s or "").lower())

        q = _norm(name)
        if not q:
            return HTMLDict({"top": None, "matches": []})

        def _score(q: str, title: str, code: str) -> int:
            ntitle, ncode = _norm(title), _norm(code)
            if q == ntitle:
                return 0
            if q == ncode:
                return 1
            if q in ncode:
                return 2
            if q in ntitle:
                return 3
            return 9999

        countries = WorldPop.list_countries()
        scored = [{"score": _score(q, title, code), "code": code, "title": title}
                  for code, title in countries.items()]
        scored = [s for s in scored if s["score"] < 9999]
        scored.sort(key=lambda x: (x["score"], x["code"], x["title"]))
        return HTMLDict({"top": scored[0] if scored else None, "matches": scored})

    def search_items(self, collections=None, year=None, project=None, resolution=None,
                     bbox=None, start_date=None, end_date=None, **kwargs):
        if collections:
            valid = set(self.list_countries().keys())
            invalid = [c for c in collections if c not in valid]
            if invalid:
                raise ValueError(f"Invalid collections: {invalid}")
        if year and str(year) not in self.SUPPORTED_PROPERTIES["years"]:
            raise ValueError(f"Unsupported year: {year}")
        if project and project not in self.SUPPORTED_PROPERTIES["projects"]:
            raise ValueError(f"Unsupported project: {project}")
        if resolution and resolution not in self.SUPPORTED_PROPERTIES["resolutions"]:
            raise ValueError(f"Unsupported resolution: {resolution}")

        datetime_range = f"{start_date}/{end_date}" if start_date and end_date else None
        query = {k: {"eq": v} for k, v in {
            "year": str(year) if year else None,
            "project": project,
            "resolution": resolution
        }.items() if v}

        search = ItemSearch(
            url=self.BASE_URL, collections=collections, bbox=bbox,
            datetime=datetime_range, query=query, **kwargs
        )

        items = list(search.items_as_dicts())
        return HTMLDict({
            "ids": [i["id"] for i in items],
            "items": {i["id"]: i for i in items},
            "count": len(items),
        })

    def get_item_by_id(self, item_id: str):
        search = ItemSearch(url=self.BASE_URL, ids=[item_id])
        items = list(search.items_as_dicts())
        if not items:
            raise ValueError(f"No item found with ID '{item_id}'")
        return HTMLDict(items[0])

    def list_assets(self, item_id: str):
        search = ItemSearch(url=self.BASE_URL, ids=[item_id])
        items = list(search.items())
        if not items:
            raise ValueError(f"No item found with ID '{item_id}'")

        item = items[0]
        formatted = {"sex": {}, "age_group": {}}
        for key, asset in item.assets.items():
            props = getattr(asset, "extra_fields", {}) or {}
            sex, sex_label = props.get("agesex:sex"), props.get("agesex:sex_label")
            age, age_label = props.get("agesex:age_group"), props.get("agesex:age_label")
            if sex:
                formatted["sex"][sex] = sex_label or sex
            if age:
                formatted["age_group"][age] = age_label or age
        return HTMLDict({"properties": formatted, "assets": item.assets})

    def search_assets(self, item_id: str, sex=None, age_group=None):
        search = ItemSearch(url=self.BASE_URL, ids=[item_id])
        items = list(search.items())
        if not items:
            raise ValueError(f"No item found with ID '{item_id}'")
        assets = items[0].assets
        if not assets:
            raise ValueError(f"No assets found for item '{item_id}'")

        props = self.list_assets(item_id).properties
        valid_sex = set(props.sex.keys())
        valid_age = set(props.age_group.keys())

        def _norm(s): return re.sub(r"[^a-z0-9]+", "", (s or "").lower())
        def _to_list(v): return [] if v is None else [_norm(x) for x in (v if isinstance(v, (list, tuple, set)) else [v])]

        sex_list, age_list = _to_list(sex), _to_list(age_group)

        invalid_sex = [s for s in sex_list if s not in map(_norm, valid_sex)]
        invalid_age = [a for a in age_list if a not in map(_norm, valid_age)]
        if invalid_sex:
            raise ValueError(f"Unsupported sex values: {invalid_sex}. Supported: {list(valid_sex)}")
        if invalid_age:
            raise ValueError(f"Unsupported age_group values: {invalid_age}. Supported: {list(valid_age)}")
        
        matches = {}
        for key, asset in assets.items():
            props = getattr(asset, "extra_fields", {}) or {}
            a_sex, a_age = props.get("agesex:sex", ""), props.get("agesex:age_group", "")
            a_sex_label, a_age_label = props.get("agesex:sex_label", ""), props.get("agesex:age_label", "")
            if sex_list and not any(q in (_norm(a_sex), _norm(a_sex_label)) for q in sex_list):
                continue
            if age_list and not any(q in (_norm(a_age), _norm(a_age_label)) for q in age_list):
                continue
            matches[key] = {
                "sex": a_sex, "sex_label": a_sex_label,
                "age_group": a_age, "age_label": a_age_label, "href": asset.href,
            }
        return HTMLDict({"ids": list(matches.keys()), "assets": matches, "count": len(matches)})

    def fetch_asset(self, item_id: str, asset_key: str, download=False, plot=False,
                    polygon=None, out_dir=None):
        search = ItemSearch(url=self.BASE_URL, ids=[item_id])
        items = list(search.items())
        if not items:
            raise ValueError(f"No item found with ID '{item_id}'")

        asset = items[0].assets.get(asset_key)
        if not asset:
            raise ValueError(f"No asset found with key '{asset_key}' in item '{item_id}'")

        href, local_path, tmp_path = asset.href, None, None

        if download:
            out_dir = out_dir or tempfile.gettempdir()
            os.makedirs(out_dir, exist_ok=True)
            local_path = os.path.join(out_dir, os.path.basename(href))
            if not os.path.exists(local_path):
                r = requests.get(href, stream=True, timeout=60)
                r.raise_for_status()
                with open(local_path, "wb") as f:
                    for chunk in r.iter_content(8192):
                        if chunk:
                            f.write(chunk)

        if plot:
            src_path = None
            if download and local_path:
                src_path = local_path
            else:
                try:
                    rasterio.open(href)
                except Exception:
                    r = requests.get(href, stream=True, timeout=60)
                    r.raise_for_status()
                    with tempfile.NamedTemporaryFile(suffix=".tif", delete=False) as tmp:
                        for chunk in r.iter_content(8192):
                            if chunk:
                                tmp.write(chunk)
                        tmp_path = tmp.name
                    src_path = tmp_path
                else:
                    src_path = href

            with rasterio.open(src_path) as src:
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
                plt.colorbar(label="pop")
                plt.title(f"{item_id} - {asset_key}")
                plt.xlabel("lon")
                plt.ylabel("lat")
                plt.gca().set_aspect("equal", adjustable="box")
                plt.show()
            if tmp_path and os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except OSError:
                    pass

        return local_path if download else href if not plot else None


class HTMLDict(dict):
    """Dict with dot access, nested wrapping, and HTML repr."""
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.update(*args, **kwargs)

    def __setitem__(self, k, v):
        if isinstance(v, dict) and not isinstance(v, HTMLDict):
            v = HTMLDict(v)
        super().__setitem__(k, v)

    def __setattr__(self, n, v):
        if n.startswith("_"):
            super().__setattr__(n, v)
        else:
            self[n] = v

    def __getattr__(self, n):
        try:
            return self[n]
        except KeyError:
            raise AttributeError(f"'HTMLDict' object has no attribute '{n}'")

    def __delattr__(self, n):
        try:
            del self[n]
        except KeyError:
            raise AttributeError(f"'HTMLDict' object has no attribute '{n}'")

    def update(self, *args, **kwargs):
        other = dict(*args, **kwargs)
        for k, v in other.items():
            if isinstance(v, dict) and not isinstance(v, HTMLDict):
                v = HTMLDict(v)
            super().__setitem__(k, v)

    def _repr_html_(self):
        env = get_jinja_env()
        if env and "JSON.jinja2" in env.list_templates():
            template = env.get_template("JSON.jinja2")
            return template.render(dict=self, plain=escape(repr(self)))
        return escape(repr(self))
