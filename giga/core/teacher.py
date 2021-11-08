import numpy as np


REQUIRED_ARGUMENTS = ('student_teacher_ratio',)
OPTIONAL_ARGUMENTS = {'student_input': 'num_students',}


class TeacherEstimateNode:
    """
        School census computation node used for inferring the
        the number of students from the population data of surrounding region
    """

    def __init__(self, name, **kwargs):
        self.name = name
        assert all([k in kwargs for k in REQUIRED_ARGUMENTS]), f"Missing one or more required arguments {REQUIRED_ARGUMENTS}"
        for attr in REQUIRED_ARGUMENTS:
            setattr(self, attr, kwargs.get(attr))
        for attr in OPTIONAL_ARGUMENTS.keys():
            setattr(self, attr, kwargs.get(attr, OPTIONAL_ARGUMENTS[attr]))

    def estimate_number_teachers(self, datarow):
        if datarow[self.student_input] == 0:
            # no teachers if there are no students
            return 0
        n_teachers = np.ceil(datarow[self.student_input] / self.student_teacher_ratio)
        # there should be at least one teacher if there are students
        n_teachers = max(1.0, n_teachers)
        return n_teachers

    def run(self, data, parameters):
        num_teachers = data.apply(lambda row: self.estimate_number_teachers(row), axis=1)
        return num_teachers
