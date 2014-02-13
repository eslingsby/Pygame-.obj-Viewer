import re
import math

class object_class():
	def __init__(self, filename, pos = [0, 0, 0], pan = [0, 0, 0]):
		self.set_pos(pos)
		self.set_pan(pan)

		self.f = open(filename)
		self.convert_obj()
		self.f.close()

	def convert_obj(self):
		self.raw_vertices = []
		self.faces = []

		for line in self.f:
			match_f4 = re.match("f ([^ ]+) ([^ ]+) ([^ ]+) ([^ ]+)\n", line)
			match_f3 = re.match("f ([^ ]+) ([^ ]+) ([^ ]+)\n", line)

			if match_f4 == None and match_f3 != None:
				self.faces.append((int(match_f3.group(1)), int(match_f3.group(2)), int(match_f3.group(3))))
			elif match_f4 != None:
				self.faces.append((int(match_f4.group(1)), int(match_f4.group(2)), int(match_f4.group(3)), int(match_f4.group(4))))

			match_v = re.match("v ([^ ]+) ([^ ]+) ([^ ]+)\n", line)

			if match_v != None:
				self.raw_vertices.append((float(match_v.group(1)) * (-1), float(match_v.group(2)) * (-1), float(match_v.group(3)) * (-1)))

	def update(self):
		self.vertices = []
		for vertex in self.raw_vertices[:]:
			self.vertices.append(vertex[:])

		self.transform()
		
	def transform(self):
		n = 0
		for vertex in self.vertices:
			x = vertex[0]
			y = vertex[1]
			z = vertex[2]

			# Pan around Z
			screen_x = x * math.cos(self.pan[2]) - y * math.sin(self.pan[2])
			screen_y = x * math.sin(self.pan[2]) + y * math.cos(self.pan[2])
			screen_z = z
			x, y, z = screen_x, screen_y, screen_z

			# Pan around Y (-90 skew)
			screen_x = x * math.cos(self.pan[1] - math.radians(180)) - z * math.sin(self.pan[1] - math.radians(180))
			screen_y = y
			screen_z = x * math.sin(self.pan[1] - math.radians(180)) + z * math.cos(self.pan[1] - math.radians(180))
			x, y, z = screen_x, screen_y, screen_z

			# Pan around X (+90 skew)
			screen_x = x
			screen_y = y * math.sin(self.pan[0] + math.radians(90)) + z * math.cos(self.pan[0] + math.radians(90))
			screen_z = y * math.cos(self.pan[0] + math.radians(90)) - z * math.sin(self.pan[0] + math.radians(90))
			x, y, z = screen_x, screen_y, screen_z

			x += self.pos[0]
			y += self.pos[1]
			z += self.pos[2]

			self.vertices[n] = (x, y, z)
			n += 1

	def set_pan(self, pan):
		self.pan = []
		for each in pan:
			self.pan.append(math.radians(each))

	def set_pos(self, pos):
		self.pos = pos

	def get_vertices(self):
		return self.vertices

	def get_faces(self):
		return self.faces