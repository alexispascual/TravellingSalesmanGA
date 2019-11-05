import random
import math
from pprint import pprint as pp
class TraversePath(object):

	locations = []
	scores = []
	
	def __init__(self, num_locations):

		self.fitness_cost_distance = 0
		self.fitness_cost_score = 0
		self.traverse_path = self.generateRandomPath(num_locations)
	
	def calculateDistanceCost(self):

		total_traverse_distance = 0

		for index in range(len(self.traverse_path) - 1):
			traverse_distance = self.calculateDistance(self.locations[self.traverse_path[index]], self.locations[self.traverse_path[index + 1]])
			total_traverse_distance += traverse_distance 
			
		self.fitness_cost_distance = total_traverse_distance

	def calculateScoresCost(self):

		total_traverse_score = 0

		for waypoint in self.traverse_path:
			total_traverse_score += self.scores[waypoint]
			
		self.fitness_cost_score = total_traverse_score
	
	def generateRandomPath(self, num_locations):

		traverse_path = []
		chances = 0

		while len(traverse_path) < num_locations:

			point = random.randint(0, num_locations - 1)

			if point not in traverse_path:
				traverse_path.append(point)
			else:
				chances += 1

			if chances == 3:
				break;

		return traverse_path
	
	@classmethod
	def assignLocationAndScores(self, locations, scores):
		self.locations = locations
		self.scores = scores

	@staticmethod
	def calculateDistance(point_a, point_b):

		euclidian_distance = math.sqrt((point_a[0] - point_b[0])**2 + (point_a[0] - point_b[0])**2)

		return euclidian_distance

	# @staticmethod
	# def mutateSelf(parent):
		