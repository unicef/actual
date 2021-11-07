from grispy import GriSPy


DEGREES_PER_1KM = 0.0089 # Degrees per 1 km
DEFAULT_CONSOLIDATION_RADIUS = 0.01 # km


class ConsolidationNode:

    """
        Computational node that can be used to consolidate nearby data entries
        This is a filter that removes data that falls within a consolidation radius of 
            another data point in the input data set
        Consolidation radius is assumed to be in km
    """

    def __init__(self, name, **kwargs):
        self.name = name
        # optional position keys
        self.consolidation_radius = kwargs.get('consolidation_radius', DEFAULT_CONSOLIDATION_RADIUS)
        self.location_input = kwargs.get('location_input', ['Lat', 'Lon'])
        self.dim = len(self.location_input)

    def consolidate(self, data, radius):
        # consolidates data based on its location in self.location_input
        # returns a consolidated subset of data where data points with location within specified radius have been filtered out
        radius *= DEGREES_PER_1KM # trasnform to degrees
        identifiers = set()
        consolidated = []
        pts = data[self.location_input].to_numpy()
        index = GriSPy(pts)
        for i, datarow in data.iterrows():
            pt = datarow[self.location_input]
            pt = pt.to_numpy(dtype=float).reshape(1, self.dim)
            dists, idxs = index.bubble_neighbors(pt, distance_upper_bound=radius, sorted=True)
            idxs = idxs[0]
            if i in identifiers:
                consolidated.append(False)
            else:
                consolidated.append(True)
                for ii in idxs[1:]:
                    identifiers.add(ii)
        return consolidated

    def run(self, data, parameters):
        radius = parameters.get('consolidation_radius', self.consolidation_radius)
        consolidated = self.consolidate(data, radius)
        return consolidated

