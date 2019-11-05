import random
import numpy as np

def initializeSpace(min_range, max_range, num_locations):

	'''
		Initializes the points to be travelled by the salesman between [min_range, max_range] along the x and y axis. It's all random.

		Arguments:
			min_range: minimum range
			max_range: maximum range
			num_locations: number of locations the salesman has to travel

		Returns:
			list of (x, y) pairs as the locations where the salesman have to travel

	'''
	locations = {}
	while(len(locations) != num_locations):
		locations = set([(random.randint(min_range, max_range), random.randint(min_range, max_range)) for _ in range(1, num_locations + 1)])
	
	return list(locations)


def initializeScores(min_score, max_score, num_locations):
	'''
	'''

	scores = []

	while (len(scores) != num_locations):
		scores = [random.randint(min_score, max_score) for _ in range(num_locations)]
	
	return scores

def generatePopulation(num_locations, population_size):

	'''
		Generates random paths around the locations

		Arguments:
			num_locations: number of locations the salesman has to travel
			population_size: number of random paths to be generated

		Returns:
			2-D list with dimension {population_size x num_locations} where each element is a path for which the salesman would traverse
			e.g. [12, 2 ,3 , 8, ...] -> The salesman would start at point 12, go to point 3, then 8, etc.

	'''

	population = []

	while (len(population)) < population_size:

		population.append(list(np.random.permutation(num_locations)))

	return population