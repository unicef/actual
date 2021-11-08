import numpy as np


REQUIRED_ARGUMENTS = ('school_age_fraction', 'school_enrollment_fraction')
OPTIONAL_ARGUMENTS = {'population_input': 'nearby_population',
                      'school_input': 'nearby_schools'}


class StudentEstimateNode:
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

    def estimate_number_students(self, datarow):
        students_to_people = self.school_age_fraction * self.school_enrollment_fraction
        people_to_schools = datarow[self.population_input] / (datarow[self.school_input] + 1)
        return np.ceil(students_to_people * people_to_schools)

    def run(self, data, parameters):
        num_students = data.apply(lambda row: self.estimate_number_students(row), axis=1)
        return num_students
