
from giga.models.census import CensusNode
from giga.core.consolidate import ConsolidationNode
from giga.core.primary_bandwidth import PrimaryBandwithNode
from giga.utils.logging import LOGGER

DEFAULT_LOCATION_INPUT = ['Lat', 'Lon']
REQUIRED_INPUTS = ['tiff_file']
FIXED_BANDWIDTH_FLAG = 'fixed_bandwidth'

class GigaNode:

    """
        Computational Node that encapsulates the end-to-end Giga model
    """

    def __init__(self, 
                 tiff_file,
                 consolidation_radius,
                 school_age_fraction,
                 school_enrollment_fraction,
                 student_teacher_ratio,
                 teacher_classroom_ratio,
                 people_per_household,
                 school_use_radius,
                 internet_use_radius,

                 emis_params,
                 portal_params,
                 emis_allowable_transfer_time,
                 peak_hours,
                 internet_browsing_bandwidth,
                 allowable_website_loading_time,
                 contention,
                 fixed_bandwidth_rate,

                 **kwargs):

        # project inputs
        self.fixed_bandwidth_rate = fixed_bandwidth_rate
        # optional arguments
        self.location_input = kwargs.get('location_input', DEFAULT_LOCATION_INPUT) # dataframe keys for school locations

        # initalize compute steps
        # consolidation
        self.consolidation_node = ConsolidationNode('consolidation-node', consolidation_radius=consolidation_radius)
        # census
        self.census_node = CensusNode(tiff_file,
                                      school_age_fraction,
                                      school_enrollment_fraction,
                                      student_teacher_ratio,
                                      teacher_classroom_ratio,
                                      people_per_household,
                                      school_use_radius=school_use_radius,
                                      internet_use_radius=internet_use_radius)
        # bandwidth
        self.primary_bandwidth_node = PrimaryBandwithNode(emis_params,
                                                          portal_params,
                                                          emis_allowable_transfer_time,
                                                          peak_hours,
                                                          internet_browsing_bandwidth,
                                                          allowable_website_loading_time,
                                                          contention)

        # output vars
        self.student_output = kwargs.get('student_output', 'num_students')
        self.teacher_output = kwargs.get('teacher_output', 'num_teachers')
        self.classroom_output = kwargs.get('classroom_output', 'num_classrooms')
        self.population_output = kwargs.get('population_output', 'nearby_population')
        self.households_output = kwargs.get('households_output', 'nearby_households')
        self.bandwidth_output = kwargs.get('bandwidth_output', 'bandwidth')

    def from_giga_parameters(parameters, tiff_file, **kwargs):
        return GigaNode(tiff_file,
                        # census
                        parameters.consolidation_radius,
                        parameters.school_age_fraction,
                        parameters.school_enrollment_fraction,
                        parameters.student_teacher_ratio,
                        parameters.teacher_classroom_ratio,
                        parameters.people_per_household,
                        parameters.school_use_radius,
                        parameters.internet_use_radius,
                        # bandwidth
                        parameters.emis,
                        parameters.portal,
                        parameters.emis_allowable_transfer_time,
                        parameters.peak_hours,
                        parameters.internet_browsing_bandwidth,
                        parameters.allowable_website_loading_time,
                        parameters.contention,
                        parameters.fixed_bandwidth_rate,
                        **kwargs)


    def consolidate(self, data, params):
        to_consolidate = self.consolidation_node.run(data, params)
        datap = data[to_consolidate].copy().reset_index() # create a new consolidated frame
        LOGGER.info(f"School consolidation, inital input with {len(data)} entries, consolidated to {len(datap)}")
        return datap

    def census(self, data, params):
        # compute
        num_students, num_teachers, num_classrooms, nearby_population, nearby_households = self.census_node.run(data, params)
        # assign
        data[self.student_output] = num_students
        data[self.teacher_output] = num_teachers
        data[self.classroom_output] = num_classrooms
        data[self.population_output] = nearby_population
        data[self.households_output] = nearby_households
        LOGGER.info(f"Completed census node")
        return data

    def bandwidth(self, data, params):
        if FIXED_BANDWIDTH_FLAG in params and params[FIXED_BANDWIDTH_FLAG]:
            LOGGER.info(f"Using fixed bandwidth rate of {self.fixed_bandwidth_rate} Mbps")
            bw = [self.fixed_bandwidth_rate]*len(data)
        else:
            bw = self.primary_bandwidth_node.run(data, {})
        data[self.bandwidth_output] = bw
        LOGGER.info(f"Completed bandwidth estimate")
        return data

    def run(self, data, params):
        LOGGER.info("Starting giga node")
        # pre process
        giga_data = self.consolidate(data, params)
        # run census model
        giga_data = self.census(giga_data, params)
        # run bandwidth model
        giga_data = self.bandwidth(giga_data, params)

        return giga_data # feasible tech costs?



