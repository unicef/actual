

class MultiplieNode:

	def __init__(self, value, data_key, **kwargs):
		self.value = value
		self.data_key = data_key

	def run(self, data, parameters):
		demand = data.apply(lambda row: row[self.frequency_key] * row[self.size_key], axis=1)
		return demand
