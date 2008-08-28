#!/usr/bin/python 
import worlds
from worlds import sdlconst,soya
import soya.widget as widget
import soya.cube
import soya.sdlconst as sdlconst
import math,random

worlds.init()

black = soya.Material()
black.shininess = 128  # 0 - plastic , 128 - metallic
black.diffuse   = (0.0, 0.0, 0.0, 1.0) #rgba 
black.specular  = (0.8, 0.95, 1.0, 1.0)

glass_sharp = soya.Material()
glass_sharp.shininess = 32  # 0 - plastic , 128 - metallic
glass_sharp.diffuse   = (0.5, 0.1, 0.0, 1.0) #rgba 
glass_sharp.specular  = (1.0, 0.0, 0.0, 1.0)
glass_sharp.additive_blending = True
#lass_sharp.separate_specular = 1 # brighter specular

glass_board = soya.Material()
glass_board.shininess = 32  # 0 - plastic , 128 - metallic
glass_board.diffuse   = (0.1, 0.15, 0.4, 1.0) #rgba 
glass_board.specular  = (0.0, 0.0, 0.0, 0.0)
glass_board.additive_blending = True
glass_board.separate_specular = 1 # brighter specular

glass_board2 = soya.Material()
glass_board2.shininess = 64  # 0 - plastic , 128 - metallic
glass_board2.diffuse   = (0.2, 0.3, 0.6, 1.0) #rgba 
glass_board2.specular  = (0.2, 0.7, 1.0, 1.0)
#glass_board2.separate_specular = 1 # brighter specular

sharp_world = soya.World(None)

# vertical (y)
worlds.Box(0.125,.5,0.125,None,glass_sharp, sharp_world,1, (-0.17,.45,-0.17))
worlds.Box(0.125,.5,0.125,None,glass_sharp, sharp_world,1, (-0.17,.45, 0.17))
worlds.Box(0.125,.5,0.125,None,glass_sharp, sharp_world,1, ( 0.17,.45,-0.17))
worlds.Box(0.125,.5,0.125,None,glass_sharp, sharp_world,1, ( 0.17,.45, 0.17))

# horizontal (x)
worlds.Box(0.95,0.125,0.125,None,glass_sharp, sharp_world,1, (0,1.3-0.37-0.5,-0.17))
worlds.Box(0.95,0.125,0.125,None,glass_sharp, sharp_world,1, (0,1.3-0.37-0.5, 0.17))

# horizontal (z)
worlds.Box(0.125,0.125,0.95,None,glass_sharp, sharp_world,1, (-0.17,1.3-0.37-0.5,0))
worlds.Box(0.125,0.125,0.95,None,glass_sharp, sharp_world,1, ( 0.17,1.3-0.37-0.5,0))

#worlds.Box(1.0,1.4,1.0,None,glass_board, sharp_world,1, (0,0.7,0))
worlds.Box(1,0.1,1,None,black, sharp_world,1, (0,0.1,0))

mesh_sharp = sharp_world.to_model()

mesh_board_cell = worlds.Box(1,0.1,1,None,glass_board).to_model()
mesh_board_cell2 = worlds.Box(1,0.1,1,None,glass_board2).to_model()

#mesh_board_cell = soya.cube.Cube(None).to_model()
light = soya.Light(worlds.scene)
light.directional = 1
light.rotate_x(120)
light.rotate_y(120)


board=[]
for x in range(11):
	row=[]
	for y in range(11):
		if (x+y)%2==0:
			board_cell = worlds.Body(mesh_board_cell)
		else:
			board_cell = worlds.Body(mesh_board_cell2)
		board_cell.x=x
		board_cell.z=y
		row.append(board_cell)

	board.append(row)
	
for i in range(11*11/3):
	x = random.randrange(11)
	y = random.randrange(11)
	sharp = worlds.Body(mesh_sharp)
	sharp.x = x
	sharp.z = y
	
	
worlds.camera.fov = 40
frame = 0

def mainloop():
	pass

def renderloop(proportion):
	global frame
	frame += proportion
	worlds.camera.set_xyz(5+math.sin(frame/100.0)*2,12,16)
	worlds.camera.look_at(board[5][6])
	
	


worlds.begin_loop(mainloop, renderloop)
