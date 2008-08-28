#!/usr/bin/python 

import sys, os, os.path, soya
from soya import sdlconst
from soya.widget


scene = None
camera = None
light = None

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

class FollowBody(Body):
	def __init__(self,filename,target):
		Body.__init__(self,filename)
		self.x=target.x
		self.y=target.y
		self.z=target.z
		self.advance_time(-5)
		self.target = target
		self.target_distance = [0.1,.4,3]
		self.set_springfactor(0)

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
		
		if distance <= _min: factor = 0.0
		elif distance >= _max: factor = 0.0
		else:
			if distance < _med:
				factor = (distance - _min) / (_med - _min)
			else:
				factor = (_max - distance) / (_max - _med)
		
		if factor < 0.2 : factor = 0.2
		
		factor2 = (_med - distance) / (_max - _min)  
		if factor2 < 1: factor2 = 1
		vel = self.target_velocity * factor2 
		self.velocity.z =  (self.velocity.z * self.target_springfactor * factor + (_med - distance) * vel ) / (self.target_springfactor * factor + 1 )
		self.velocity.z *=  factor2
		
		if self.velocity.z<0: self.look_at(self.target)
		if self.target.velocity.z>0.01: 
			self.target.look_at(self)
			self.target.rotate_y(180)

		self.velocity.z = (self.velocity.z + self.target.velocity.z * factor2) / (factor2+1.0)
		
		if self.velocity.z < 0: 
			if self.velocity.z < (_min - distance) :
				self.velocity.z = (_min - distance) 
			
			self.velocity.z *= factor2



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

	


