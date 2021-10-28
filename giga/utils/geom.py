import numpy as np


def points_in_circle(x_center, y_center, radius):
	"""
	Given center and radius of a circle,
	gives all integer points which lie inside or on the circle radius
	"""
	x_ = np.arange(x_center - radius, x_center + radius + 1, dtype=int)
	y_ = np.arange(y_center - radius, y_center + radius + 1, dtype=int)
	x, y = np.where((x_[:,np.newaxis] - x_center)**2 + (y_ - y_center)**2 <= radius**2)
	return x_[x], y_[y]