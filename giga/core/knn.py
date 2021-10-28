from grispy import GriSPy


DEGREES_PER_10KM = 0.0089 # Degrees per 10 km
DEFAULT_NEIGHBOR_RADIUS = 10.0 # km


class NearestNeighborsNode:

	def __init__(self, name, pts, **kwargs):
		self.name = name
		self.index = GriSPy(pts)
		# optional position keys
		self.pt_keys = kwargs.get('pt_keys', ['Lat', 'Lon'])
		self.dim = len(self.pt_keys)

	def reindex(self, pts):
		self.index = GriSPy(pts)

	def num_nearest_neighbors(self, datarow, radius):
		pt = datarow[self.pt_keys]
		pt = pt.to_numpy(dtype=float).reshape(1, self.dim)
		dists, idxs = self.index.bubble_neighbors(pt, distance_upper_bound=radius, sorted=True)
		return len(dists[0])

	def run(self, data, parameters):
		radius = parameters.get('radius_knn', DEFAULT_NEIGHBOR_RADIUS * DEGREES_PER_10KM)
		n_nearest = data.apply(lambda row: self.num_nearest_neighbors(row, radius), axis=1)
		return n_nearest

