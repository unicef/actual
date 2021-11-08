import numpy as np


REQUIRED_ARGUMENTS = ('teacher_classroom_ratio',)
OPTIONAL_ARGUMENTS = {'teacher_input': 'num_teachers',}


class ClassroomEstimateNode:
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

    def estimate_number_classrooms(self, datarow):
        return np.round(datarow[self.teacher_input] / self.teacher_classroom_ratio)

    def run(self, data, parameters):
        num_classrooms = data.apply(lambda row: self.estimate_number_classrooms(row), axis=1)
        return num_classrooms
