from giga.core.population import PopulationNode
from giga.core.knn import NearestNeighborsNode


DEFAULT_SCHOOL_USE_RADIUS = 10.0 # km
DEFAULT_CENSUS_RADIUS = 1.0 # km


class CensusNode:

	def __init__(self, population_file,
					   school_locations,
					   school_age_fraction,
					   school_enrollment_fraction,
					   **kwargs):
		lon_input = kwargs.get('lon_key', 'Lon')
		lat_input = kwargs.get('lat_key', 'Lat')
		# initialize compute nodes needed to perform a full census
		self.population_node = PopulationNode.from_tiff('population-node', population_file,
														lon_input=lon_input,
														lat_inpit=lat_input)
		self.nearest_neighbors_node = NearestNeighborsNode('nearest-neighbor-node',
														   school_locations,
														   pt_input=[lat_input, lon_input])


		self.school_use_radius = kwargs.get('school_use_radius', DEFAULT_SCHOOL_USE_RADIUS)
		self.census_radius = kwargs.get('census_radius', DEFAULT_CENSUS_RADIUS)

		self.student_output = kwargs.get('student_output', 'num_students')
		self.teacher_output = kwargs.get('teacher_output', 'num_teachers')
		self.classroom_output = kwargs.get('classroom_output', 'num_classrooms')
		self.population_output = kwargs.get('population_output', 'nearby_population')
		self.households_output = kwargs.get('households_output', 'nearby_households')

	def run(self, data, params):
		# get num students, teachers, classrooms
		# get neraby pop
		# get num households
		data[self.student_output] = num_students

		return data
