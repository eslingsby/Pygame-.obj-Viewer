class scene_class():
	def __init__(self, screen_width, screen_height, zoom, objects = []):
		self.zoom = zoom
		self.shift = (screen_width / 2, screen_height / 2)
		self.objects = objects
	
	def addChild(self, object):
		self.objects.append(object)
		
	def get_wireframe(self):
		wireframe = []

		for obj in self.objects:
			obj.update()

			vertices = []
			for vertex in obj.get_vertices():
				x = vertex[0]
				y = vertex[1]
				z = vertex[2]
				vertices.append((int(x / z * self.zoom + self.shift[0]), int(y / z  * self.zoom + self.shift[1]), z))

			for face in obj.get_faces():
				if len(face) == 3:
					for i in range(3):
						i2 = (i + 1) % 3
						struc = (vertices[face[i] - 1], vertices[face[i2] - 1])
						struc_rev = (vertices[face[i2] - 1], vertices[face[i] - 1])

						if struc[0][2] > 0 and struc[1][2] > 0:
							if (struc not in wireframe) and (struc_rev not in wireframe):
								wireframe.append((struc[0], struc[1]))

				elif len(face) == 4:
					for i in range(4):
						i2 = (i + 1) % 4
						struc = (vertices[face[i] - 1], vertices[face[i2] - 1])
						struc_rev = (vertices[face[i2] - 1], vertices[face[i] - 1])

						if struc[0][2] > 0 and struc[1][2] > 0:
							if (struc not in wireframe) and (struc_rev not in wireframe):
								wireframe.append((struc[0], struc[1]))

		return wireframe