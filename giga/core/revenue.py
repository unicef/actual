

REQUIRED_ARGUMENTS = ('connectivity_params', 'subscription_conversion_default', 'fraction_community_using_school_internet',
                      'income_per_household', 'fraction_income_for_communications')
OPTIONAL_ARGUMENTS = {'households_input': 'nearby_households',
                      'coverage_input': 'Type of Cell Coverage',
                      'coverage_4g_input': '4G',
                      'coverage_3g_input': '3G',
                      'coverage_2g_input': '2G'}


class RevenueNode:

    def __init__(self, name, **kwargs):
        self.name = name
        assert all([k in kwargs for k in REQUIRED_ARGUMENTS]), f"Missing one or more required arguments {REQUIRED_ARGUMENTS}"
        for attr in REQUIRED_ARGUMENTS:
            setattr(self, attr, kwargs.get(attr))
        for attr in OPTIONAL_ARGUMENTS.keys():
            setattr(self, attr, kwargs.get(attr, OPTIONAL_ARGUMENTS[attr]))
        self.conn_types = set(self.connectivity_params['Type'])

    def estiamte_conversion(self, coverage):
        if coverage in self.conn_types:
            return float(self.connectivity_params[self.connectivity_params['Type'] == coverage]['Subscription Conversion Rate'])
        else:
            return self.subscription_conversion_default

    def estimate_annual_revenue(self, datarow):
        subscribers = datarow[self.households_input] * self.fraction_community_using_school_internet
        conversion = self.estiamte_conversion(datarow[self.coverage_input])
        revenue = subscribers * conversion * self.income_per_household * self.fraction_income_for_communications
        return revenue

    def run(self, data, params):
        annual_revenue = data.apply(lambda row: self.estimate_annual_revenue(row), axis=1)
        return annual_revenue