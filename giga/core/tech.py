COVERAGE_4G = '4G'
COVERAGE_3G = '3G'
COVERAGE_2G = '2G'

DEFAULT_FIBER_RANGE = 10 # km
DEFAULT_WISP_RANGE = 5 # km


class TechnologyNode:

    def __init__(self,
                 name,
                 speed_4g,
                 speed_3g,
                 speed_2g,
                 **kwargs):
        self.name = name
        self.speed_4g = speed_4g
        self.speed_3g = speed_3g
        self.speed_2g = speed_2g

        # optional
        self.fiber_range = kwargs.get('fiber_range', DEFAULT_FIBER_RANGE)
        self.wisp_range = kwargs.get('wisp_range', DEFAULT_WISP_RANGE)
        self.bandwidth_input = kwargs.get('bandwidth_input', 'bandwidth')
        self.cell_coverage_input = kwargs.get('cell_coverage_input', 'Type of Cell Coverage')
        self.fiber_input = kwargs.get('fiber_input', 'Distance to Nearest Fiber')
        self.output_4g = kwargs.get('output_4g', 'cell4G')
        self.output_3g = kwargs.get('output_3g', 'cell3G')
        self.output_2g = kwargs.get('output_2g', 'cell2G')
        self.output_fiber = kwargs.get('output_fiber', 'WISP')
        self.output_sattelite = kwargs.get('output_satellite', 'satellite')

    def valid_coverage(self, data, speed, coverage):
        if (data[self.bandwidth_input] < speed) and (data[self.cell_coverage_input] == coverage):
            return True
        else:
            return False

    def valid_fiber(self, data):
        if (data[self.fiber_input] >= self.fiber_range) and (data[self.fiber_input] < (self.fiber_range + self.wisp_range)):
            return True
        else:
            return False

    def determine_tech(self, datarow):
        if self.valid_coverage(datarow, self.speed_4g, COVERAGE_4G):
            return self.output_4g
        elif self.valid_fiber(datarow):
            return self.output_fiber
        elif self.valid_coverage(datarow, self.speed_2g, COVERAGE_2G):
            return self.output_2g
        elif self.valid_coverage(datarow, self.speed_3g, COVERAGE_3G):
            return self.output_3g
        else:
            return self.output_sattelite

    def run(self, data, params):
        tech = data.apply(lambda row: self.determine_tech(row), axis=1)
        return tech