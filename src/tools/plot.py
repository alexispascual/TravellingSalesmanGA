import matplotlib.pyplot as plt
import os

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


def plotPathLengthvsScore(population):

	fig, ax = plt.subplots(2, 1, figsize = (14, 10))

	for path in population:
		ax[0].scatter(len(path.traverse_path), path.fitness_cost_score)
		ax[1].scatter(path.fitness_cost_distance, path.fitness_cost_score)

	ax[0].set_title('Length of traverse vs Score')
	ax[0].set_xlabel('Length of Traverse')
	ax[0].set_ylabel('Score')

	ax[1].set_title('Distance vs Score')
	ax[1].set_xlabel('Distance')
	ax[1].set_ylabel('Score')

	save_path = os.path.join(".", "plots")

	if not (os.path.isdir(save_path)):
		print("Creating save directory in ../plots/")
		os.mkdir(save_path)

	full_save_path = os.path.join(save_path, "Traverse vs Score.png")

	plt.savefig(full_save_path)
	plt.close()



















