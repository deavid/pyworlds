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

white = soya.Material()
white.shininess = 1  # 0 - plastic , 128 - metallic
white.diffuse   = (0.9, 1.0, 0.9, 1.0) #rgba 
white.specular  = (1.0, 1.0, 1.0, 0.3)

energy = soya.Material()
energy.shininess = 1  # 0 - plastic , 128 - metallic
energy.diffuse   = (0.7, 1.0, 0.7, 0.2) #rgba 
energy.specular  = (0.0, 1.0, 0.0, 0.1)
energy.additive_blending = True

glass_sharp = soya.Material()
glass_sharp.shininess = 32  # 0 - plastic , 128 - metallic
glass_sharp.diffuse   = (0.5, 0.1, 0.0, 1.0) #rgba 
glass_sharp.specular  = (1.0, 0.0, 0.0, 1.0)
glass_sharp.additive_blending = True
#lass_sharp.separate_specular = 1 # brighter specular

glass_board = soya.Material()
glass_board.shininess = 32  # 0 - plastic , 128 - metallic
glass_board.diffuse   = (0.05, 0.10, 0.25, 1.0) #rgba 
glass_board.specular  = (0.0, 0.0, 0.0, 0.0)
glass_board.additive_blending = True
glass_board.separate_specular = 1 # brighter specular

glass_board2 = soya.Material()
glass_board2.shininess = 64  # 0 - plastic , 128 - metallic
glass_board2.diffuse   = (0.1, 0.15, 0.3, 1.0) #rgba 
glass_board2.specular  = (0.2, 0.7, 1.0, 1.0)
#glass_board2.separate_specular = 1 # brighter specular

point_world = soya.World(None)
worlds.Sphere(position=(0.02,.02,0.02), size=(.12,.08,.1), material=energy, quality=(8,8), insert_into=point_world)
worlds.Sphere(position=(0.02,.02,0.02), size=(.08,.08,.08), material=energy, quality=(6,6), insert_into=point_world)
worlds.Sphere(position=(0.02,.02,0.02), size=(.06,.06,.06), material=energy, quality=(3,3), insert_into=point_world)
mesh_point = point_world.to_model() 

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

mesh_board_cell = worlds.Box(.98,0.1,.98,None,glass_board).to_model()
mesh_board_cell2 = worlds.Box(.98,0.1,.98,None,glass_board2).to_model()

#mesh_board_cell = soya.cube.Cube(None).to_model()
light = soya.Light(worlds.scene)
light.directional = 1
light.rotate_x(120)
light.rotate_y(120)

points={}

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
		point = worlds.Body(mesh_point)
		point.x=x
		point.z=y
		point.y=.3
		point.rotation[0]=random.uniform(-5, 5)
		point.rotation[1]=random.uniform(-5, 5)
		point.rotation[2]=random.uniform(-5, 5)
		points[(x,y)]=point
		

	board.append(row)


sharps={}
while len(sharps)<11*11/4:
	x = random.randrange(11)
	y = random.randrange(11)
	if (x,y) not in sharps:
		sharp = worlds.Body(mesh_sharp)
		sharp.x = x
		sharp.z = y
		sharps[(x,y)]=sharp
		points[(x,y)].visible=False
		del points[(x,y)]
	
squisher = worlds.Character("echassien2@vert")
squisher.scale(.5,.5,.5)
squisher.x=2
squisher.z=2
	
sorcerer = worlds.Character("balazar")
sorcerer.scale(.6,.6,.6)

sorcerer.x=5
sorcerer.z=6

	
worlds.camera.fov = 60
frame = 0

def mainloop():
	global sorcerer
	walk=False
	
	if sdlconst.K_UP in worlds.KEY:			walk=True; sorcerer.desiredangle=270
	if sdlconst.K_DOWN in worlds.KEY:		walk=True; sorcerer.desiredangle=+90
	if sdlconst.K_LEFT in worlds.KEY:   walk=True; sorcerer.desiredangle=180
	if sdlconst.K_RIGHT in worlds.KEY:	walk=True; sorcerer.desiredangle=0
	anglewrong=abs(sorcerer.angle-sorcerer.desiredangle)
	if anglewrong>180: anglewrong-=360; anglewrong=abs(anglewrong)
	
	if walk and anglewrong<20: 
		
		sorcerer.character_setstate("walk")
		if sorcerer.velocity.z>-0.1: sorcerer.velocity.z-=0.02
	else:	
		sorcerer.character_setstate("stop")
		if sorcerer.velocity.z!=0: 
			sorcerer.velocity.z/=1.2
		
		
			
		
	
	pass

def renderloop(proportion):
	global frame,sorcerer,sharps
	frame += proportion
	worlds.camera.set_xyz(5+math.sin(frame/200.0)*2,12,16)
	worlds.camera.look_at(sorcerer)
	dist = worlds.camera.distance_to(sorcerer)
	dfov = 500/dist
	worlds.camera.fov = (worlds.camera.fov  * 10+ dfov) / 11.0
	
	


worlds.begin_loop(mainloop, renderloop)
