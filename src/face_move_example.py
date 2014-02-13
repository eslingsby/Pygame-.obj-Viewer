from scene_class import *
from object_class import *
from transformation_object_class import *

import pygame, sys
from pygame.locals import *

screen_size = (1280, 720)
zoom = 500

main_scene = scene_class(screen_size[0], screen_size[1], zoom)

pygame.init()
screen = pygame.display.set_mode(screen_size, 0, 32)

#////////[ Load Start ]////////#
def change_range(OldMin, OldMax, NewMin, NewMax, OldValue):
	return (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin
	
face_1 = transformation_object_class("objects/face.obj", "objects/face_transformations.dat", pos = [1, 0, 5], pan = [0, 0, 0])
face_2 = transformation_object_class("objects/face.obj", "objects/face_transformations.dat", pos = [-1, 0, 5], pan = [0, 0, 0])

main_scene.addChild(face_1)
main_scene.addChild(face_2)

line_colour = (220, 220, 220)
text_colour = (255, 255, 255)
bg_colour = (20, 20, 20)
#////////[  Load End  ]////////#

instructions = pygame.image.load("instructions.png")

mouse_x, mouse_y = pygame.mouse.get_pos()
d_z = 0;
d_x = 0;
i = 0

while 1:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

		if event.type == pygame.KEYDOWN:
			if event.key == K_DOWN:
				d_z = +.1
		if event.type == pygame.KEYDOWN:
			if event.key == K_UP:
				d_z = -.1
		if event.type == pygame.KEYDOWN:
			if event.key == K_RIGHT:
				d_x = +.1
		if event.type == pygame.KEYDOWN:
			if event.key == K_LEFT:
				d_x = -.1
		
		if event.type == pygame.KEYUP:
			if event.key == K_DOWN:
				d_z = 0
		if event.type == pygame.KEYUP:
			if event.key == K_UP:
				d_z = 0
		if event.type == pygame.KEYUP:
			if event.key == K_RIGHT:
				d_x = 0
		if event.type == pygame.KEYUP:
			if event.key == K_LEFT:
				d_x = 0
		
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button  == 5:
				main_scene.zoom -= 10;
		if event.type == pygame.MOUSEBUTTONUP:
			if event.button  == 4:
				main_scene.zoom += 10;

	mouse_x, mouse_y = pygame.mouse.get_pos()

	screen.fill(bg_colour)
	
	#////////[ Update Start ]////////#
	face_1.pos[0] += d_x
	face_2.pos[0] += d_x
	face_1.pos[2] += d_z
	face_2.pos[2] += d_z
	face_2.set_transformations(("upper_eye", "lower_eye", "top_mouth", "bottom_mouth", "inner_brows", "outer_brows", "mouth_sides"), (i / 100, i / 100, i / 100, i / 100, i / 100, i / 100, i / 100))
	#face_1.set_transformations(("upper_eye", "lower_eye", "top_mouth", "bottom_mouth", "inner_brows", "outer_brows", "mouth_sides"), (i / 100, i / 100, i / 100, i / 100, i / 100, i / 100, i / 100))
	face_1.set_pan([i, i, 0])
	
	face_2.set_pan([change_range(0, screen_size[1], -100, 100, mouse_y), change_range(0, screen_size[0], -100, 100, mouse_x), 0])
	#////////[  Update End  ]////////#

	wireframe = main_scene.get_wireframe()
	
	for line in wireframe:
		pygame.draw.line(screen, line_colour, line[0][:2], line[1][:2])
	
	screen.blit(instructions, (10, 15))
	
	pygame.display.update()

	i += 1