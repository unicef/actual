

class RevenueNode:

    def __init__(self, name,
                       conn_params,
                       subscription_conversion_default,
                       fraction_community_using_school_internet,
                       income_per_household,
                       fraction_income_for_communications,
                       **kwargs
                       ):
        self.name = name
        self.conn_params = conn_params
        self.conn_types = set(conn_params['Type'])
        self.subscription_conversion_default = subscription_conversion_default
        self.fraction_community_using_school_internet = fraction_community_using_school_internet
        self.income_per_household = income_per_household
        self.fraction_income_for_communications = fraction_income_for_communications
        # optional params
        self.households_input = kwargs.get('households_input', 'nearby_households')
        self.coverage_input = kwargs.get('coverage_input', 'Type of Cell Coverage')
        self.coverage_4g_input = kwargs.get('coverage_4g_input', '4G')
        self.coverage_3g_input = kwargs.get('coverage_3g_input', '3G')
        self.coverage_2g_input = kwargs.get('coverage_2g_input', '2G')

    def estiamte_conversion(self, coverage):
        if coverage in self.conn_types:
            return float(self.conn_params[self.conn_params['Type'] == coverage]['Subscription Conversion Rate'])
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