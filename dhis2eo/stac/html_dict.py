from html import escape
from dhis2eo.html.jinja_env import get_jinja_env

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
