import numpy as np
import pandas as pd

from giga.core.population import PopulationNode
from giga.core.knn import NearestNeighborsNode
from giga.core.student import StudentEstimateNode
from giga.core.teacher import TeacherEstimateNode
from giga.core.classroom import ClassroomEstimateNode
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
					   student_teacher_ratio,
					   teacher_classroom_ratio,
					   people_per_household,
					   **kwargs):
		lon_input = kwargs.get('lon_key', 'Lon')
		lat_input = kwargs.get('lat_key', 'Lat')
		self.people_per_household = people_per_household
		self.school_use_radius = kwargs.get('school_use_radius', DEFAULT_SCHOOL_USE_RADIUS)
		self.census_radius = kwargs.get('census_radius', DEFAULT_CENSUS_RADIUS)
		self.compute_students = kwargs.get('compute_students', True)
		self.compute_teachers = kwargs.get('compute_teachers', True)
		# output vars
		self.student_var = kwargs.get('student_output', 'num_students')
		self.teacher_var = kwargs.get('teacher_output', 'num_teachers')
		self.classroom_var = kwargs.get('classroom_output', 'num_classrooms')
		self.population_var = kwargs.get('population_output', 'nearby_population')
		self.households_var = kwargs.get('households_output', 'nearby_households')
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
		self.teacher_node = TeacherEstimateNode('teacher-node',
												 student_teacher_ratio,
												 student_input=self.student_var)
		self.classroom_node = ClassroomEstimateNode('classroom-node',
			 										 teacher_classroom_ratio,
			 										 teacher_input=self.teacher_var)

	def run(self, data, params):
		LOGGER.info("Starting census node")
		# find nearest schools 
		n_neareby_schools = self.nearest_neighbors_node.run(data, 
															{**params, 
															 **{'radius_nearest_neighbor': self.school_use_radius}})
		LOGGER.info(f"Completed nearby school estimate for school use in {self.school_use_radius} km radius")
		# find nearby population
		nearby_school_population = self.population_node.run(data, 
														    {**params,
														     **{'radius': self.school_use_radius}})
		LOGGER.info(f"Completed nearby population estimate for school use in {self.school_use_radius} km radius")
		# estimate number of students
		temp = pd.DataFrame(list(zip(n_neareby_schools, nearby_school_population)), columns =[SCHOOL_USE_NERBY_COUNTS_VAR, SCHOOL_USE_POP_VAR])
		num_students = self.student_node.run(temp, params)
		LOGGER.info("Completed student estimate")
		# estimate number of teachers
		temp = pd.DataFrame(list(zip(num_students)), columns =[self.student_var])
		num_teachers = self.teacher_node.run(temp, params)
		LOGGER.info("Completed teacher estimate")
		# estimate number of classrooms
		temp = pd.DataFrame(list(num_teachers), columns =[self.teacher_var])
		num_classrooms = self.classroom_node.run(temp, params)
		LOGGER.info("Completed classroom estimate")
		# estimate nearby schools for internet use population
		n_neareby_schools_internet_use = self.nearest_neighbors_node.run(data, 
																		{**params, 
															 			 **{'radius_nearest_neighbor': self.census_radius}})
		LOGGER.info(f"Completed nearby school estimate for internent use in {self.census_radius} km radius")
		# estimate nearby population for internet use
		nearby_population_internet_use = self.population_node.run(data, 
														    	 {**params,
														     	 **{'radius': self.census_radius}})
		nearby_population = np.round(nearby_population_internet_use / n_neareby_schools_internet_use)
		LOGGER.info(f"Completed nearby population estimate for internet use in {self.census_radius} km radius")

		# estimate local internet use households
		neabry_households = np.round(nearby_population / self.people_per_household)
		LOGGER.info(f"Completed nearby households estimate for internet use in {self.census_radius} km radius")
		return num_students, num_teachers, num_classrooms, nearby_population, neabry_households
