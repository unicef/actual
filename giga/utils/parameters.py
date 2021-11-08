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

    def connectivity_speed(self, conn_type):
        return float(self.table_params['connectivity'][self.table_params['connectivity']['Type'] == conn_type]['Speed'])

    @property
    def emis(self):
        return self.table_params['emis']

    @property
    def portal(self):
        return self.table_params['portal']

    @property
    def connectivity(self):
        return self.table_params['connectivity']

    @property
    def energy(self):
        return self.table_params['energy']

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

    @property
    def labor_cost_skilled_hr(self):
        return self.named_params['Skilled Labor Cost per Hour']

    @property
    def labor_cost_regular_hr(self):
        return self.named_params['Regular Labor Cost per Hour']

    @property
    def fraction_community_using_school_internet(self):
        return self.named_params['Fraction of Community Using School Internet']

    @property
    def income_per_household(self):
        return self.named_params['Income per Household']

    @property
    def fraction_income_for_communications(self):
        return self.named_params['Fraction of Income on Communications']

    @property
    def subscription_conversion_default(self):
        return self.named_params['Default Subscription Conversion Rate']

    @property
    def revenue_over_cost_factor(self):
        return self.named_params['Revenue Over Cost Factor']

    @property
    def speed_2g(self):
        return self.connectivity_speed('2G')

    @property
    def speed_3g(self):
        return self.connectivity_speed('3G')

    @property
    def speed_4g(self):
        return self.connectivity_speed('4G')
