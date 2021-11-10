from giga.models.census import CensusNode
from giga.core.consolidate import ConsolidationNode
from giga.core.primary_bandwidth import PrimaryBandwithNode
from giga.core.secondary_bandwidth import SecondaryBandwithNode
from giga.core.tech import TechnologyNode
from giga.core.cost import CostEstimateNode
from giga.core.revenue import RevenueNode
from giga.core.business import BusinessModelNode
from giga.utils.logging import LOGGER


FIXED_BANDWIDTH_FLAG = 'fixed_bandwidth'
PRIMARY_BANDWIDTH_SELECTOR = 'critical'
SECONDARY_BANDIWDTH_SELECTOR = 'non_critical'

REQUIRED_ARGUMENTS = ('population_file', 'consolidation_radius', 'school_age_fraction', # census
                      'school_enrollment_fraction', 'student_teacher_ratio', 'teacher_classroom_ratio',
                      'people_per_household', 'school_use_radius', 'internet_use_radius',
                      'emis_usage', 'portal_usage', 'emis_allowable_transfer_time', 'peak_hours', # bandwidth
                      'internet_browsing_bandwidth', 'allowable_website_loading_time',
                      'contention', 'fixed_bandwidth_rate',
                      'teacher_research_time', 'teacher_prep_hours', 'website_size',
                      'num_daily_assignments_per_student', 'student_prep_time',
                      'size_of_document', 'student_research_time', 'student_assignment_time',
                      'gdoc_bandwidth', 'allowable_completed_assignment_loading_time',
                      'video_data_rate', 'annual_checkups', 'illness_per_year',
                      'consults_per_illness', 'consult_time', 'consult_hours',
                      'weekly_sessions', 'session_length', 'community_access_hours',
                      'weekly_planning_time', 'fraction_of_planning_time_browsing',
                      'speed_2g', 'speed_3g', 'speed_4g', # tech
                      'connectivity_params', 'energy_params', 'labor_cost_skilled', 'labor_cost_regular', # cost
                      'subscription_conversion_default', 'fraction_community_using_school_internet', # revenue
                      'income_per_household', 'fraction_income_for_communications',
                      'revenue_over_cost_factor') # biz
OPTIONAL_ARGUMENTS = {'location_input': ['Lat', 'Lon'],
                      'student_output':'num_students',
                      'teacher_output': 'num_teachers',
                      'classroom_output': 'num_classrooms',
                      'population_output': 'nearby_population',
                      'households_output': 'nearby_households',
                      'bandwidth_output': 'bandwidth',
                      'critical_bandwidth_output': 'critical_bandwidth',
                      'non_ciritical_bandwidth_output': 'non_critical_bandwidth',
                      'technology_output': 'technology',
                      'overnight_cost_output': 'overnight_cost',
                      'annual_cost_output': 'annual_cost',
                      'annual_revenue_output': 'annual_revenue',
                      'business_model_output': 'explore_business_model',
                      'bandwidth_priority_model': 'both'}


class GigaNode:

    """
        Computational Node that encapsulates the end-to-end Giga model
    """

    def __init__(self, name, **kwargs):
        for k in REQUIRED_ARGUMENTS:
            assert k in kwargs, f"Missing required argument {k}"
        for attr in REQUIRED_ARGUMENTS:
            setattr(self, attr, kwargs.get(attr))
        for attr in OPTIONAL_ARGUMENTS.keys():
            setattr(self, attr, kwargs.get(attr, OPTIONAL_ARGUMENTS[attr]))

        # initalize compute steps
        # consolidation
        self.consolidation_node = ConsolidationNode('consolidation-node', **kwargs)
        # census
        self.census_node = CensusNode('census-node', **kwargs)
        # bandwidth
        self.primary_bandwidth_node = PrimaryBandwithNode('bandwidth-node', **kwargs)
        self.secondary_bandwidth_node = SecondaryBandwithNode('non-critical-bandwidth-node', **kwargs)
        # tech
        self.technology_node = TechnologyNode('technology-node', **kwargs)
        # cost
        self.cost_node = CostEstimateNode('cost-node', **kwargs)
        # revenue
        self.revenue_node = RevenueNode('revenue-node', **kwargs)
        # business
        self.business_node = BusinessModelNode('business-node', **kwargs)

    def from_giga_parameters(name, parameters, population_file_tiff, **kwargs):
        kwargs = {**kwargs, 
                  **vars(parameters),
                  **parameters.cell_connectivity_speeds,
                  **{'population_file': population_file_tiff}}
        return GigaNode(name, **kwargs)

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

    def add_bandwidths(self, data, params):
        if self.bandwidth_priority_model == PRIMARY_BANDWIDTH_SELECTOR:
            primary = self.primary_bandwidth_node.run(data, params)
            secondary = [0.0]*len(data)
        elif self.bandwidth_priority_model == SECONDARY_BANDIWDTH_SELECTOR:
            primary = [0.0]*len(data)
            secondary = self.secondary_bandwidth_node.run(data, params)
        else:
            primary = self.primary_bandwidth_node.run(data, params)
            secondary = self.secondary_bandwidth_node.run(data, params)
        data[self.critical_bandwidth_output] = primary
        data[self.non_ciritical_bandwidth_output] = secondary
        return primary + secondary


    def bandwidth(self, data, params):
        if FIXED_BANDWIDTH_FLAG in params and params[FIXED_BANDWIDTH_FLAG]:
            LOGGER.info(f"Using fixed bandwidth rate of {self.fixed_bandwidth_rate} Mbps")
            bw = [self.fixed_bandwidth_rate]*len(data)
        else:
            bw = self.add_bandwidths(data, params)
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
