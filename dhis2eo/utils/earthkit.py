import earthkit.transforms.aggregate
import xarray as xr

def aggregate_to_org_units(data, org_units, variables, id_col='org_unit_id'):
    # aggregate to org unit for each time period
    # note: a bit strange, but the earthkit aggregate doesnt allow specifying aggregation method
    #agg_data = earthkit.transforms.aggregate.spatial.reduce(data, org_units, method=method, mask_dim=id_col)

    # mask based on org unit id
    data_with_mask = earthkit.transforms.aggregate.spatial.mask(data, org_units, mask_dim=id_col, all_touched=True)

    # get aggregation method
    def aggregate(xarray, variable, method):
        # get aggregation function for specific xarray variable
        try:
            method_func = getattr(xarray[variable], method)
        except NameError:
            raise ValueError(f'Unsupported method value: {method}')
        # apply the aggregation function while keeping the spatial dimensions
        agg = method_func(dim=spatial_dims, skipna=True)
        # return aggregated data for the variable
        return agg

    # figure out which dimensions are spatial
    spatial_dims = [d for d in data_with_mask.dims if d in ("lat", "lon", "latitude", "longitude", "x", "y")]

    # aggregate the data
    agg_data = xr.Dataset(
        {
            var: aggregate(data_with_mask, var, agg)
            for var, agg in variables.items()
            if var in data_with_mask
        }
    )

    # convert to dataframe
    agg_df = agg_data.to_dataframe().reset_index()

    # return
    return agg_df
