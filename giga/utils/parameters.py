import json
import pandas as pd

from giga.utils.parse import fetch_all_params_from_gsheet, serialize_params, deserialize_params


NAMED_PARAMETERS = ['project', 'usage', 'assignment', 'community', 'lesson', 'telemedicine', 'model']
TABULAR_PARAMETERS = ['emis', 'portal', 'connectivity', 'energy']


class GigaParameters:

    def __init__(self, params):
        self.params = params
        # unpack the parameters
        self.named_params = {}
        for n in NAMED_PARAMETERS:
            named = {row['Name']: row['Value'] for _, row in params[n].iterrows()}
            self.named_params = {**self.named_params, **named}
        self.table_params = {n: params[n] for n in TABULAR_PARAMETERS}

    @staticmethod
    def from_google_sheet(docid):
        params = fetch_all_params_from_gsheet(docid)
        return GigaParameters(params)

    @staticmethod
    def from_json(filename):
        with open(filename) as f:
            p = json.load(f)
        params = deserialize_params(p)
        return GigaParameters(params)
        
    def to_json(self, filename):
        with open(filename, 'w') as f:
            json.dump(serialize_params(self.params), f, indent=4)

    @property
    def consolidation_radius(self):
        return self.named_params['School Consolidation Radius']
