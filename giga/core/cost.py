
WH_PER_KWH = 1000

ENERGY_TYPE_IDENTIFIER = 'Type'
CONNECTIVITY_TYPE_IDENTIFIER = 'Type'

OVERNIGHT_COST_VAR = 'overnight'
ANNUAL_COST_VAR = 'annual'

REQUIRED_ARGUMENTS = ('connectivity_params', 'energy_params', 'labor_cost_skilled', 'labor_cost_regular')
OPTIONAL_ARGUMENTS = {'technology_input': 'technology',
                      'power_parameter': 'Power',
                      'solar_parameter': 'Solar',
                      'battery_parameter': 'Battery'}


class CostEstimateNode:

    def __init__(self, name, **kwargs):
        self.name = name
        assert all([k in kwargs for k in REQUIRED_ARGUMENTS]), f"Missing one or more required arguments {REQUIRED_ARGUMENTS}"
        for attr in REQUIRED_ARGUMENTS:
            setattr(self, attr, kwargs.get(attr))
        for attr in OPTIONAL_ARGUMENTS.keys():
            setattr(self, attr, kwargs.get(attr, OPTIONAL_ARGUMENTS[attr]))

    @property
    def battery_cost(self):
        return self.energy_params[self.energy_params[ENERGY_TYPE_IDENTIFIER] == self.battery_parameter]

    @property
    def solar_cost(self):
        return self.energy_params[self.energy_params[ENERGY_TYPE_IDENTIFIER] == self.solar_parameter]

    def estimate_overnight_fixed_cost(self):
        labor = self.connectivity_params['Overnight Labor Fixed'] * self.labor_cost_skilled
        return self.connectivity_params['Setup Fees'] + self.connectivity_params['Overnight Hardware Fixed'] + labor

    def estimate_annual_cost(self, fixed):
        hw_cost = self.connectivity_params['Annual Hardware'] * fixed
        labor_cost = self.connectivity_params['Annual Labor Time'] * self.labor_cost_regular
        return hw_cost + labor_cost + self.connectivity_params['Annual Fees']

    def compute_technology_cost_estimates(self):
        overnight_fixed_cost = self.estimate_overnight_fixed_cost()
        annual_cost = self.estimate_annual_cost(overnight_fixed_cost)
        costs = self.connectivity_params.copy()
        costs[OVERNIGHT_COST_VAR] = overnight_fixed_cost
        costs[ANNUAL_COST_VAR] = annual_cost
        return costs

    def compute_cost(self, datarow, costs):
        tech_cost = costs[costs[CONNECTIVITY_TYPE_IDENTIFIER] == datarow[self.technology_input]]
        return float(tech_cost[OVERNIGHT_COST_VAR]), float(tech_cost[ANNUAL_COST_VAR])

    def run(self, data, params):
        tech_costs = self.compute_technology_cost_estimates()
        costs = data.apply(lambda row: self.compute_cost(row, tech_costs), axis=1, result_type='expand')
        overnight, annual = costs[0].to_numpy(), costs[1].to_numpy()
        return overnight, annual
        