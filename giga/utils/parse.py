import pandas as pd


def fetch_from_excel(file, cols, row_start, row_end):
    nrows = row_end - row_start
    return pd.read_excel(file, 
                         engine='openpyxl', 
                         usecols=cols,
                         skiprows=row_start-1,
                         nrows=nrows)