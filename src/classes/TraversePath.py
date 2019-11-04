import random

class TraversePath(object):

	def __init__(self, num_locations):

		self.fitness_cost = 0
		self.traverse_path = self.generateRandomPath(num_locations)

	@staticmethod
	def generateRandomPath(num_locations):

		traverse_path = []
		point = random.randint(0, num_locations)

		if point not in traverse_path:
			traverse_path.append(point)
		else:
			return traverse_path

	@staticmethod
	def calculateCost(locations, scores):

		for index, waypoint in enumerate(self.traverse_path):
			
			traverse_score += scores[index]

			if index == (len(traverse_path) - 1):
				break;

			traverse_distance += calculateDistance(locations[waypoint], locations[index + 1])
			
		self.fitness_cost = traverse_distance + traverse_score
			

	@staticmethod
	def calculateDistance(point_a, point_b):

		euclidian_distance = math.sqrt((point_a[0] - point_b[0])**2 + (point_a[0] - point_b[0])**2)

		return euclidian_distance

	@staticmethod
	def mutateSelf(parent):
		