from grispy import GriSPy


DEGREES_PER_1KM = 0.0089 # Degrees per 1 km
DEFAULT_NEIGHBOR_RADIUS = 0.01 # km


class ConsolidationNode:

	def __init__(self, name, **kwargs):
		self.name = name
		# optional position keys
		self.pt_input = kwargs.get('pt_input', ['Lat', 'Lon'])
		self.dim = len(self.pt_input)

	def consolidate(self, data, radius):
		identifiers = set()
		consolidated = []
		pts = data[self.pt_input].to_numpy()
		index = GriSPy(pts)
		for i, datarow in data.iterrows():
			pt = datarow[self.pt_input]
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
		radius = parameters.get('radius_consolidate', DEFAULT_NEIGHBOR_RADIUS)
		radius *= DEGREES_PER_1KM
		consolidated = self.consolidate(data, radius)
		return consolidated

