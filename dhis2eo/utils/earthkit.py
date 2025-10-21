from earthkit.transforms import aggregate

def aggregate_to_org_units(data, org_units, method, id_col='org_unit_id'):
    # aggregate to org unit for each time period
    #agg_data = aggregate.spatial.reduce(data, org_units, method=method, mask_dim=id_col)

    # mask based on org unit id
    id_mask = aggregate.spatial.mask(data, org_units, mask_dim=id_col)
    import logging
    logging.info(id_mask)

    # get aggregation method
    try:
        method_func = getattr(id_mask, method)
    except NameError:
        raise ValueError(f'Unsupported method value: {method}')

    # figure out which dimensions are spatial
    spatial_dims = [d for d in id_mask.dims if d in ("lat", "lon", "latitude", "longitude", "x", "y")]

    # aggregate the data
    agg_data = method_func(dim=spatial_dims, skipna=True)

    # convert to dataframe
    agg_df = agg_data.to_dataframe().reset_index()

    # return
    return agg_df
