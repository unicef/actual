import numpy as np


class TeacherEstimateNode:
	"""
		School census computation node used for inferring the
		the number of students from the population data of surrounding region
	"""

	def __init__(self, name,
					   student_teacher_ratio,
					   **kwargs):
		self.name = name
		self.student_teacher_ratio = student_teacher_ratio
		# optional/default parameters
		self.student_input = kwargs.get('student_input', 'num_students')

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
