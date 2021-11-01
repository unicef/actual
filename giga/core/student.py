import numpy as np


class StudentEstimateNode:
	"""
		School census computation node used for inferring the
		the number of students from the population data of surrounding region
	"""

	def __init__(self, name, 
					   school_age_fraction,
					   school_enrollment_fraction,
					   **kwargs):
		self.name = name
		self.school_age_fraction = school_age_fraction
		self.school_enrollment_fraction = school_enrollment_fraction
		# optional/default parameters
		self.population_input = kwargs.get('population_input', 'nearby_population')
		self.school_input = kwargs.get('school_input', 'nearby_schools')

	def estimate_number_students(self, datarow):
		students_to_people = self.school_age_fraction * self.school_enrollment_fraction
		people_to_schools = datarow[self.population_input] / (datarow[self.school_input] + 1)
		return np.ceil(students_to_people * people_to_schools)

	def run(self, data, parameters):
		num_students = data.apply(lambda row: self.estimate_number_students(row), axis=1)
		return num_students
