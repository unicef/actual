import pandas as pd

from giga.core.population import PopulationNode
from giga.core.knn import NearestNeighborsNode
from giga.core.student import StudentEstimateNode
from giga.utils.logging import LOGGER


DEFAULT_SCHOOL_USE_RADIUS = 10.0 # km
DEFAULT_CENSUS_RADIUS = 1.0 # km
SCHOOL_USE_POP_VAR = 'school_use_population'
SCHOOL_USE_NERBY_COUNTS_VAR = 'school_use_nearby_counts'


class CensusNode:

	def __init__(self, population_file,
					   school_locations,
					   school_age_fraction,
					   school_enrollment_fraction,
					   **kwargs):
		lon_input = kwargs.get('lon_key', 'Lon')
		lat_input = kwargs.get('lat_key', 'Lat')
		self.school_use_radius = kwargs.get('school_use_radius', DEFAULT_SCHOOL_USE_RADIUS)
		self.census_radius = kwargs.get('census_radius', DEFAULT_CENSUS_RADIUS)
		self.compute_students = kwargs.get('compute_students', True)
		self.compute_teachers = kwargs.get('compute_teachers', True)
		# initialize compute nodes needed to perform a full census
		self.population_node = PopulationNode.from_tiff('population-node', population_file,
														lon_input=lon_input,
														lat_inpit=lat_input)
		self.nearest_neighbors_node = NearestNeighborsNode('nearest-neighbor-node',
														   school_locations,
														   pt_input=[lat_input, lon_input])
		self.student_node = StudentEstimateNode('student-node', 
												school_age_fraction, 
												school_enrollment_fraction,
												population_input=SCHOOL_USE_POP_VAR,
												school_input=SCHOOL_USE_NERBY_COUNTS_VAR)




		self.student_output = kwargs.get('student_output', 'num_students')
		self.teacher_output = kwargs.get('teacher_output', 'num_teachers')
		self.classroom_output = kwargs.get('classroom_output', 'num_classrooms')
		self.population_output = kwargs.get('population_output', 'nearby_population')
		self.households_output = kwargs.get('households_output', 'nearby_households')

	def run(self, data, params):
		LOGGER.info("Starting census node")
		# find nearest schools
		n_neareby_schools = self.nearest_neighbors_node.run(data, 
															{**params, 
															 **{'radius_nearest_neighbor': self.school_use_radius}})
		LOGGER.info("Completed nearby school estimate")

		# find nearby population
		nearby_school_population = self.population_node.run(data, 
														    {**params,
														     **{'radius': self.school_use_radius}})
		LOGGER.info("Completed nearby population estimate")

		# find nearby students
		temp = pd.DataFrame(list(zip(n_neareby_schools, nearby_school_population)), columns =[SCHOOL_USE_NERBY_COUNTS_VAR, SCHOOL_USE_POP_VAR])
		num_students = self.student_node.run(temp, params)
		LOGGER.info("Completed student estimate")



		"""
		student_output = kwargs.get('student_output', 'num_students')
		teacher_output = kwargs.get('teacher_output', 'num_teachers')
		classroom_output = kwargs.get('classroom_output', 'num_classrooms')
		population_output = kwargs.get('population_output', 'nearby_population')
		households_output = kwargs.get('households_output', 'nearby_households')
		# get num students, teachers, classrooms
		# get neraby pop
		# get num households
		data[self.student_output] = num_students
		"""

		return num_students
