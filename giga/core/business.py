

class BusinessModelNode:

    def __init__(self,
                 name,
                 revenue_over_cost_factor,
                 **kwargs):
        self.name = name
        self.revenue_over_cost_factor = revenue_over_cost_factor
        # optional params
        self.revenue_input = kwargs.get('revenue_input', 'annual_revenue')
        self.cost_input = kwargs.get('cost_input', 'annual_cost')

    def assess_business_model(self, datarow):
        if datarow[self.revenue_input] * self.revenue_over_cost_factor > datarow[self.cost_input]:
            return True
        else:
            return False

    def run(self, data, params):
        explore_business_model = data.apply(lambda row: self.assess_business_model(row), axis=1)
        return explore_business_model