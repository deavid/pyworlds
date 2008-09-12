#!/usr/bin/python 

import sys,os
sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), '..', 'src')))

import math,random

import pyworlds.worlds as worlds
from pyworlds.worlds import sdlconst,soya
import soya.widget as widget
import soya.cube
import soya.sdlconst as sdlconst


class BoardMap():
	def __init__(self,rows,cols):
		self.rows=rows
		self.cols=cols
		
		self.boardmap=[]
		self.wallmap=[]
		for i in range(cols):
			self.boardmap.append([])
			self.wallmap.append([])
		
		for col in self.boardmap:
			for i in range(rows):
				col.append(None)
			
		for col in self.wallmap:
			for i in range(rows):
				col.append(None)
			
	def checkxy(self,x,y):
		if ( x < 0 or
			x >= self.cols or
			y < 0 or
			y >= self.rows ):
				return False
		return True

	def setxy(self,x,y,obj):
		if not self.checkxy(x,y): return False
		p_obj=self.getxy(x,y)
		if p_obj != None:
			try:
				p_obj.map_xy = None
			except:
				pass
			
		try:
			self.boardmap[x][y]=obj
			try: 
				obj.map_xy = (x,y)
			except:
				pass
		except:
			print	"BoardMap.setxy(%d,%d,obj): Error ocurred when trying to set x,y" % (x,y)

	def getxy(self,x,y):
		if not self.checkxy(x,y): return False
		try:
			return self.boardmap[x][y]
		except:
			print	"BoardMap.getxy(%d,%d): Error ocurred when trying to get x,y" % (x,y)
			return None

	def iswall(self,x,y):
		if not self.checkxy(x,y): return True
		p = self.getwall(x,y)
		if p == None: return False
		if p == "": return False
		if p == " ": return False
		return True
		
	def getwall(self,x,y):
		if not self.checkxy(x,y): return False
		try:
			return self.wallmap[x][y]
		except:
			print	"BoardMap.getwall(%d,%d): Error ocurred when trying to get x,y" % (x,y)
			return None

	def setwall(self,x,y,wall="#"):
		if not self.checkxy(x,y): return False
		try:
			self.wallmap[x][y]=wall
		except:
			print	"BoardMap.setwall(%d,%d,obj): Error ocurred when trying to set x,y" % (x,y)

	def unsetwall(self,x,y):
		if not self.checkxy(x,y): return False
		try:
			self.wallmap[x][y]=None
		except:
			print	"BoardMap.unsetwall(%d,%d,obj): Error ocurred when trying to set x,y" % (x,y)








