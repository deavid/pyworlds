#!/usr/bin/python 

import sys, os, os.path, soya
from soya import sdlconst
import soya.widget
import math

scene = None
camera = None
light = None

animated_meshes = {}
meshes = {}
KEY = {}
callback_round = None
callback_advance = None
scene_body = None

enable_fps = False

def is_pyWorlds_installed():
	print "pyWorlds seem to be installed and working."
	return True
	
	
def init(create_basic=True):
	global scene
	soya.init()
	soya.path.append(os.path.join(os.path.dirname(sys.argv[0]), "data"))
	scene = soya.World()
	if create_basic:
		init_basicscene()

def init_basicscene():
	global scene, light, camera
	light = soya.Light(scene)
	light.directional = 1
	light.rotate_x(-90)
	

	camera = soya.Camera(scene)
	camera.set_xyz(0,2,5)
	camera.rotate_x(-15)
	camera.back = 200
	#camera = soya.TravelingCamera(scene)
	
def begin_loop(callbackround=None, callbackadvance=None ):
	global scene, callback_round, callback_advance, camera
	callback_round = callbackround
	callback_advance = callbackadvance 
	soya.set_root_widget(soya.widget.Group())
	soya.root_widget.add(camera)
	if enable_fps: soya.root_widget.add(soya.widget.FPSLabel())
	scene_body = SceneBody(scene,None)
	soya.MainLoop(scene).main_loop()
	
class SceneBody(soya.Body):
	def advance_time(self, proportion):
		global callback_advance
		soya.Body.advance_time(self, proportion)
		if callback_advance: callback_advance(proportion)
	
	def begin_round(self):
		global KEY,callback_round
		soya.Body.begin_round(self)		
		for event in soya.process_event():
			if event[0] == soya.sdlconst.KEYDOWN:
				if event[1] == soya.sdlconst.K_ESCAPE: soya.MAIN_LOOP.stop()
				else:
					KEY[event[1]]=True
					
			elif event[0] == sdlconst.KEYUP:
				if event[1] in KEY:	del KEY[event[1]]
				
			elif event[0] == sdlconst.QUIT:
				soya.MAIN_LOOP.stop()				
		
		if callback_round: callback_round()


class Body(soya.Body):
	def __init__(self,filename):
		global scene
		if type(filename) == type(''):
			if filename in meshes:
				mesh = meshes[filename]
			else:
				mesh = soya.Model.get(filename)
				meshes[filename] = mesh
		else:
			# if it's not a text it is a mesh.
			mesh = filename
		
		self.mesh = mesh
		soya.Body.__init__(self,scene,mesh)
		self.velocity = soya.Vector(self,0,0,0)
		self.rotation = [0,0,0]
	
	def advance_time(self, proportion):
		soya.Body.advance_time(self, proportion)
		self.add_mul_vector(proportion, self.velocity)
		self.rotate_x(proportion * self.rotation[0])
		self.rotate_y(proportion * self.rotation[1])
		self.rotate_z(proportion * self.rotation[2])

	#def begin_round(self):
	#	soya.Body.begin_round(self)		

class Character(soya.Body):
	def __init__(self,filename):
		global scene
		if type(filename) == type(''):
			if filename in animated_meshes:
				mesh = animated_meshes[filename]
			else:
				mesh = soya.AnimatedModel.get(filename)
				animated_meshes[filename] = mesh
		else:
			# if it's not a text it is a animated-mesh.
			mesh = filename
		self.mesh = mesh
		# print "Available meshes    :", sorcerer_model.meshes    .keys()
		# print "Available animations:", mesh.animations.keys()
		# -> Available animations: ['marche', 'tourneD', 'chute', 'tourneG', 'attente', 'recule']

		soya.Body.__init__(self,scene,mesh)
		self.states = {
						"stop" : ["garde","attente"], 
						"walk" : ["marche"],
						}
		self.state = None
		self.statecycle = None
		self.character_setstate("stop")
		self.velocity = soya.Vector(self,0,0,0)
		self.rotation = [0,0,0]
		self.desiredangle = 0
		
	def advance_time(self, proportion):
		soya.Body.advance_time(self, proportion)
		self.add_mul_vector(proportion, self.velocity)
		self.rotate_x(proportion * self.rotation[0])
		self.rotate_y(proportion * self.rotation[1])
		self.rotate_z(proportion * self.rotation[2])

		
		
	def get_absoluteangleXZ(self,vector=None):
		if vector == None:
			vector = soya.Vector(self,0,0,-1)

		q=vector % scene # I mean an upper container.
		h_xz=math.sqrt(q.x*q.x+q.z*q.z)
		x=q.x/h_xz
		z=q.z/h_xz
		angle=math.asin(z)*180/math.pi
		if x<0:
			angle+=90  # place 0 degrees up
			angle=-angle # mirror the result
			angle-=90  # restore it.
			
		if angle<0: angle+=360
		
		return angle
		
		
		

	def begin_round(self):
		soya.Body.begin_round(self)		
		self.angle = self.get_absoluteangleXZ()
		if self.desiredangle >= 360: self.desiredangle-=360
		if self.desiredangle < 0: self.desiredangle+=360
		
		anglediff = self.desiredangle - self.angle
		if anglediff > 180:	anglediff-=360
		if anglediff < -180:	anglediff+=360
		anglemov = anglediff/3.0
		
		if abs(self.rotation[1])>abs(anglemov): 
			self.rotation[1]=(self.rotation[1]-anglemov)/2.0
		else:
			self.rotation[1]=(self.rotation[1]*5-anglemov)/6.0
		if abs(anglediff)<1:
			self.rotation[1]=-anglediff

	def character_setstate(self,newstate):
		if newstate==self.state: return False
		if len(self.states[newstate])<1: raise
		newstatecycle=None
		try:
			for statecycle in self.states[newstate]:
				if statecycle in self.mesh.animations:
					newstatecycle=statecycle
					break;
		except:
			raise
		if not newstatecycle: 
			print "Not found any animation for %s: " % newstate,  self.states[newstate]
			print "Available animations:", self.mesh.animations.keys()
			raise

		if self.statecycle:
			self.animate_clear_cycle(self.statecycle)			
			self.statecycle = None
		self.animate_blend_cycle(newstatecycle)
		self.statecycle = newstatecycle
		self.state=newstate
		return True
	
