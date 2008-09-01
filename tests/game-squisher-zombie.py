#!/usr/bin/python 
import worlds
from worlds import sdlconst,soya
import soya.widget as widget
import soya.cube
import soya.sdlconst as sdlconst
import math,random


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
		self.x=x
		self.z=y
		self.desired_x=x
		self.desired_z=y
		self.map_xy = None
		self.boardmap = board
		self.boardmap.setxy(x,y,self)
		self.boardmap.setwall(x,y,char)
		
		
	def begin_round(self):
		worlds.Character.begin_round(self)		
		anglewrong=abs(self.angle-self.desiredangle)
		if anglewrong>180: 
			anglewrong-=360; 
			anglewrong=abs(anglewrong)
		self.distance=self.dist_to_walk()
			
		if self.distance>0.2:
			
			if self.distance<-self.velocity.z*3.0:
				self.character_setstate("stop")
				self.velocity.z = -self.distance / 3.0
				self.character_updateangle()
			elif self.distance>0.4 and self.velocity.z>-0.5: 
				self.character_setstate("walk")
				if anglewrong<20: anglewrong = 20.0
				self.velocity.z =-2 / anglewrong
				self.character_updateangle()
		else:
			if self.map_xy != None:
				mx,my= self.map_xy
				if (round(mx,1) != round(self.desired_x,1)
					or round(my,1) != round(self.desired_z,1)):
						self.update_mapxy()
			else:
				self.update_mapxy()
			self.velocity.z /=1.2
			self.x=(self.x*10+self.desired_x)/11.0
			self.z=(self.z*10+self.desired_z)/11.0
			
	def advance_time(self, proportion):
		worlds.Character.advance_time(self, proportion)
		
	def is_inplace(self):
		if self.map_xy != None:
			mx,my= self.map_xy
			if (round(mx,1) != round(self.desired_x,1)
				or round(my,1) != round(self.desired_z,1)):
				return False
			else:
				return True
				
		if ( abs(self.desired_x-self.x)<0.1 and
				 abs(self.desired_z-self.z)<0.1 ):
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
		self.boardmap.setwall(dx,dy)
		
		return True
		
					

	def character_move(self,dx,dy):
		if not self.boardmap.iswall(self.desired_x+dx,
		self.desired_z+dy) :
			self.desired_x+=dx
			self.desired_z+=dy
			self.update_mapxy()
			self.character_updateangle()
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
		self.deleted=True

	def __init__(self,filename,x,y,board):
		BoardCharacter.__init__(self,filename,x,y,board)
		self.deleted=False
		
	def begin_round(self):
		if self.deleted:
			self.velocity.y+=0.01
		else:
			BoardCharacter.begin_round(self)		
		
		
	
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
worlds.Sphere(position=(0.02,.0,0.02), size=(.12,.08,.1), material=energy, quality=(8,8), insert_into=point_world)
worlds.Sphere(position=(0.02,.0,0.02), size=(.08,.08,.08), material=energy, quality=(6,6), insert_into=point_world)
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
while num_sharps<11*11/3:
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
enemies=[]
while num_enemies < 2:
	x = random.randrange(3)+8
	y = random.randrange(5)+num_enemies*5
	if boardmap.getxy(x,y) == None:
		squisher = BoardCharacter("chef_morkul",x,y,boardmap,"$")
		squisher.scale(.5,.5,.5)
		enemies.append(squisher)
		num_enemies += 1

num_humans = 0 
while num_humans < 1:
	x = random.randrange(3)
	y = random.randrange(5)+3
	if boardmap.getxy(x,y) == None:
		sorcerer = BoardCharacter("balazar",x,y,boardmap,"H")
		sorcerer.scale(.6,.6,.6)
		num_humans += 1


for x in range(11):
	for y in range(11):
		if boardmap.getxy(x,y) == None:
			point = BoardPoint(mesh_point,x,y,boardmap)
			point.y=0.1

	
worlds.camera.fov = 60
frame = 0

def mainloop():
	if human_move():
		enemies_move()


def human_move():
	global sorcerer
	if sorcerer.is_inplace():
		if sdlconst.K_UP in worlds.KEY:		
			del worlds.KEY[sdlconst.K_UP]
			return sorcerer.character_move(0,-1)
		if sdlconst.K_DOWN in worlds.KEY:				
			del worlds.KEY[sdlconst.K_DOWN]
			return sorcerer.character_move(0,1)
		if sdlconst.K_LEFT in worlds.KEY:   	
			del worlds.KEY[sdlconst.K_LEFT]
			return sorcerer.character_move(-1,0)
		if sdlconst.K_RIGHT in worlds.KEY:	
			del worlds.KEY[sdlconst.K_RIGHT]
			return sorcerer.character_move(1,0)
	
	return False


def enemies_move():
	global enemies,sorcerer
	for enemy in enemies:
		dx1 = sorcerer.x - enemy.x 
		dy1 = sorcerer.z - enemy.z
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
			if enemy.character_move(dx,0): continue
			if enemy.character_move(0,dy): continue
			if enemy.character_move(0,-dy): continue
			if enemy.character_move(-dx,0): continue
		else:
			if enemy.character_move(0,dy): continue
			if enemy.character_move(dx,0): continue
			if enemy.character_move(-dx,0): continue
			if enemy.character_move(0,-dy): continue

def renderloop(proportion):
	global frame,sorcerer,sharps
	frame += proportion
	worlds.camera.set_xyz(5+math.sin(frame/200.0)*2,12,16)
	worlds.camera.look_at(sorcerer)
	dist = worlds.camera.distance_to(sorcerer)
	dfov = 500/dist
	worlds.camera.fov = (worlds.camera.fov  * 10+ dfov) / 11.0
	
	


worlds.begin_loop(mainloop, renderloop)
