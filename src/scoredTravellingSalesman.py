#Generic GA Solving the Travelling Salesman Problem

import numpy as np
import random
import math
import matplotlib.pyplot as plt
import yaml
import os

from classes.TraversePath import TraversePath

from itertools import permutations
from pprint import pprint as pp

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
		locations = set([(random.randint(min_range, max_range), random.randint(min_range, max_range)) for _ in range(num_locations)])
	
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

		population.append(TraversePath(num_locations))
		
	return population

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

def mutateGenomes(fittest_genomes, population, mutated_subset_percentage, generation):

	'''
		Mutates the genomes of the top fittest genomes (paths with the shortest distances)

		Essentially gets the first few waypoints of the traverse of the shortest paths, and then randomizes the rest of the waypoints to complete the whole path. 

		Arguments:
			fittest_genomes: Top fittest genomes
			population: list of all the paths
			mutated_subset_percentage: percentage of the fittest genomes to mutate
			generation: number of GA iterations 

		Returns:
			List of the mutated genomes, or the modified paths from the parent

	'''

	child = []
	mutated_genome_subset = []
	inheritance_factor = 1
	
	while(len(mutated_genome_subset) < int(len(population) * mutated_subset_percentage)):

		child = []

		parent = fittest_genomes[random.randint(0, len(fittest_genomes) - 1)]

		inherited_genome_length = math.floor((len(parent))/2)

		inheritance_factor = getInheritanceFactor("random", generation, parent)

		child[0:inheritance_factor] = parent[0:inheritance_factor]

		while (len(child) != len(parent)):
			chromosome = random.randint(0, math.floor(len(parent) -1))

			if chromosome not in child:
				child.append(chromosome)


		assert(len(set(child)) == len(parent))

		mutated_genome_subset.append(child)

	return mutated_genome_subset

def getInheritanceFactor(mode, generation, parent):

	'''
		Randomizes how many genes to copy from the parent to the child, or how many initial waypoints to copy from the parent to the child

		Arguments:
			mode: For now, can be "random" or "generational" 
					random: random number of genes to copy. 
					generational: increase number of genes to copy as generation number increases
			generation: number of GA iterations
			parent: parent gene to copy from

		Returns:
			How many genes to copy

	'''

	if mode == "random":
		inheritance_factor = random.randint(math.floor(len(parent)/4), math.floor(len(parent)/2))

	if mode == "generational":
		inheritance_factor = math.floor(generation/100)

	return inheritance_factor



def plotFigure(path, initial_locations, generation, fitness_cost):

	'''
		Plots the figures of the initial points, as well as the path of the salesman

		Arguments:
			path: Path to plot
			initial_locations: The locations where the salesman have to travel
			generation: number of GA iterations
			fitness_cost: Fitness cost of the current path

		Returns:
			PNG image of the figure

	'''

	if (generation == 0):

		fig, ax = plt.subplots()
		for location in initial_locations: 
			ax.scatter(location[0], location[1])

		ax.set_title("Original Points")
		ax.set_xlabel('x')
		ax.set_ylabel('y')

	else:

		fig, ax = plt.subplots(1, 2, figsize=(16, 6)) 
		for i in range(0, len(path) -1):

			x1 = initial_locations[path[i]][0]
			x2 = initial_locations[path[i + 1]][0]
			y1 = initial_locations[path[i]][1]
			y2 = initial_locations[path[i + 1]][1]

			ax[1].plot([x1, x2], [y1, y2])
			ax[1].annotate(i, (x1, y1))

			ax[0].scatter(x1, y1)
			
		ax[0].set_title("Original Points")
		ax[0].set_xlabel('x')
		ax[0].set_ylabel('y')

		ax[1].annotate(len(path) -1, (x2, y2))
		ax[1].set_title("Order of traverse for Generation {} \n Cost: {}".format(generation, fitness_cost))
		ax[1].set_xlabel('x')
		ax[1].set_ylabel('y')

	save_path = os.path.join(".", "plots")

	if not (os.path.isdir(save_path)):
		print("Creating save directory in ../plots/")
		os.mkdir(save_path)

	full_save_path = os.path.join(save_path, "Generation {}.png".format(generation))

	plt.savefig(full_save_path)
	plt.close()

if __name__ == "__main__":

	# Load config file
	config_file = "./config/config_scoredTravellingSalesman.yaml"

	with open(config_file, 'r') as f:
		args = yaml.safe_load(f)

	# Initialize variables
	convergence = False
	generation = 0
	fitness_cost = []
	population = []

	# Randomize initial locations and scores
	initial_locations = initializeSpace(args['min_range'], args['max_range'], args['num_locations'])
    initial_scores = initializeScores(args['min_score'], args['max_score'], args['num_locations'])

	# Initialize random paths
	population = generatePopulation(args['num_locations'], args['num_population'])

	# Plot original points
	plotFigure("", initial_locations, 0, "")

	# Loop while convergence is not met
	# TODO: Define convergence
	while not convergence:

		#Initialize variables
		next_generation = []
		fittest_genomes = []
		mutated_genomes = []
		random_genomes = []
		fitness_cost = []

		# Calculate fitness cost of each of the path in the population
		for path in population:
			fitness_cost.append(calculateFitnestCost(initial_locations, path))

		# Sort fitness cost from least to most
		fitness_cost, population = (list(t) for t in zip(*sorted(zip(fitness_cost, population))))

		# Plot graph every certain number of generations
		if generation % args['plot_generations'] == 0:

			print("Generation: {}, Fitness cost: {}".format(generation, fitness_cost[0]))
			print("Shortest path: {}".format(population[0]))
			plotFigure(population[0], initial_locations, generation, fitness_cost[0])

		# Get fittest genomes -> The paths with the least distance travelled
		fittest_genomes = population[:int(args['fittest_subset_percentage'] * args['num_population'])]

		# Mutate genomes -> Get initial paths from the shortest paths in the population
		mutated_genomes = mutateGenomes(fittest_genomes, population, args['mutated_subset_percentage'], generation)

		# Generate random genomes
		random_genomes = generatePopulation(args['num_locations'], args['num_population'] - (len(fittest_genomes) + len(mutated_genomes)))

		# Lump them all into the next generation
		next_generation.extend(fittest_genomes)
		next_generation.extend(mutated_genomes)
		next_generation.extend(random_genomes)

		# Run the GA again with the new generation as the population
		population = next_generation
		generation += 1

		# Convergence criteria
		if generation == args['convergence_generation']:
			convergence = True