class FollowBody(Body):
	def __init__(self,filename,target):
		Body.__init__(self,filename)
		self.x=target.x
		self.y=target.y
		self.z=target.z
		self.advance_time(-5)
		self.target = target
		self.target_distance = [0.1,.4,3]
		self.set_springfactor(16)

		for i in range(25):
			self.begin_round()
			self.advance_time(0.5)
	
	def set_springfactor(self,factor):
		self.target_springfactor = factor / 100.0
		self.target_velocity = 1 / (self.target_springfactor+1)
		
	def begin_round(self):
		Body.begin_round(self)		
		
		distance = self.distance_to(self.target)
		_min = self.target_distance[0]
		_med = self.target_distance[1]
		_max = self.target_distance[2]
		factor = 1
		Q = 1
		if distance <= _min: factor = 0.0
		elif distance >= _max: factor = 0.0
		else:
			Q = (_med - distance) 
			if distance < _med:
				Q /= math.sqrt(_med - _min)
				factor = (distance - _min) / (_med - _min)
			else:
				Q /= math.sqrt(_max - _med)
				factor = (_max - distance) / (_max - _med)
		
		
		
		factor2 = (_med - distance) / (_max - _min)  
		if factor2 < 1: factor2 = 1
		if self.velocity.z>1:
			factor/=self.velocity.z
		vel = self.target_velocity 
		# self.velocity.z =  (self.velocity.z * self.target_springfactor * factor + Q * vel ) / (self.target_springfactor * factor + 1 )
		self.velocity.z =  (self.velocity.z * self.target_springfactor * factor + (_med - distance) * vel ) / (self.target_springfactor * factor + 1 )
		#self.velocity.z *=  factor2
		
		if distance<_max:
			look_at_elastic(self,self.target, sqrt_from=360, factor=(1-factor)+.3)
		else:
			self.look_at(self.target)
			

					



