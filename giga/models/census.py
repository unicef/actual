import numpy as np
import pandas as pd

from giga.core.population import PopulationNode
from giga.core.knn import NearestNeighborsNode
from giga.core.student import StudentEstimateNode
from giga.core.teacher import TeacherEstimateNode
from giga.core.classroom import ClassroomEstimateNode
from giga.utils.logging import LOGGER


STUDENT_VAR = 'num_students'
TEACHER_VAR = 'num_teachers'
SCHOOL_USE_POP_VAR = 'school_use_population'
SCHOOL_USE_NERBY_COUNTS_VAR = 'school_use_nearby_counts'

REQUIRED_ARGUMENTS = ('population_file', 'school_age_fraction', 'school_enrollment_fraction',
                      'student_teacher_ratio', 'teacher_classroom_ratio', 'people_per_household')
OPTIONAL_ARGUMENTS = {'location_input': ['Lat', 'Lon'],
                      'school_use_radius': 10.0, # km
                      'internet_use_radius': 1.0, # km
                      }


class CensusNode:

    def __init__(self, name, **kwargs):
        self.name = name
        assert all([k in kwargs for k in REQUIRED_ARGUMENTS]), f"Missing one or more required arguments {REQUIRED_ARGUMENTS}"
        for attr in REQUIRED_ARGUMENTS:
            setattr(self, attr, kwargs.get(attr))
        for attr in OPTIONAL_ARGUMENTS.keys():
            setattr(self, attr, kwargs.get(attr, OPTIONAL_ARGUMENTS[attr]))
        # initialize compute nodes needed to perform a full census
        self.population_node = PopulationNode.from_tiff('population-node', self.population_file,
                                                         location_input=self.location_input)
        self.nearest_neighbors_node = NearestNeighborsNode('nearest-neighbor-node',
                                                           np.zeros((1, len(self.location_input))), # default input
                                                           location_input=self.location_input)
        self.student_node = StudentEstimateNode('student-node',
                                                population_input=SCHOOL_USE_POP_VAR,
                                                school_input=SCHOOL_USE_NERBY_COUNTS_VAR,
                                                **kwargs)
        self.teacher_node = TeacherEstimateNode('teacher-node',
                                                student_input=STUDENT_VAR,
                                                **kwargs)
        self.classroom_node = ClassroomEstimateNode('classroom-node',
                                                    teacher_input=TEACHER_VAR,
                                                    **kwargs)

    def update_nodes(self, data, params):
        # dynamically update nodes based on input data
        # single update needed - reindex nearest neighbor node
        locations = data[self.location_input].to_numpy()
        self.nearest_neighbors_node.reindex(locations)

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
        data = pd.DataFrame(list(num_students), columns =[STUDENT_VAR])
        num_teachers = self.teacher_node.run(data, params)
        LOGGER.info("Completed teacher estimate")
        return num_teachers

    def classroom_estiamte(self, num_teachers, params):
        data = pd.DataFrame(list(num_teachers), columns =[TEACHER_VAR])
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
        # update nodes using input data if needed
        self.update_nodes(data, params)
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
