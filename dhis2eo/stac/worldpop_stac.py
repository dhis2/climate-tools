import re, requests
from functools import lru_cache
from pystac_client import ItemSearch

from .stac_base import STAC
from .worldpop_item import WorldPopItem
from .html_dict import HTMLDict

class WorldPopSTAC(STAC):
    COLLECTIONS_URL = "https://api.stac.worldpop.org/collections"
    SEARCH_URL = "https://api.stac.worldpop.org/search"

    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.collections = self._verify_endpoint(self.COLLECTIONS_URL, "collections", True).get("collections", [])
        self._verify_endpoint(self.SEARCH_URL, "search")

    def _verify_endpoint(self, url: str, name: str, return_data=False):
        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
        except requests.exceptions.Timeout:
            raise ConnectionError(f"Timeout while trying to reach the {name} endpoint: {url}")
        except requests.exceptions.ConnectionError:
            raise ConnectionError(f"Could not connect to the {name} endpoint: {url}")
        except requests.exceptions.HTTPError as e:
            raise ConnectionError(f"{name.capitalize()} endpoint returned an HTTP error: {e}")

        try:
            data = response.json()
        except ValueError:
            raise ValueError(f"{name.capitalize()} endpoint did not return valid JSON: {url}")
        
        if return_data:
            return data

    @lru_cache(maxsize=1)
    def list_countrycodes(self):
        countries = {c.get("id", "").upper(): c.get("title", "") for c in self.collections}
        return HTMLDict({"countries": countries})

    @lru_cache(maxsize=1)
    def list_item_properties(self):
        values = self.collections[0]["summaries"]
        values["collection"] = list(self.list_countrycodes()["countries"].keys())
        # Fix errors in WP collections summaries
        values['year'] = [str(y) for y in values.pop('years')]
        values['project'] = values.pop('projects')
        values["resolution"] = ['1km' if r == '1km_ua' else r for r in values.pop("resolutions")]
        return HTMLDict(values)

    def search_countrycode(self, name: str):
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

        countries = self.list_countrycodes()["countries"]
        scored = [{"score": _score(q, title, code), "code": code, "title": title}
                  for code, title in countries.items()]
        scored = [s for s in scored if s["score"] < 9999]
        scored.sort(key=lambda x: (x["score"], x["code"], x["title"]))
        return HTMLDict({"top": scored[0] if scored else None, "countries": scored, "count": len(scored)})

    def get_countrycode(self, name: str):
        
        search = self.search_countrycode(name)
       
        if search["count"] == 0:
            raise ValueError(f"No countrycode found for parameters: {name}")
        if search["count"] > 1:
            raise ValueError(f"Multiple countrycodes found for parameters: {name}")
        
        return search["top"]["code"]

    def search_items(self, collections=None, years=None, projects=None, resolutions=None,
                     bbox=None, start_date=None, end_date=None, **kwargs):
        
        def to_list(val):
            if val is None:
                return []
            if isinstance(val, str):
                return [v.strip() for v in val.split(",") if v.strip()]
            if isinstance(val, (list, tuple, set)):
                return list(val)
            return [val]
        
        def validate(key, values, valid_values = None):
            if not values:
                return
            if not valid_values:
                valid_values = set(self.list_item_properties()[key])
            invalid = [v for v in values if v not in valid_values]
            if invalid:
                raise ValueError(f"Invalid {key}(s): {invalid}. Allowed: {sorted(valid_values)}")
        
        collections = [str(c).upper() for c in to_list(collections)]
        years = [str(y) for y in to_list(years)]
        projects = to_list(projects)
        resolutions = to_list(resolutions)

        validate("collection", collections, set(self.list_countrycodes()["countries"].keys()))
        validate("year", years)
        validate("project", projects)
        validate("resolution", resolutions)

        datetime_range = f"{start_date}/{end_date}" if start_date and end_date else None
        
        def filter_part(property, values):
            if not values:
                return None
            if len(values) == 1:
                return {"op": "eq", "args": [ {"property": property}, values[0] ]}
            return {
                "op": "or",
                "args": [ {"op": "eq", "args": [ {"property": property}, v ]} for v in values ]
            }

        filter_args = [f for f in [
            filter_part("year", years),
            filter_part("project", projects),
            filter_part("resolution", resolutions)
        ] if f is not None]

        if filter_args:
            filter_obj = {"op": "and", "args": filter_args}
        else:
            filter_obj = None

        search = ItemSearch(
            url=self.SEARCH_URL,
            collections=collections if collections else None,
            bbox=bbox,
            datetime=datetime_range,
            filter=filter_obj,
            **kwargs,
        )

        items = list(search.items_as_dicts())

        return HTMLDict({
            "ids": [i["id"] for i in items],
            "items": {i["id"]: WorldPopItem(i) for i in items},
            "count": len(items),
        })
    
    def get_item(self, collection=None, year=None, project=None, resolution=None,
                     bbox=None, start_date=None, end_date=None, **kwargs):
        
        search = self.search_items(collection, year, project, resolution,
                           bbox, start_date, end_date, **kwargs)
       
        if search["count"] == 0:
            raise ValueError(f"No item found for parameters.")
        if search["count"] > 1:
            raise ValueError(f"Multiple items found for parameters.")
        
        return search['items'][search.ids[0]]
