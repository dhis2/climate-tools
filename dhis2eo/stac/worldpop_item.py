from .html_dict import HTMLDict
from .worldpop_asset import WorldPopAsset

class WorldPopItem(HTMLDict):
    ITEM_PROPERTIES = [
        "version",
        "year",
        "project",
        "resolution",
    ]

    def __init__(self, item_dict):
        if not isinstance(item_dict, dict):
            raise TypeError(f"Expected dict for item_dict, got {type(item_dict)}")
        metadata = {
            "id": item_dict.get("id"),
            "bbox": item_dict.get("bbox"),
            "type": item_dict.get("type", "Feature"),
            "geometry": item_dict.get("geometry"),
            "collection": item_dict.get("collection"),
            "properties": item_dict.get("properties", {}),
        }
        assets_dict = item_dict.get("assets", {}) or {}
        metadata["assets"] =  {k: WorldPopAsset(v) for k, v in assets_dict.items()}
        super().__init__(metadata)

    def list_asset_properties(self):
        if self["properties"]["project"] == "Population":
            return HTMLDict({})
        if self["properties"]["project"] == "Age and Sex Structures":
            values = {k: set() for k in WorldPopAsset.ASSET_PROPERTIES}
            for asset in self["assets"].values():
                for key in WorldPopAsset.ASSET_PROPERTIES:
                    key_wprefix = f"{WorldPopAsset.ASSET_PROPERTIES_PREFIX}:{key}"
                    if key_wprefix in asset and asset[key_wprefix]:
                        values[key].add(asset[key_wprefix])
            values = {k: sorted(v) for k, v in values.items()}
            return HTMLDict(values)
    
    def search_assets(self, sexes=None, sex_labels=None, age_groups=None, age_labels=None):
        
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
                valid_values = set(self.list_asset_properties()[key])
            invalid = [v for v in values if v not in valid_values]
            if invalid:
                raise ValueError(f"Invalid {key}(s): {invalid}. Allowed: {sorted(valid_values)}")
            
        sexes = to_list(sexes)
        sex_labels = to_list(sex_labels)
        age_groups = to_list(age_groups)
        age_labels = to_list(age_labels)

        validate("sex", sexes)
        validate("sex_label", sex_labels)
        validate("age_group", age_groups)
        validate("age_label", age_labels)

        search = {}
        prefix = WorldPopAsset.ASSET_PROPERTIES_PREFIX
        for id, asset in self["assets"].items():
            sex, sex_label = asset.get(f"{prefix}:sex", ""), asset.get(f"{prefix}:sex_label", "")
            age_group, age_label = asset.get(f"{prefix}:age_group", ""), asset.get(f"{prefix}:age_label", "")
            if (sexes or sex_labels) and not any(q in (sex, sex_label) for q in (sexes + sex_labels)):
                continue
            if (age_groups or age_labels) and not any(q in (age_group, age_label) for q in (age_groups + age_labels)):
                continue 
            search[id] = asset
        return HTMLDict({"ids": list(search.keys()), "assets": search, "count": len(search)})


    def get_asset(self, sex=None, sex_label=None, age_group=None, age_label=None):
                
        search = self.search_assets(sex, sex_label, age_group, age_label)
        
        if self["properties"]["project"] == "Population":
            return search['assets']['data']
       
        if search["count"] == 0:
            raise ValueError(f"No asset found for parameters.")
        if search["count"] > 1:
            raise ValueError(f"Multiple assets found for parameters.")
        
        return search['assets'][search.ids[0]]
