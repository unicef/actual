import numpy as np


SEC_PER_HR = 3600.0
KB_PER_MB = 1024
MIN_EMPLOYEES = 2
TEACHERS_PER_EMPLOYEE = 10

class PrimaryBandwithNode:

    def __init__(self, name,
                       emis_usage,
                       portal_usage, 
                       emis_allowable_transfer_time_hrs,
                       peak_hours,
                       internet_browsing_bandwidth,
                       allowable_website_loading_time,
                       contention,
                       **kwargs):
        self.name = name
        self.emis_usage = emis_usage
        self.portal_usage = portal_usage
        self.emis_allowable_transfer_time = emis_allowable_transfer_time_hrs * SEC_PER_HR
        self.peak_hours = peak_hours
        self.internet_browsing_bandwidth = internet_browsing_bandwidth
        self.allowable_website_loading_time = allowable_website_loading_time
        self.contention = contention
        # optional params
        self.user_input = kwargs.get('user_input', 'User')
        self.size_input = kwargs.get('size_input', 'Size')
        self.frequency_input = kwargs.get('freqeuncy_input', 'Frequency')
        self.timeperiod_input = kwargs.get('timeperiod_input', 'Time Period (Days)')

        self.student_input = kwargs.get('student_input', 'num_students')
        self.teacher_input = kwargs.get('teacher_input', 'num_teachers')
        self.classroom_input = kwargs.get('classroom_input', 'num_classrooms')
        self.population_input = kwargs.get('population_input', 'nearby_population')
        self.households_input = kwargs.get('households_input', 'nearby_households')
        

    def create_roles(self, data):
        return {'Teachers': data[self.teacher_input],
                'Students': data[self.student_input],
                'Classroom': data[self.classroom_input],
                'School' : 1,
                'Employees': max(MIN_EMPLOYEES, np.floor(data[self.teacher_input] / TEACHERS_PER_EMPLOYEE)),
                'Households': data[self.households_input],
                'Individuals': data[self.population_input]}

    def estimate_emis_bw(self, datarow, roles):
        per_use = self.emis_allowable_transfer_time * SEC_PER_HR
        nagents = self.emis_usage[self.user_input].map(roles)
        self.emis_usage['data'] = self.emis_usage[self.size_input] * nagents
        emis_bws = self.emis_usage.groupby(self.frequency_input)['data'].sum() / self.emis_allowable_transfer_time
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