

COVERAGE_4G = '4G'
COVERAGE_3G = '3G'
COVERAGE_2G = '2G'

REQUIRED_ARGUMENTS = ('speed_4g', 'speed_3g', 'speed_2g')
OPTIONAL_ARGUMENTS = {'fiber_range': 10.0, # km
                      'wisp_range': 5.0, # km
                      'bandwidth_input': 'bandwidth',
                      'cell_coverage_input': 'Type of Cell Coverage',
                      'fiber_input': 'Distance to Nearest Fiber',
                      'output_4g': '4G',
                      'output_3g': '3G',
                      'output_2g': '2G',
                      'output_wisp': 'WISP',
                      'output_fiber': 'Fiber',
                      'output_satellite': 'Satellite'}


class TechnologyNode:

    def __init__(self, name, **kwargs):
        self.name = name
        assert all([k in kwargs for k in REQUIRED_ARGUMENTS]), f"Missing one or more required arguments {REQUIRED_ARGUMENTS}"
        for attr in REQUIRED_ARGUMENTS:
            setattr(self, attr, kwargs.get(attr))
        for attr in OPTIONAL_ARGUMENTS.keys():
            setattr(self, attr, kwargs.get(attr, OPTIONAL_ARGUMENTS[attr]))

    def valid_coverage(self, data, speed, coverage):
        if (data[self.bandwidth_input] < speed) and (data[self.cell_coverage_input] == coverage):
            return True
        else:
            return False

    def valid_fiber(self, data):
        if (data[self.fiber_input] < self.fiber_range):
            return True
        else:
            return False

    def valid_wisp(self, data):
        if (data[self.fiber_input] >= self.fiber_range) and (data[self.fiber_input] < (self.fiber_range + self.wisp_range)):
            return True
        else:
            return False

    def determine_tech(self, datarow):
        if self.valid_fiber(datarow):
            return self.output_fiber
        elif self.valid_coverage(datarow, self.speed_4g, COVERAGE_4G):
            return self.output_4g
        elif self.valid_wisp(datarow):
            return self.output_wisp
        elif self.valid_coverage(datarow, self.speed_2g, COVERAGE_2G):
            return self.output_2g
        elif self.valid_coverage(datarow, self.speed_3g, COVERAGE_3G):
            return self.output_3g
        else:
            return self.output_satellite

    def run(self, data, params):
        tech = data.apply(lambda row: self.determine_tech(row), axis=1)
        return tech