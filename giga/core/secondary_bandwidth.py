import numpy as np


DAYS_PER_YEAR = 365
DAYS_PER_WEEK = 7
SCHOOL_DAYS_PER_WEEK = 5
SEC_PER_HR = 3600.0
MINUTES_PER_HOUR = 60.0
KB_PER_MB = 1024
AVERAGE_ASSIGNMENTS_GRADED = 8

REQUIRED_ARGUMENTS = ('teacher_research_time', 'teacher_prep_hours', 'website_size',
                      'allowable_website_loading_time', 'num_daily_assignments_per_student',
                      'student_prep_time', 'size_of_document', 'student_research_time',
                      'student_assignment_time', 'gdoc_bandwidth',
                      'allowable_completed_assignment_loading_time', 'video_data_rate',
                      'annual_checkups', 'illness_per_year', 'consults_per_illness',
                      'consult_time', 'consult_hours', 'internet_browsing_bandwidth',
                      'fraction_community_using_school_internet', 'weekly_sessions',
                      'session_length', 'community_access_hours', 'contention',
                      'weekly_planning_time', 'fraction_of_planning_time_browsing')
OPTIONAL_ARGUMENTS = {'student_input': 'num_students',
                      'teacher_input': 'num_teachers',
                      'classroom_input': 'num_classrooms',
                      'population_input': 'nearby_population',
                      'households_input': 'nearby_households'}


class SecondaryBandwithNode:

    def __init__(self, name, **kwargs):
        self.name = name
        assert all([k in kwargs for k in REQUIRED_ARGUMENTS]), f"Missing one or more required arguments {REQUIRED_ARGUMENTS}"
        for attr in REQUIRED_ARGUMENTS:
            setattr(self, attr, kwargs.get(attr))
        for attr in OPTIONAL_ARGUMENTS.keys():
            setattr(self, attr, kwargs.get(attr, OPTIONAL_ARGUMENTS[attr]))

    def assignment_bw(self, data):
        # assignment creation
        per_teacher = (self.teacher_research_time / self.teacher_prep_hours) * self.website_size / self.allowable_website_loading_time
        bw = data[self.teacher_input] * per_teacher / KB_PER_MB
        # assignment access
        per_student = self.num_daily_assignments_per_student / (SEC_PER_HR * self.student_prep_time)
        bw += data[self.student_input] * per_student * self.size_of_document / KB_PER_MB
        # assignment research
        per_student = self.student_research_time / self.student_prep_time * self.website_size / self.allowable_website_loading_time
        bw += data[self.student_input] * per_student / KB_PER_MB
        # assignment completion
        per_student = self.student_assignment_time / self.student_prep_time * self.gdoc_bandwidth
        bw += data[self.student_input] * per_student / KB_PER_MB
        # assignment grading
        per_teacher = self.size_of_document / self.allowable_completed_assignment_loading_time * AVERAGE_ASSIGNMENTS_GRADED
        per_teacher += self.gdoc_bandwidth
        bw += data[self.teacher_input] * per_teacher / KB_PER_MB
        return bw

    def instructional_video_bw(self, data):
        # Recorded Instructional Clips
        return data[self.classroom_input] * self.video_data_rate

    def telemedicine_bw(self, data):
        # Telemedicine Consultations
        sessions_per_day = (self.annual_checkups + self.illness_per_year * self.consults_per_illness) / DAYS_PER_YEAR
        hours_per_day = sessions_per_day * (self.consult_time / self.consult_hours)
        usage_per_person = self.video_data_rate * hours_per_day
        return data[self.population_input] * usage_per_person

    def community_access_bw(self, data):
        # On-premise community internet access
        hours_per_person = self.weekly_sessions / DAYS_PER_WEEK * self.session_length / MINUTES_PER_HOUR
        bw_per_person = hours_per_person / self.community_access_hours * self.internet_browsing_bandwidth
        net_bw = data[self.population_input] * self.fraction_community_using_school_internet * bw_per_person / self.contention
        return np.maximum(self.internet_browsing_bandwidth, net_bw)

    def lesson_planning_bw(self, data):
        hours_per_teacher = self.weekly_planning_time / SCHOOL_DAYS_PER_WEEK * self.fraction_of_planning_time_browsing / self.teacher_prep_hours
        return data[self.teacher_input] * hours_per_teacher * self.internet_browsing_bandwidth

    def estimate_bw(self, datarow):
        community_bw = self.telemedicine_bw(datarow) + self.community_access_bw(datarow)
        education_bw = self.assignment_bw(datarow) + self.instructional_video_bw(datarow) + self.lesson_planning_bw(datarow)
        return community_bw + education_bw

    def run(self, data, parameters):
        bw = data.apply(lambda row: self.estimate_bw(row), axis=1)
        return bw