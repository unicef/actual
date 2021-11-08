import numpy as np


SEC_PER_HR = 3600.0
KB_PER_MB = 1024
MIN_EMPLOYEES = 2
TEACHERS_PER_EMPLOYEE = 10


REQUIRED_ARGUMENTS = ('emis_usage', 'portal_usage', 'emis_allowable_transfer_time', 'peak_hours',
                      'internet_browsing_bandwidth', 'allowable_website_loading_time', 'contention')
OPTIONAL_ARGUMENTS = {'user_input': 'User',
                      'size_input': 'Size',
                      'frequency_input': 'Frequency',
                      'timeperiod_input': 'Time Period (Days)',
                      'student_input': 'num_students',
                      'teacher_input': 'num_teachers',
                      'classroom_input': 'num_classrooms',
                      'population_input': 'nearby_population',
                      'households_input': 'nearby_households'}

class PrimaryBandwithNode:

    def __init__(self, name, **kwargs):
        self.name = name
        assert all([k in kwargs for k in REQUIRED_ARGUMENTS]), f"Missing one or more required arguments {REQUIRED_ARGUMENTS}"
        for attr in REQUIRED_ARGUMENTS:
            setattr(self, attr, kwargs.get(attr))
        for attr in OPTIONAL_ARGUMENTS.keys():
            setattr(self, attr, kwargs.get(attr, OPTIONAL_ARGUMENTS[attr]))

    def create_roles(self, data):
        return {'Teachers': data[self.teacher_input],
                'Students': data[self.student_input],
                'Classroom': data[self.classroom_input],
                'School' : 1,
                'Employees': max(MIN_EMPLOYEES, np.floor(data[self.teacher_input] / TEACHERS_PER_EMPLOYEE)),
                'Households': data[self.households_input],
                'Individuals': data[self.population_input]}

    def estimate_emis_bw(self, datarow, roles):
        nagents = self.emis_usage[self.user_input].map(roles)
        self.emis_usage['data'] = self.emis_usage[self.size_input] * nagents
        emis_bws = self.emis_usage.groupby(self.frequency_input)['data'].sum() / (self.emis_allowable_transfer_time * SEC_PER_HR)
        return np.max(emis_bws) / KB_PER_MB

    def estimate_portal_bw(self, datarow, roles):
        nagents = self.portal_usage[self.user_input].map(roles)
        sessions = nagents / self.portal_usage[self.timeperiod_input]
        concurrent = sessions / self.peak_hours
        portal_bw = self.portal_usage[self.size_input] * concurrent / self.allowable_website_loading_time / self.contention / KB_PER_MB
        portal_bw = portal_bw.sum()
        return np.maximum(self.internet_browsing_bandwidth, portal_bw)

    def estimate_bw(self, datarow):
        roles = self.create_roles(datarow)
        emis_bw = self.estimate_emis_bw(datarow, roles)
        portal_bw = self.estimate_portal_bw(datarow, roles)
        return emis_bw + portal_bw

    def run(self, data, parameters):
        bw = data.apply(lambda row: self.estimate_bw(row), axis=1)
        return bw