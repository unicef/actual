from giga.models.census import CensusNode
from giga.core.consolidate import ConsolidationNode
from giga.core.primary_bandwidth import PrimaryBandwithNode
from giga.core.tech import TechnologyNode
from giga.core.cost import CostEstimateNode
from giga.core.revenue import RevenueNode
from giga.core.business import BusinessModelNode
from giga.utils.logging import LOGGER

DEFAULT_LOCATION_INPUT = ['Lat', 'Lon']
REQUIRED_INPUTS = ['tiff_file']
FIXED_BANDWIDTH_FLAG = 'fixed_bandwidth'

class GigaNode:

    """
        Computational Node that encapsulates the end-to-end Giga model
    """

    def __init__(self, 
                 population_file_tiff,
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

                 speed_2g,
                 speed_3g,
                 speed_4g,

                 conn_params,
                 energy_params,
                 labor_cost_skilled_hr,
                 labor_cost_regular_hr,

                 subscription_conversion_default,
                 fraction_community_using_school_internet,
                 income_per_household,
                 fraction_income_for_communications,

                 revenue_over_cost_factor,

                 **kwargs):
        # TODO: reduce input size, make census_params, bandwidth_params, tech_params

        # project inputs
        self.fixed_bandwidth_rate = fixed_bandwidth_rate
        # optional arguments
        self.location_input = kwargs.get('location_input', DEFAULT_LOCATION_INPUT) # dataframe keys for school locations

        # initalize compute steps
        # consolidation
        self.consolidation_node = ConsolidationNode('consolidation-node', consolidation_radius=consolidation_radius)
        # census
        self.census_node = CensusNode(population_file_tiff,
                                      school_age_fraction,
                                      school_enrollment_fraction,
                                      student_teacher_ratio,
                                      teacher_classroom_ratio,
                                      people_per_household,
                                      school_use_radius=school_use_radius,
                                      internet_use_radius=internet_use_radius)
        # bandwidth
        self.primary_bandwidth_node = PrimaryBandwithNode('bandwidth-node',
                                                          emis_params,
                                                          portal_params,
                                                          emis_allowable_transfer_time,
                                                          peak_hours,
                                                          internet_browsing_bandwidth,
                                                          allowable_website_loading_time,
                                                          contention)

        # tech
        self.technology_node = TechnologyNode('technology-node',
                                              speed_4g,
                                              speed_3g,
                                              speed_2g)

        # cost
        self.cost_node = CostEstimateNode('cost-node',
                                          conn_params,
                                          energy_params,
                                          labor_cost_skilled_hr,
                                          labor_cost_regular_hr)

        # revenue
        self.revenue_node = RevenueNode('revenue-node',
                                         conn_params,
                                         subscription_conversion_default,
                                         fraction_community_using_school_internet,
                                         income_per_household,
                                         fraction_income_for_communications)

        # business
        self.business_node = BusinessModelNode('business-node', revenue_over_cost_factor)

        # output vars
        self.student_output = kwargs.get('student_output', 'num_students')
        self.teacher_output = kwargs.get('teacher_output', 'num_teachers')
        self.classroom_output = kwargs.get('classroom_output', 'num_classrooms')
        self.population_output = kwargs.get('population_output', 'nearby_population')
        self.households_output = kwargs.get('households_output', 'nearby_households')
        self.bandwidth_output = kwargs.get('bandwidth_output', 'bandwidth')
        self.technology_output = kwargs.get('technology_output', 'technology')
        self.overnight_cost_output = kwargs.get('overnight_cost_output', 'overnight_cost')
        self.annual_cost_output = kwargs.get('annual_cost_output', 'annual_cost')
        self.annual_revenue_output = kwargs.get('annual_revenue_output', 'annual_revenue')
        self.business_model_output = kwargs.get('business_model_output', 'explore_business_model')

    def from_giga_parameters(parameters, population_file_tiff, **kwargs):
        return GigaNode(population_file_tiff,
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
                        # technology
                        parameters.speed_2g,
                        parameters.speed_3g,
                        parameters.speed_4g,
                        # cost
                        parameters.connectivity,
                        parameters.energy,
                        parameters.labor_cost_skilled_hr,
                        parameters.labor_cost_regular_hr,
                        # revenue
                        parameters.subscription_conversion_default,
                        parameters.fraction_community_using_school_internet,
                        parameters.income_per_household,
                        parameters.fraction_income_for_communications,
                        # business
                        parameters.revenue_over_cost_factor,
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
            bw = self.primary_bandwidth_node.run(data, params)
        data[self.bandwidth_output] = bw
        LOGGER.info(f"Completed bandwidth estimate")
        return data

    def technology(self, data, params):
        tech = self.technology_node.run(data, params)
        data[self.technology_output] = tech
        LOGGER.info("Completed technology assesment")
        return data

    def cost(self, data, params):
        overnight, annual = self.cost_node.run(data, params)
        data[self.overnight_cost_output] = overnight
        data[self.annual_cost_output] = annual
        LOGGER.info("Completed cost estimate")
        return data

    def revenue(self, data, params):
        annual_revenue = self.revenue_node.run(data, params)
        data[self.annual_revenue_output] = annual_revenue
        LOGGER.info("Completed revenue estimate")
        return data

    def business(self, data, params):
        explore_business_model = self.business_node.run(data, params)
        data[self.business_model_output] = explore_business_model
        LOGGER.info("Completed business model assesment")
        return data

    def run(self, data, params):
        LOGGER.info("Starting giga node")
        # pre process
        giga_data = self.consolidate(data, params)
        # run census model
        giga_data = self.census(giga_data, params)
        # run bandwidth model
        giga_data = self.bandwidth(giga_data, params)
        # run technology model
        giga_data = self.technology(giga_data, params)
        # run cost model
        giga_data = self.cost(giga_data, params)
        # run revenue model
        giga_data = self.revenue(giga_data, params)
        # run business model
        giga_data = self.business(giga_data, params)
        return giga_data



