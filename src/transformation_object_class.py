from object_class import *

import re
import math

class transformation_object_class(object_class):
	def __init__(self, filename, transformation_filename, pos = [0, 0, 0], pan = [0, 0, 0]):
		object_class.__init__(self, filename, pos, pan)
		
		self.f = open(transformation_filename)
		self.convert_transformation_data()
		self.f.close()

	def convert_transformation_data(self):
		self.transformation_vertices = []
		self.transformation_trig_data = []
		self.transformations = []

		for line in self.f:
			split = re.split(" ", line)
			if len(split) >= 4: 
				self.transformations.append(0)

				if split[-1][-1] == "\n":
					split[-1] = split[-1][:-1]

				transformation_vertices = []
				for vertex in split[3:]:
					transformation_vertices.append(int(vertex))

				transformation_trig_data = (split[0], split[1], float(split[2]))

				self.transformation_vertices.append(tuple(transformation_vertices))
				self.transformation_trig_data.append(transformation_trig_data)

	def update(self):
		self.vertices = []
		for vertex in self.raw_vertices[:]:
			self.vertices.append(vertex[:])

		self.transform()
		object_class.transform(self)

	def transform(self):
		n = 0
		for opcode in self.transformation_trig_data:
			for vertex in self.transformation_vertices[n]:
				if opcode[1] == "s":
					self.vertices[vertex - 1] = (self.vertices[vertex - 1][0], self.vertices[vertex - 1][1] + math.sin(self.transformations[n]) * opcode[2], self.vertices[vertex - 1][2])
				elif opcode[1] == "-s":
					self.vertices[vertex - 1] = (self.vertices[vertex - 1][0], self.vertices[vertex - 1][1] - math.sin(self.transformations[n]) * opcode[2], self.vertices[vertex - 1][2])
				elif opcode[1] == "c":
					self.vertices[vertex - 1] = (self.vertices[vertex - 1][0], self.vertices[vertex - 1][1] + (math.cos(self.transformations[n]) - .5) * opcode[2], self.vertices[vertex - 1][2])
				elif opcode[1] == "-c":
					self.vertices[vertex - 1] = (self.vertices[vertex - 1][0], self.vertices[vertex - 1][1] - (math.cos(self.transformations[n]) - .5) * opcode[2], self.vertices[vertex - 1][2])
			n += 1

	def set_transformations(self, labels, change):
		n = 0
		for label in labels:
			i = 0
			for opcode in self.transformation_trig_data:
				if opcode[0] == label:
					self.transformations[i] += math.radians(change[n])
				i += 1
			n += 1