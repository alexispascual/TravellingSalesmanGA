import math

def calculateDistance(point_a, point_b):

	'''
		Calculate distance between two points for the fitness cost

		Arguments:
			point_a: point A
			point_b: point B

		Returns:
			Euclidian distance between the two points

	'''

	euclidian_distance = math.sqrt((point_a[0] - point_b[0])**2 + (point_a[0] - point_b[0])**2)

	return euclidian_distance


def calculateFitnestCost(initial_locations, path):

	'''
		Calculates the fitness cost of each of the paths in the population

		Arguments:
			initial_locations: The locations where the salesman have to travel
			path: The path that the salesman would have to traverse

		Returns:
			Total distance of the whole traverse

	'''

	total_distance = 0

	for index in range(len(path) - 1):
		traverse_distance = calculateDistance(initial_locations[path[index]], initial_locations[path[index + 1]])
		total_distance += traverse_distance 

	return total_distance