class BoardCharacter(worlds.Character):
	""" This is a character that can move along in a board made of rectangles. """
	def __init__(self,filename,x,y,board,char=None):
		worlds.Character.__init__(self,filename)
		self.points=0
		self.x=x
		self.z=y
		self.desired_x=x
		self.desired_z=y
		self.map_xy = None
		self.boardmap = board
		self.boardmap.setxy(x,y,self)
		self.boardmap.setwall(x,y,char)
		self.map_char=char
		
		
	def begin_round(self):
		worlds.Character.begin_round(self)		
		self.distance=self.dist_to_walk()
			
		if self.distance>0.2:
			anglewrong=abs(self.angle-self.desiredangle)
			if anglewrong>180: 
				anglewrong-=360; 
				anglewrong=abs(anglewrong)
			
			if anglewrong<45: 
				self.character_setstate("walk")
				#if anglewrong<20: anglewrong = 20.0
				self.velocity.z =-3
				self.character_updateangle()
		else:
			if self.velocity.z!=0:
				self.character_setstate("stop")
				self.velocity.z =0
			
	def advance_time(self, proportion):
		worlds.Character.advance_time(self, proportion)
		if self.distance<0.2 :
			self.x=(self.x*1+self.desired_x*proportion)/(1.0+proportion)
			self.z=(self.z*1+self.desired_z*proportion)/(1.0+proportion)
		
	def is_inplace(self):
		if self.map_xy != None:
			mx,my= self.map_xy
			if (round(mx,1) != round(self.desired_x,1)
				or round(my,1) != round(self.desired_z,1)):
				return False
				
		if ( abs(self.desired_x-self.x)<0.7 and
				 abs(self.desired_z-self.z)<0.7 ):
			return True
		else:
			return False
		
	def update_mapxy(self):
		dx = self.desired_x
		dy = self.desired_z
		if self.map_xy!=None: 
			mx,my= self.map_xy
			self.boardmap.setxy(mx,my,None)
			self.boardmap.unsetwall(mx,my)
			replaced_obj=self.boardmap.getxy(dx,dy)
			if replaced_obj!=None:
				try:
					replaced_obj.deleted_by(self)
				except:
					pass
		
		self.boardmap.setxy(dx,dy,self)
		self.boardmap.setwall(dx,dy,self.map_char)
		
		return True
		
					

	def character_move(self,dx,dy):
		if not self.boardmap.iswall(self.desired_x+dx,
		self.desired_z+dy) :
			self.desired_x+=dx
			self.desired_z+=dy
			self.update_mapxy()
			self.character_updateangle()
			self.distance=self.dist_to_walk()
			return True
		return False
	
	def character_updateangle(self):
		dx=self.desired_x-self.x
		dy=self.desired_z-self.z
		self.desiredangle=worlds.xy_toangle(dx,dy)
			
	def dist_to_walk(self):
		dx=self.desired_x-self.x
		dy=self.desired_z-self.z
		return math.sqrt(dx*dx+dy*dy)			
		
		
class BoardPoint(BoardCharacter):
	def deleted_by(self,origin):
		origin.points += 10
		self.deleted=True

	def __init__(self,filename,x,y,board):
		BoardCharacter.__init__(self,filename,x,y,board)
		self.deleted=False
		
	def advance_time(self, proportion):
		worlds.Character.advance_time(self, proportion)
		elapsed = worlds.mainloop.round_duration * proportion
		if elapsed==0: elapsed=0.001
		
		if self.deleted:
			self.velocity.y+=10*elapsed
		

class GameTurn():
	def __init__(self):
		self.objlist=[]
		self.nturns=0
		self.curturn=0
		self.movingturn=False
	
	def addBody(self,Body):
		self.objlist.append(Body)
	
	def beginMove(self):
		self.movingturn=True
	
	def checkEndMove(self):
		if self.movingturn:
			body=self.inTurn(False)
			if body.is_inplace():
				self.movingturn=False
				self.nextTurn()
	
	def nextTurn(self):
		self.curturn+=1
		while self.curturn >= len(self.objlist):
			self.curturn-=len(self.objlist)
			self.nturns+=1
		
	def inTurn(self,allowNone=True):
		if allowNone and self.movingturn: return None
		return self.objlist[self.curturn]

	
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
worlds.Sphere(position=(0.02,.0,0.02), size=(.12,.08,.1), material=energy, quality=(4,4), insert_into=point_world)
worlds.Sphere(position=(0.02,.0,0.02), size=(.08,.08,.08), material=energy, quality=(4,4), insert_into=point_world)
worlds.Sphere(position=(0.02,.0,0.02), size=(.06,.06,.06), material=energy, quality=(3,3), insert_into=point_world)
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

boardmap=BoardMap(11,11)
gameturn=GameTurn()


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


num_sharps = 0
while num_sharps<11*11/8:
	x = random.randrange(11)
	y = random.randrange(11)
	if boardmap.getxy(x,y) == None:
		sharp = worlds.Body(mesh_sharp)
		sharp.x = x
		sharp.z = y
		boardmap.setxy(x,y,sharp)
		boardmap.setwall(x,y)
		num_sharps += 1
		
num_enemies = 0
totalenemies = 1
enemies=[]
while num_enemies < totalenemies:
	x = random.randrange(3)+8
	y = random.randrange(11/totalenemies)+num_enemies*11/totalenemies
	if boardmap.getxy(x,y) == None:
		squisher = BoardCharacter("chef_morkul",x,y,boardmap,"$")
		squisher.scale(.5,.5,.5)
		gameturn.addBody(squisher)
		enemies.append(squisher)
		num_enemies += 1

