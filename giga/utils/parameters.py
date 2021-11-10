import json
import pandas as pd

from giga.utils.parse import fetch_all_params_from_gsheet, serialize_params, deserialize_params


NAMED_PARAMETERS = ['project', 'usage', 'assignment', 'community', 'lesson', 'telemedicine', 'model']
TABULAR_PARAMETERS = ['emis', 'portal', 'connectivity', 'energy']

SPREADSHEET_TO_GIGA_MAP = {'School Consolidation Radius': 'consolidation_radius', 'School Age Fraction': 'school_age_fraction',
                           'School Enrollment Fraction': 'school_enrollment_fraction',
                           'Student Teacher Ratio': 'student_teacher_ratio',
                           'Teacher Classroom Ratio': 'teacher_classroom_ratio',
                           'People per Household': 'people_per_household',
                           'School Use Radius': 'school_use_radius',
                           'Teacher Research Time': 'teacher_research_time',
                           'Teacher Prep Hours': 'teacher_prep_hours',
                           'Size of Website': 'website_size',
                           'Number of Daily Assignments Per Student': 'num_daily_assignments_per_student',
                           'Student Prep Time': 'student_prep_time',
                           'Size of Document': 'size_of_document',
                           'Student Research Time': 'student_research_time',
                           'Student Assignments Time': 'student_assignment_time',
                           'Google Docs Bandwidth': 'gdoc_bandwidth',
                           'Allowable Completed Assignments Loading Time': 'allowable_completed_assignment_loading_time',
                           'Video Data Rate (480p)': 'video_data_rate',
                           'Annual Checkups': 'annual_checkups',
                           'Illness per Year': 'illness_per_year',
                           'Consults per Illness': 'consults_per_illness',
                           'Consult time': 'consult_time',
                           'Consult hours': 'consult_hours',
                           'Weekly Sessions': 'weekly_sessions',
                           'Session Length': 'session_length',
                           'Community Access Hours': 'community_access_hours',
                           'Weekly Planning Time': 'weekly_planning_time',
                           'Fraction of Planning Time Browsing': 'fraction_of_planning_time_browsing',
                           'Internet Use Radius': 'internet_use_radius',
                           'EMIS Allowable Transfer Time': 'emis_allowable_transfer_time','Peak Hours': 'peak_hours',
                           'Internet Browsing Bandwidth': 'internet_browsing_bandwidth',
                           'Allowable Website Loading Time': 'allowable_website_loading_time','Contention': 'contention',
                           'Fixed Bandwidth Rate': 'fixed_bandwidth_rate',
                           'Skilled Labor Cost per Hour': 'labor_cost_skilled',
                           'Regular Labor Cost per Hour': 'labor_cost_regular',
                           'Default Subscription Conversion Rate': 'subscription_conversion_default',
                           'Fraction of Community Using School Internet': 'fraction_community_using_school_internet',
                           'Income per Household': 'income_per_household',
                           'Fraction of Income on Communications': 'fraction_income_for_communications',
                           'Revenue Over Cost Factor': 'revenue_over_cost_factor',
                           'emis': 'emis_usage','portal': 'portal_usage', 'connectivity': 'connectivity_params',
                           'energy': 'energy_params'}


class GigaParameters:

    def __init__(self, params):
        self.params = params
        # unpack the parameters
        self.named_params = {}
        for n in NAMED_PARAMETERS:
            named = {row['Name']: row['Value'] for _, row in params[n].iterrows()}
            self.named_params = {**self.named_params, **named}
        self.table_params = {n: params[n] for n in TABULAR_PARAMETERS}
        for param, val in self.named_params.items():
            if param in SPREADSHEET_TO_GIGA_MAP:
                setattr(self, SPREADSHEET_TO_GIGA_MAP[param], val)
        for param, val in self.table_params.items():
            setattr(self, SPREADSHEET_TO_GIGA_MAP[param], val)

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
    def cell_connectivity_speeds(self):
        return {'speed_2g': self.connectivity_speed('2G'),
                'speed_3g': self.connectivity_speed('3G'),
                'speed_4g': self.connectivity_speed('4G')}
