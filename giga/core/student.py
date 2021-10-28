import numpy as np


class StudentEstimateNode:
	"""
		School census computation node used for inferring the
		the number of students from the population data of surrounding region
	"""

	def __init__(self, name, **kwargs):
		self.name = name
		# optional/default parameters
		self.school_age_fraction = kwargs.get('school_age_fraction')
		self.school_enrollment_fraction = kwargs.get('school_enrollment_fraction')
		self.population_key = kwargs.get('population_key', 'nearby_population')
		self.school_key = kwargs.get('school_key', 'nearby_schools')

	def estimate_number_students(self, datarow):
		students_to_people = self.school_age_fraction * self.school_enrollment_fraction
		people_to_schools = datarow[self.population_key] / (datarow[self.school_key] + 1)
		return np.ceil(students_to_people * people_to_schools)

	def run(self, data, parameters):
		num_students = data.apply(lambda row: self.estimate_number_students(row), axis=1)
		return num_students
