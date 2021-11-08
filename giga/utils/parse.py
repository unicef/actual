import json
import pandas as pd


DEFAULT_DOCID = "1LsOLtcZG8FO9uF79H7Z_PdN6iHkuMyr5TXw3UllbahE"
# Spreadsheet locations for the google sheet document above
# https://docs.google.com/spreadsheets/d/1LsOLtcZG8FO9uF79H7Z_PdN6iHkuMyr5TXw3UllbahE/edit#gid=0
# parmas = (gid, columns, start row, end row)
DEFAULT_PROJECT_PARAMS = ('0', range(0,3), 3, 13)
DEFAULT_USAGE_PARAMS = ('0', range(0,3), 16, 28)
DEFAULT_ASSIGNMENT_PARAMS = ('0', range(0,3), 31, 37)
DEFAULT_COMMUNITY_PARAMS = ('0', range(0,3), 40, 45)
DEFAULT_LESSON_PARAMS = ('0', range(0,3), 48, 50)
DEFAULT_TELEMEDICINE_PARAMS = ('0', range(0,3), 53, 58)
DEFAULT_MODEL_PARAMS = ('0', range(0,3), 61, 66)
DEFAULT_EMIS_PARAMS = ('0', range(4,10), 3, 20)
DEFAULT_PORTAL_PARMS = ('0', range(11,18), 3, 9)
DEFAULT_CONNECTIVITY_PARAMS = ('0', range(19,31), 3, 10)
DEFAULT_ENERGY_PARAMS = ('0', range(32,40), 3, 5)



def shool_data_from_excel(file):
    return pd.read_excel(file, engine='openpyxl')

def get_gsheet_download_url(docid, gid="0"):
    return f"https://docs.google.com/spreadsheets/d/{docid}/export?format=xlsx&gid={gid}"

def format_gsheet_keys(frame, delim='.'):
    new_columns = {}
    for k in frame.keys():
        if delim in k:
            new_k = k.split(delim)[0]
            new_columns[k] = new_k
    return frame.rename(columns=new_columns)

def fetch_from_excel(file, cols, row_start, row_end):
    nrows = row_end - row_start
    return pd.read_excel(file, 
                         engine='openpyxl', 
                         usecols=cols,
                         skiprows=row_start-1,
                         nrows=nrows)

def fetch_from_gsheet(docid, 
                      gid,
                      cols,
                      row_start,
                      row_end):
    url = get_gsheet_download_url(docid, gid=gid)
    emis = format_gsheet_keys(fetch_from_excel(url, cols, row_start, row_end))
    return emis

def to_ordered_dict(df):
    out = []
    for i, row in df.iterrows():
        out.append(json.loads(row.to_json()))
    return out

def serialize_params(p):
    serialized = {}
    for k, v in p.items():
        serialized[k] = to_ordered_dict(v)
    return serialized

def deserialize_params(p):
    deserealized = {}
    for k, v in p.items():
        deserealized[k] = pd.DataFrame(data=v)
    return deserealized

def fetch_all_params_from_gsheet(docid):
    return {'project': fetch_from_gsheet(docid, *DEFAULT_PROJECT_PARAMS),
            'usage': fetch_from_gsheet(docid, *DEFAULT_USAGE_PARAMS),
            'assignment': fetch_from_gsheet(docid, *DEFAULT_ASSIGNMENT_PARAMS),
            'community': fetch_from_gsheet(docid, *DEFAULT_COMMUNITY_PARAMS),
            'lesson': fetch_from_gsheet(docid, *DEFAULT_LESSON_PARAMS),
            'telemedicine': fetch_from_gsheet(docid, *DEFAULT_TELEMEDICINE_PARAMS),
            'model': fetch_from_gsheet(docid, *DEFAULT_MODEL_PARAMS),
            'emis': fetch_from_gsheet(docid, *DEFAULT_EMIS_PARAMS),
            'portal': fetch_from_gsheet(docid, *DEFAULT_PORTAL_PARMS),
            'connectivity': fetch_from_gsheet(docid, *DEFAULT_CONNECTIVITY_PARAMS),
            'energy': fetch_from_gsheet(docid, *DEFAULT_ENERGY_PARAMS)}

def fetch_default_params():
    return fetch_all_params_from_gsheet(DEFAULT_DOCID)