def Box(x,y,z,parent = None, material = None, insert_into = None, texcoord_size=1, origin=(0,0,0)):
	"""Box(parent = None, material = None, insert_into = None) -> World

Creates and returns a World in PARENT, containing a box(x,y,z) length centered
on the origin, with material MATERIAL.

If INSERT_INTO is not None, the cube's faces are inserted into it, instead of
creating a new world."""
	ox=origin[0]
	oy=origin[1]
	oz=origin[2]
	
	cube = insert_into or soya.World(parent)
	s = texcoord_size
	soya.Face(cube, [soya.Vertex(cube,  0.5*x+ox,  0.5 * y+oy,  0.5 * z+oz, 1.0*s, 1.0*s),
									soya.Vertex(cube, -0.5*x+ox,  0.5 * y+oy,  0.5 * z+oz, 0.0, 1.0*s),
									soya.Vertex(cube, -0.5*x+ox, -0.5 * y+oy,  0.5 * z+oz, 0.0, 0.0),
									soya.Vertex(cube,  0.5*x+ox, -0.5 * y+oy,  0.5 * z+oz, 1.0*s, 0.0),
									], material)

	soya.Face(cube, [soya.Vertex(cube,  0.5*x+ox,  0.5 * y+oy, -0.5 * z+oz, 0.0, 1.0*s),
									soya.Vertex(cube,  0.5*x+ox, -0.5 * y+oy, -0.5 * z+oz, 0.0, 0.0),
									soya.Vertex(cube, -0.5*x+ox, -0.5 * y+oy, -0.5 * z+oz, 1.0*s, 0.0),
									soya.Vertex(cube, -0.5*x+ox,  0.5 * y+oy, -0.5 * z+oz, 1.0*s, 1.0*s),
									], material)
	

	soya.Face(cube, [soya.Vertex(cube,  0.5*x+ox,  0.5 * y+oy,  0.5 * z+oz, 1.0*s, 0.0),
									soya.Vertex(cube,  0.5*x+ox,  0.5 * y+oy, -0.5 * z+oz, 1.0*s, 1.0*s),
									soya.Vertex(cube, -0.5*x+ox,  0.5 * y+oy, -0.5 * z+oz, 0.0, 1.0*s),
									soya.Vertex(cube, -0.5*x+ox,  0.5 * y+oy,  0.5 * z+oz, 0.0, 0.0),
									], material)
	soya.Face(cube, [soya.Vertex(cube,  0.5*x+ox, -0.5 * y+oy,  0.5 * z+oz, 1.0*s, 0.0),
									soya.Vertex(cube, -0.5*x+ox, -0.5 * y+oy,  0.5 * z+oz, 1.0*s, 1.0*s),
									soya.Vertex(cube, -0.5*x+ox, -0.5 * y+oy, -0.5 * z+oz, 0.0, 1.0*s),
									soya.Vertex(cube,  0.5*x+ox, -0.5 * y+oy, -0.5 * z+oz, 0.0, 0.0),
									], material)
	
	soya.Face(cube, [soya.Vertex(cube,  0.5*x+ox,  0.5 * y+oy,  0.5 * z+oz, 1.0*s, 1.0*s),
									soya.Vertex(cube,  0.5*x+ox, -0.5 * y+oy,  0.5 * z+oz, 1.0*s, 0.0),
									soya.Vertex(cube,  0.5*x+ox, -0.5 * y+oy, -0.5 * z+oz, 0.0, 0.0),
									soya.Vertex(cube,  0.5*x+ox,  0.5 * y+oy, -0.5 * z+oz, 0.0, 1.0*s),
									], material)
	soya.Face(cube, [soya.Vertex(cube, -0.5*x+ox,  0.5 * y+oy,  0.5 * z+oz, 0.0, 1.0*s),
									soya.Vertex(cube, -0.5*x+ox,  0.5 * y+oy, -0.5 * z+oz, 1.0*s, 1.0*s),
									soya.Vertex(cube, -0.5*x+ox, -0.5 * y+oy, -0.5 * z+oz, 1.0*s, 0.0),
									soya.Vertex(cube, -0.5*x+ox, -0.5 * y+oy,  0.5 * z+oz, 0.0, 0.0),
									], material)
	
	return cube

	


