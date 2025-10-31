from html import escape
from dhis2eo.html.jinja_env import get_jinja_env
import re
import requests
from functools import lru_cache
from pystac_client import ItemSearch

class Manager:
    """
    Base class for STAC helpers.
    """
    SUPPORTED_SOURCES = ["worldpop", "sentinel"]

    @classmethod
    def list_supported_sources(cls):
        return cls.SUPPORTED_SOURCES

# WorldPop STAC helper using ItemSearch
class WorldPop(Manager):
    """
    STAC helper for WorldPop metadata.
    """
    BASE_URL = "https://api.stac.worldpop.org/search"
    COLLECTIONS_URL = "https://api.stac.worldpop.org/collections"
    SUPPORTED_PROPERTIES = {
        "years": [str(y) for y in range(2015, 2031)],
        "version": ["v1"],
        "projects": ["Population", "Age and Sex Structures"],
        "resolutions": ["100m", "1km"],
    }

    def list_properties(self):
        """
        Return all supported property values for WorldPop STAC queries.
        """
        return HTMLDict(self.SUPPORTED_PROPERTIES)
    
    @staticmethod
    @lru_cache(maxsize=1)
    def list_countries():
        """
        Fetch and cache the list of available country codes (STAC collections).
        """
        response = requests.get(WorldPop.COLLECTIONS_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        # Build a list of dicts with id and title when available
        countries = []
        for c in data.get("collections", []):
            cid = c.get("id", "").upper()
            title = c.get("title") or ""
            countries.append({"id": cid, "title": title})
        # Return sorted list of codes by id by default
        return HTMLDict({'countries': sorted(countries, key=lambda x: x["id"])}) if countries else HTMLDict({'countries': []})

    @staticmethod
    def find_country_code(name: str, as_dict: bool = True):
        """
        Find country code(s) by full country name.
        """
        if not name:
            return []

        # Ensure we have an up-to-date list
        countries = WorldPop.list_countries()['countries']
        # Normalization helper
        def _norm(s: str) -> str:
            return re.sub(r"[^a-z0-9]+", "", (s or "").lower())

        q = _norm(name)
        scored = []
        for c in countries:
            title = c.get("title") or ""
            ntitle = _norm(title)
            # exact or substring match always scores high
            if q == ntitle:
                score = 0
            elif q in ntitle:
                score = 1
            else:
                # no match
                score = 9999
            if score < 9999:
                scored.append((score, c))

        # sort by score then by id/title
        scored.sort(key=lambda x: (x[0], x[1].get("id", ""), x[1].get("title", "")))
        results = [c for _, c in scored]
        if as_dict:
            return HTMLDict({'countries': results})
        return HTMLDict({'countries': [r.get("id") for r in results]})

    def search_items(
        self, 
        year=None, 
        project=None, 
        resolution=None,
        bbox=None, 
        start_date=None, 
        end_date=None, 
        **kwargs
    ):
        """
        Search WorldPop STAC items.
        """
        # Validate inputs
        if year and str(year) not in self.SUPPORTED_PROPERTIES["years"]:
            raise ValueError(f"Unsupported year: {year}. Supported: {self.SUPPORTED_PROPERTIES['years']}")
        if project and project not in self.SUPPORTED_PROPERTIES["projects"]:
            raise ValueError(f"Unsupported project: {project}. Supported: {self.SUPPORTED_PROPERTIES['projects']}")
        if resolution and resolution not in self.SUPPORTED_PROPERTIES["resolutions"]:
            raise ValueError(f"Unsupported resolution: {resolution}. Supported: {self.SUPPORTED_PROPERTIES['resolutions']}")

        datetime_range = None
        if start_date and end_date:
            datetime_range = f"{start_date}/{end_date}"

        # Build query dict for STAC search
        query = {}
        if year:
            query["year"] = {"eq": str(year)}
        if project:
            query["project"] = {"eq": project}
        if resolution:
            query["resolution"] = {"eq": resolution}

        # Perform search
        search = ItemSearch(
            url=self.BASE_URL,
            collections=["population"],  # or dynamic if needed
            bbox=bbox,
            datetime=datetime_range,
            query=query,
            **kwargs
        )
        return HTMLDict(list(search.items()))

class HTMLDict(dict):
    def _repr_html_(self) -> str:
        jinja_env = get_jinja_env()
        if jinja_env and "JSON.jinja2" in jinja_env.list_templates():
            template = jinja_env.get_template("JSON.jinja2")
            return template.render(dict=self, plain=escape(repr(self)))
        else:
            return escape(repr(self))
