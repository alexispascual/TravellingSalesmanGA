#Generic GA Solving the Travelling Salesman Problem

import numpy as np
import random
import math
import matplotlib.pyplot as plt
import yaml
import os
import sys

from itertools import permutations
from pprint import pprint as pp

from tools.cost import calculateFitnestCost, calculateDistance
from tools.initializers import initializeSpace, generatePopulation
from tools.mutations import mutateGenomes, getInheritanceFactor
from tools.plot import plotFigure

if __name__ == "__main__":

	# Load config file
	config_file = "../config/config_travellingSalesman.yaml"
	if not os.path.exists(config_file):
		print("Config file does not exist. Make sure ../config/config_travellingSalesman.yaml exists or that you are in /src.")
		sys.exit(1)

	with open(config_file, 'r') as f:
		args = yaml.safe_load(f)

	# Initialize variables
	convergence = False
	generation = 0
	fitness_cost = []
	population = []

	# Randomize rnitial locations
	initial_locations = initializeSpace(args['min_range'], args['max_range'], args['num_locations'])

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