num_humans = 0 
while num_humans < 1:
	x = random.randrange(3)
	y = random.randrange(5)+3
	if boardmap.getxy(x,y) == None:
		sorcerer = BoardCharacter("balazar",x,y,boardmap,"H")
		sorcerer.scale(.6,.6,.6)
		gameturn.addBody(sorcerer)
		num_humans += 1


for x in range(11):
	for y in range(11):
		if boardmap.getxy(x,y) == None:
			point = BoardPoint(mesh_point,x,y,boardmap)
			point.y=0.1

	
worlds.camera.fov = 60
frame = 0

def mainloop():
	global gameturn,sorcerer,lblPoints
	lblPoints.text = u"%d Points" % sorcerer.points
	
	BodyInTurn=gameturn.inTurn()
	if BodyInTurn!=None:
		if BodyInTurn==sorcerer:
			if human_move():
				gameturn.beginMove()
		else:
			enemies_move(BodyInTurn)
			gameturn.beginMove()
	else:
		gameturn.checkEndMove()


def human_move():
	global sorcerer
	if sorcerer.is_inplace():
		if sdlconst.K_UP in worlds.KEY:		
			return sorcerer.character_move(0,-1)
		if sdlconst.K_DOWN in worlds.KEY:				
			return sorcerer.character_move(0,1)
		if sdlconst.K_LEFT in worlds.KEY:   	
			return sorcerer.character_move(-1,0)
		if sdlconst.K_RIGHT in worlds.KEY:	
			return sorcerer.character_move(1,0)
	
	return False


def enemies_move(enemy):
	global enemies,sorcerer
	dx1 = sorcerer.desired_x - enemy.x + random.uniform(-4,4)
	dy1 = sorcerer.desired_z - enemy.z + random.uniform(-4,4)
	dx = 1 if dx1 > 0 else -1
	dy = 1 if dy1 > 0 else -1
	if abs(dx1) < 1: 
		dx1 = 1
		dy1 *=10

	if abs(dy1) < 1: 
		dy1 = 1
		dx1 *=10
	dx1=round(abs(dx1),0)
	dy1=round(abs(dy1),0)
	
	if random.randrange(dx1) > random.randrange(dy1):
		if enemy.character_move(dx,0): return True
		if enemy.character_move(0,dy): return True
		if enemy.character_move(0,-dy): return True
		if enemy.character_move(-dx,0): return True
	else:
		if enemy.character_move(0,dy): return True
		if enemy.character_move(dx,0): return True
		if enemy.character_move(-dx,0): return True
		if enemy.character_move(0,-dy): return True
	return False

def renderloop(proportion):
	global frame,sorcerer,sharps
	frame += proportion
	worlds.camera.set_xyz(5+math.sin(frame/200.0)*2,12,16)
	worlds.camera.look_at(sorcerer)
	dist = worlds.camera.distance_to(sorcerer)
	dfov = 600/dist
	worlds.camera.fov = (worlds.camera.fov  * 10+ dfov) / 11.0
	
	
worlds.init_gui()
import soya.gui

table = soya.gui.VTable(worlds.root, 2)
table.row_pad = 10
table.col_pad = 10
table.border_pad = 1

label=soya.gui.Label(table, u"Score:")
label.color = (1.0,1.0,1.0,0.5)

lblPoints=soya.gui.Label(table, u"0 Points")
lblPoints.color = (1.0,1.0,1.0,0.8)

 
#import hotshot, hotshot.stats
#prof = hotshot.Profile("worlds.prof")
#prof.start()

worlds.begin_guiloop(mainloop, renderloop)

#prof.stop()
#prof.close()
#stats = hotshot.stats.load("worlds.prof")
#stats.strip_dirs()
#stats.sort_stats('time', 'calls')
#stats.print_stats()


