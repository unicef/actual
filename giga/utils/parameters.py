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
    def emis(self):
        return self.table_params['emis']

    @property
    def portal(self):
        return self.table_params['portal']

    @property
    def fixed_bandwidth_rate(self):
        return self.named_params['Fixed Bandwidth Rate']

    @property
    def consolidation_radius(self):
        return self.named_params['School Consolidation Radius']

    @property
    def school_use_radius(self):
        return self.named_params['School Use Radius']

    @property
    def internet_use_radius(self):
        return self.named_params['Internet Use Radius']

    @property
    def school_age_fraction(self):
        return self.named_params['School Age Fraction']

    @property
    def school_enrollment_fraction(self):
        return self.named_params['School Enrollment Fraction']

    @property
    def student_teacher_ratio(self):
        return self.named_params['Student Teacher Ratio']

    @property
    def teacher_classroom_ratio(self):
        return self.named_params['Teacher Classroom Ratio']

    @property
    def people_per_household(self):
        return self.named_params['People per Household']

    @property
    def emis_allowable_transfer_time(self):
        return self.named_params['EMIS Allowable Transfer Time']

    @property
    def peak_hours(self):
        return self.named_params['Peak Hours']

    @property
    def internet_browsing_bandwidth(self):
        return self.named_params['Internet Browsing Bandwidth']

    @property
    def allowable_website_loading_time(self):
        return self.named_params['Allowable Website Loading Time']

    @property
    def contention(self):
        return self.named_params['Contention']
