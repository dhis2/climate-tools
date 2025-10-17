from earthkit.transforms import aggregate

def aggregate_to_org_units(data, org_units, id_col='org_unit_id'):
    # aggregate to org unit for each time period
    agg_data = aggregate.spatial.reduce(data, org_units, mask_dim=id_col)
    # convert to dataframe
    agg_df = agg_data.to_dataframe().reset_index()
    # return
    return agg_df
