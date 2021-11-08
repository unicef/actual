

REQUIRED_ARGUMENTS = ('revenue_over_cost_factor',)
OPTIONAL_ARGUMENTS = {'revenue_input': 'annual_revenue',
                      'cost_input': 'annual_cost'}


class BusinessModelNode:

    def __init__(self, name, **kwargs):
        self.name = name
        assert all([k in kwargs for k in REQUIRED_ARGUMENTS]), f"Missing one or more required arguments {REQUIRED_ARGUMENTS}"
        for attr in REQUIRED_ARGUMENTS:
            setattr(self, attr, kwargs.get(attr))
        for attr in OPTIONAL_ARGUMENTS.keys():
            setattr(self, attr, kwargs.get(attr, OPTIONAL_ARGUMENTS[attr]))

    def assess_business_model(self, datarow):
        if datarow[self.revenue_input] * self.revenue_over_cost_factor > datarow[self.cost_input]:
            return True
        else:
            return False

    def run(self, data, params):
        explore_business_model = data.apply(lambda row: self.assess_business_model(row), axis=1)
        return explore_business_model