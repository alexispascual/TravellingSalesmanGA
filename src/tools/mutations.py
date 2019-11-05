import random
import math

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


