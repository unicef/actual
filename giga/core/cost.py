
WH_PER_KWH = 1000

ENERGY_TYPE_IDENTIFIER = 'Type'
CONNECTIVITY_TYPE_IDENTIFIER = 'Type'

OVERNIGHT_COST_VAR = 'overnight'
ANNUAL_COST_VAR = 'annual'



class CostEstimateNode:

    def __init__(self, name,
                       tech_costs,
                       energy_costs,
                       labor_cost_skilled,
                       labor_cost_regular,
                       **kwargs):
        self.name = name
        self.tech_costs = tech_costs
        self.energy_costs = energy_costs
        self.labor_cost_skilled = labor_cost_skilled
        self.labor_cost_regular = labor_cost_regular
        # optional arguments
        self.technology_input = kwargs.get('technology_input', 'technology')
        self.power_parameter = kwargs.get('power_parameter', 'Power')
        self.solar_parameter = kwargs.get('solar_parameter', 'Solar')
        self.battery_parameter = kwargs.get('batter_parameter', 'Battery')

    @property
    def battery_cost(self):
        return self.energy_costs[self.energy_cost[ENERGY_TYPE_IDENTIFIER] == self.battery_parameter]

    @property
    def solar_cost(self):
        return self.energy_costs[self.energy_cost[ENERGY_TYPE_IDENTIFIER] == self.solar_parameter]

    def estimate_overnight_energy_cost(self, power_required, costs):
        pass

    def estimate_energy_costs(self):
        battery_overnight = self.estimate_overnight_cost(self.tech_costs[self.power_input])
        solar_overnight = self.estimate_overnight_cost(self.tech_costs)

    def estimate_overnight_fixed_cost(self):
        labor = self.tech_costs['Overnight Labor Fixed'] * self.labor_cost_skilled
        return self.tech_costs['Setup Fees'] + self.tech_costs['Overnight Hardware Fixed'] + labor

    def estimate_overnight_variable_cost(self):
        pass

    def estimate_annual_cost(self, fixed):
        hw_cost = self.tech_costs['Annual Hardware'] * fixed
        labor_cost = self.tech_costs['Annual Labor Time'] * self.labor_cost_regular
        return hw_cost + labor_cost + self.tech_costs['Annual Fees']

    def compute_technology_cost_estimates(self):
        overnight_fixed_cost = self.estimate_overnight_fixed_cost()
        annual_cost = self.estimate_annual_cost(overnight_fixed_cost)
        costs = self.tech_costs.copy()
        costs[OVERNIGHT_COST_VAR] = overnight_fixed_cost
        costs[ANNUAL_COST_VAR] = annual_cost
        return costs

    def compute_cost(self, datarow, costs):
        #print(datarow[self.technology_input], costs[CONNECTIVITY_TYPE_IDENTIFIER])
        tech_cost = costs[costs[CONNECTIVITY_TYPE_IDENTIFIER] == datarow[self.technology_input]]
        return float(tech_cost[OVERNIGHT_COST_VAR]), float(tech_cost[ANNUAL_COST_VAR])

    def run(self, data, params):
        tech_costs = self.compute_technology_cost_estimates()
        costs = data.apply(lambda row: self.compute_cost(row, tech_costs), axis=1, result_type='expand')
        overnight, annual = costs[0].to_numpy(), costs[1].to_numpy()
        return overnight, annual
        