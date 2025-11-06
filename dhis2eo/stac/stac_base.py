class STAC:
    """Base class for STAC helpers."""
    SUPPORTED_SOURCES = ["WorldPop"]

    @classmethod
    def list_supported_sources(cls):
        return cls.SUPPORTED_SOURCES

