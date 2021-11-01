import numpy as np


class ClassroomEstimateNode:
	"""
		School census computation node used for inferring the
		the number of students from the population data of surrounding region
	"""

	def __init__(self, name,
					   teacher_classroom_ratio,
					   **kwargs):
		self.name = name
		self.teacher_classroom_ratio = teacher_classroom_ratio
		# optional/default parameters
		self.teacher_input = kwargs.get('teacher_input', 'num_teachers')

	def estimate_number_classrooms(self, datarow):
		return np.round(datarow[self.teacher_input] / self.teacher_classroom_ratio)

	def run(self, data, parameters):
		num_classrooms = data.apply(lambda row: self.estimate_number_classrooms(row), axis=1)
		return num_classrooms