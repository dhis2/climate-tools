import os
import sys
import functools
import hashlib
import tempfile
import logging

import xarray as xr

logger = logging.getLogger(__name__)

# Since this module is so download centric, force all info logs to be printed
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter('%(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)
logger.setLevel(logging.INFO)

def netcdf_cache(cache_dir=None):
    """Cache xarray results to disk as netcdf using module + function name in key."""
    cache_dir = cache_dir or tempfile.gettempdir()
    os.makedirs(cache_dir, exist_ok=True)

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Identify the function uniquely by module + qualified name
            func_id = f"{func.__module__}.{func.__qualname__}"

            # Create a hash of the arguments
            key_data = str(args) + str(kwargs)
            key_hash = hashlib.md5(key_data.encode()).hexdigest()[:10]

            # Combine everything into a filename
            safe_func_id = func_id.replace(".", "_")
            filename = f"{safe_func_id}_{key_hash}.nc"
            path = os.path.join(cache_dir, filename)

            if os.path.exists(path):
                logger.info(f'Loading from cache: {path}')
                return xr.open_dataset(path)

            else:
                # run the download function
                ds = func(*args, **kwargs)
                
                # save to cache
                ds.to_netcdf(path)
                
                # return from cached path to ensure same results every time
                ds = xr.open_dataset(path)
                return ds

        return wrapper
    return decorator
