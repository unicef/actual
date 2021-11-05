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
DEFAULT_EMIS_PARAMS = ('0', range(4,10), 3, 20)
DEFAULT_PORTAL_PARMS = ('0', range(11,18), 3, 9)
DEFAULT_CONNECTIVITY_PARAMS = ('0', range(19,30), 3, 10)
DEFAULT_ENERGY_PARAMS = ('0', range(31,39), 3, 5)



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

def fetch_project_from_gsheet(docid):
    return fetch_from_gsheet(docid, *DEFAULT_PROJECT_PARAMS)

def fetch_usage_from_gsheet(docid):
    return fetch_from_gsheet(docid, *DEFAULT_USAGE_PARAMS)

def fetch_assignment_from_gsheet(docid):
    return fetch_from_gsheet(docid, *DEFAULT_ASSIGNMENT_PARAMS)

def fetch_community_from_gsheet(docid):
    return fetch_from_gsheet(docid, *DEFAULT_COMMUNITY_PARAMS)

def fetch_lesson_from_gsheet(docid):
    return fetch_from_gsheet(docid, *DEFAULT_LESSON_PARAMS)

def fetch_telemedicine_from_gsheet(docid):
    return fetch_from_gsheet(docid, *DEFAULT_TELEMEDICINE_PARAMS)

def fetch_emis_from_gsheet(docid):
    return fetch_from_gsheet(docid, *DEFAULT_EMIS_PARAMS)

def fetch_portal_from_gsheet(docid):
    return fetch_from_gsheet(docid, *DEFAULT_PORTAL_PARMS)

def fetch_connectivity_from_gsheet(docid):
    return fetch_from_gsheet(docid, *DEFAULT_CONNECTIVITY_PARAMS)

def fetch_energy_from_gsheet(docid):
    return fetch_from_gsheet(docid, *DEFAULT_ENERGY_PARAMS)

def fetch_all_params_from_gsheet(docid):
    return {'project': fetch_project_from_gsheet(docid),
            'usage': fetch_usage_from_gsheet(docid),
            'assignment': fetch_assignment_from_gsheet(docid),
            'community': fetch_community_from_gsheet(docid),
            'lesson': fetch_lesson_from_gsheet(docid),
            'telemedicine': fetch_telemedicine_from_gsheet(docid),
            'emis': fetch_emis_from_gsheet(docid),
            'portal': fetch_portal_from_gsheet(docid),
            'connectivity': fetch_connectivity_from_gsheet(docid),
            'energy': fetch_energy_from_gsheet(docid)}
