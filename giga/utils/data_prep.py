import pandas as pd


def cell_coverage_type(row):
    if row['4G']:
        return '4G'
    if row['3G']:
        return '3G'
    if row['2G']:
        return '2G'
    return '0G'

def zw_base_to_giga_format(df):
    # transforms the given input format for Zimbabwe data into giga modeling framework format
    df = df.rename(columns={'latitude': 'Lat',
                            'longitude': 'Lon',
                            'fiber_node_distance': 'Distance to Nearest Fiber'})
    df['Type of Cell Coverage'] = df.apply(cell_coverage_type, axis=1)
    return df

