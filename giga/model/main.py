

class GigaNode:

	"""
		Computational Node that encapsulates the Giga model
	"""

	def __init__(self, ):
		# initalize graph
		# school bandwidth
		# community badnwidth
		# cost
		# initialize with loggers?
		pass

	def run(self, input, params):
		# pre process

		# compute bandwidths

		# sum bandwidths
		bw = self.bandwidths.sum()
		# asses technology
		techs = self.tech.run(bw)
		# asses costs
		costs = [self.cost(t) for t in techs]
		return costs # feasible tech costs?