def Sphere(parent = None, material = None, quality = (10,10), smooth_lit = 1, insert_into = None, 
					texcoords=[(0,1),(0,1)], size=(1,1,1),position=(0,0,0)):
	"""Sphere(parent = None, material = None, slices = 20, stacks = 20, insert_into = None, min_tex_x = 0.0, max_tex_x = 1.0, min_tex_y = 0.0, max_tex_y = 1.0) -> World

Creates and returns a World in PARENT, containing a sphere of 1 radius centered
on the origin, with material MATERIAL.

SLICES and STACKS can be used to control the quality of the sphere.

If INSERT_INTO is not None, the sphere's faces are inserted into it, instead of
creating a new world.

MIN/MAX_TEX_X/Y can be used to limit the range of the texture coordinates to the given
values."""
	from math import sin, cos
	slices = quality[0]
	stacks = quality[1]
	
	min_tex_x = texcoords[0][0] 
	max_tex_x = texcoords[0][1]
	min_tex_y = texcoords[1][0]
	max_tex_y = texcoords[1][1]

	px=position[0]
	py=position[1]
	pz=position[2]
	
	sx=size[0]
	sy=size[1]
	sz=size[2]
	
	
	sphere = insert_into or World(parent)
	
	step1 = 6.28322 / slices
	step2 = 3.14161 / stacks
	
	angle1 = 0.0
	for i in xrange(slices):
		angle2 = 0.0
		j = 0
		
		face = soya.Face(sphere, [
			soya.Vertex(sphere, cos(angle1        ) * sin(angle2        ) * sx + px, cos(angle2        ) * sy + py, sin(angle1        ) * sin(angle2        ) * sz + pz, min_tex_x + (max_tex_x - min_tex_x) * float(i    ) / slices, min_tex_y + (max_tex_y - min_tex_y) * float(j    ) / stacks),
			soya.Vertex(sphere, cos(angle1 + step1) * sin(angle2 + step2) * sx + px, cos(angle2 + step2) * sy + py, sin(angle1 + step1) * sin(angle2 + step2) * sz + pz, min_tex_x + (max_tex_x - min_tex_x) * float(i + 1) / slices, min_tex_y + (max_tex_y - min_tex_y) * float(j + 1) / stacks),
			soya.Vertex(sphere, cos(angle1        ) * sin(angle2 + step2) * sx + px, cos(angle2 + step2) * sy + py, sin(angle1        ) * sin(angle2 + step2) * sz + pz, min_tex_x + (max_tex_x - min_tex_x) * float(i    ) / slices, min_tex_y + (max_tex_y - min_tex_y) * float(j + 1) / stacks),
			], material)
		face.smooth_lit = smooth_lit
		angle2 += step2
		
		for j in range(1, stacks - 1):
			face = soya.Face(sphere, [
				soya.Vertex(sphere, cos(angle1        ) * sin(angle2        ) * sx + px, cos(angle2        ) * sy + py, sin(angle1        ) * sin(angle2        ) * sz + pz, min_tex_x + (max_tex_x - min_tex_x) * float(i    ) / slices, min_tex_y + (max_tex_y - min_tex_y) * float(j    ) / stacks),
				soya.Vertex(sphere, cos(angle1 + step1) * sin(angle2        ) * sx + px, cos(angle2        ) * sy + py, sin(angle1 + step1) * sin(angle2        ) * sz + pz, min_tex_x + (max_tex_x - min_tex_x) * float(i + 1) / slices, min_tex_y + (max_tex_y - min_tex_y) * float(j    ) / stacks),
				soya.Vertex(sphere, cos(angle1 + step1) * sin(angle2 + step2) * sx + px, cos(angle2 + step2) * sy + py, sin(angle1 + step1) * sin(angle2 + step2) * sz + pz, min_tex_x + (max_tex_x - min_tex_x) * float(i + 1) / slices, min_tex_y + (max_tex_y - min_tex_y) * float(j + 1) / stacks),
				soya.Vertex(sphere, cos(angle1        ) * sin(angle2 + step2) * sx + px, cos(angle2 + step2) * sy + py, sin(angle1        ) * sin(angle2 + step2) * sz + pz, min_tex_x + (max_tex_x - min_tex_x) * float(i    ) / slices, min_tex_y + (max_tex_y - min_tex_y) * float(j + 1) / stacks),
				], material)
			face.smooth_lit = smooth_lit
			angle2 += step2

		j = stacks - 1
		
		face = soya.Face(sphere, [
			soya.Vertex(sphere, cos(angle1        ) * sin(angle2        ) * sx + px, cos(angle2        ) * sy + py, sin(angle1        ) * sin(angle2        ) * sz + pz, min_tex_x + (max_tex_x - min_tex_x) * float(i    ) / slices, min_tex_y + (max_tex_y - min_tex_y) * float(j    ) / stacks),
			soya.Vertex(sphere, cos(angle1 + step1) * sin(angle2        ) * sx + px, cos(angle2        ) * sy + py, sin(angle1 + step1) * sin(angle2        ) * sz + pz, min_tex_x + (max_tex_x - min_tex_x) * float(i + 1) / slices, min_tex_y + (max_tex_y - min_tex_y) * float(j    ) / stacks),
			soya.Vertex(sphere, cos(angle1        ) * sin(angle2 + step2) * sx + px, cos(angle2 + step2) * sy + py, sin(angle1        ) * sin(angle2 + step2) * sz + pz, min_tex_x + (max_tex_x - min_tex_x) * float(i    ) / slices, min_tex_y + (max_tex_y - min_tex_y) * float(j + 1) / stacks),
			], material)
		face.smooth_lit = smooth_lit
		
		angle1 += step1
		
	return sphere

def look_at_elastic(self,p2,vector=None, factor=0.5, sqrt_from=15):
	if p2 == None: raise Exception, "lookat_elastic: You must give at least the p2 parameter"
	if vector == None:
		vector = soya.Vector(self,0,0,-1000)

	q=vector % scene # I mean an upper container.
	
	v1 = (self >> q)
	v2 = (self >> p2)
	
	angle = v1.angle_to(v2)
	
	v12 = v1.cross_product(v2)
	a12 = v1.dot_product(v2)
	if a12<0: angle = -angle
	if abs(angle)>90: angle=-angle
	v12.normalize()
	if abs(angle) < 0.1: 
		return
	if abs(angle) == 180.0: angle=180.1;

	original_angle=angle
	
	if angle>sqrt_from:
		angle/=sqrt_from
		angle=math.sqrt(angle)
		angle*=sqrt_from	
	
	angle*=factor
	
	self.rotate_axis(angle, v12)
