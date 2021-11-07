import numpy as np
import pandas as pd

from giga.core.population import PopulationNode
from giga.core.knn import NearestNeighborsNode
from giga.core.student import StudentEstimateNode
from giga.core.teacher import TeacherEstimateNode
from giga.core.classroom import ClassroomEstimateNode
from giga.utils.logging import LOGGER


DEFAULT_SCHOOL_USE_RADIUS = 10.0 # km
DEFAULT_INTERNET_USE_RADIUS = 1.0 # km
DEFAULT_LOCATION_INPUT = ['Lat', 'Lon']
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
        location_input = kwargs.get('location_input', DEFAULT_LOCATION_INPUT)
        self.people_per_household = people_per_household
        self.school_use_radius = kwargs.get('school_use_radius', DEFAULT_SCHOOL_USE_RADIUS)
        self.internet_use_radius = kwargs.get('internet_use_radius', DEFAULT_INTERNET_USE_RADIUS)
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
                                                         location_input=location_input)

        self.nearest_neighbors_node = NearestNeighborsNode('nearest-neighbor-node',
                                                           school_locations,
                                                           location_input=location_input)
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

    def regional_census_estimate(self, data, params, radius, tag='school use'):
        n_neareby_schools = self.nearest_neighbors_node.run(data,
                                                            {**params,
                                                            **{'radius_nearest_neighbor': radius}})
        LOGGER.info(f"Completed nearby school estimate for {tag} in {radius} km radius")
        nearby_population = self.population_node.run(data,
                                                     {**params,
                                                     **{'radius': radius}})
        LOGGER.info(f"Completed nearby population estimate for {tag} in {radius} km radius")
        return n_neareby_schools, nearby_population

    def student_estiamte(self, nearby_schools, nearby_population, params):
        data = pd.DataFrame(list(zip(nearby_schools, nearby_population)), columns =[SCHOOL_USE_NERBY_COUNTS_VAR, SCHOOL_USE_POP_VAR])
        num_students = self.student_node.run(data, params)
        LOGGER.info("Completed student estimate")
        return num_students

    def teacher_estimate(self, num_students, params):
        data = pd.DataFrame(list(num_students), columns =[self.student_var])
        num_teachers = self.teacher_node.run(data, params)
        LOGGER.info("Completed teacher estimate")
        return num_teachers

    def classroom_estiamte(self, num_teachers, params):
        data = pd.DataFrame(list(num_teachers), columns =[self.teacher_var])
        num_classrooms = self.classroom_node.run(data, params)
        LOGGER.info("Completed classroom estimate")
        return num_classrooms

    def internet_use_estimate(self, nearby_schools, nearby_population):
        internet_use_population = np.round(nearby_population / nearby_schools)
        internet_use_households = np.round(internet_use_population / self.people_per_household)
        LOGGER.info(f"Completed internet use estimate for neabry population")
        return internet_use_population, internet_use_households

    def run(self, data, params):
        LOGGER.info("Starting census node")
        # school use census estaimte
        n_neareby_schools, nearby_school_population = self.regional_census_estimate(data,
                                                                                    params,
                                                                                    self.school_use_radius,
                                                                                    tag='school use')
        # student estimate
        num_students = self.student_estiamte(n_neareby_schools, nearby_school_population, params)
        # teacher estiamte
        num_teachers = self.teacher_estimate(num_students, params)
        # estimate number of classrooms
        num_classrooms = self.classroom_estiamte(num_teachers, params)
        # internet use census estimate
        internet_use_schools, nearby_population = self.regional_census_estimate(data,
                                                                                params,
                                                                                self.internet_use_radius,
                                                                                tag='internet use')
        # estimate nearby population + households for internet use
        internet_use_population, internet_use_households = self.internet_use_estimate(internet_use_schools,
                                                                                      nearby_population)
        return num_students, num_teachers, num_classrooms, internet_use_population, internet_use_households
