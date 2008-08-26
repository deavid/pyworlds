#!/usr/bin/python 

import sys, os, os.path, soya

scene = None
camera = None
light = None

meshes = {}
KEY = {}
callback_round = None
callback_advance = None
scene_body = None

def is_pyWorlds_installed():
	print "pyWorlds seem to be installed and working."
	return True
	
	
def init(create_basic=True):
	global scene
	soya.init()
	soya.path.append(os.path.join(os.path.dirname(sys.argv[0]), "data"))
	scene = soya.World()
	scene_body = SceneBody(scene,None)
	if create_basic:
		init_basicscene()

def init_basicscene():
	global scene, light, camera
	light = soya.Light(scene)
	light.set_xyz(5.0,0.0,20.0)

	camera = soya.Camera(scene)
	camera.z = 10.0

	soya.set_root_widget(camera)
	
def begin_loop(callbackround=None, callbackadvance=None ):
	global scene, callback_round, callback_advance
	callback_round = callbackround
	callback_advance = callbackadvance 
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
					
			elif event[0] == soya.sdlconst.KEYUP:
				if event[1] in KEY:	del KEY[event[1]]
				
			elif event[0] == soya.sdlconst.QUIT:
				soya.MAIN_LOOP.stop()				
		
		if callback_round: callback_round()


class Body(soya.Body):
	def __init__(self,filename):
		global scene
		if filename in meshes:
			mesh = meshes[filename]
		else:
			mesh = soya.Model.get(filename)
			meshes[filename] = mesh
		
		
		soya.Body.__init__(self,scene,mesh)
		self.velocity = soya.Vector(self,0,0,0)
		self.rotation = [0,0,0]
		
	def advance_time(self, proportion):
		soya.Body.advance_time(self, proportion)
		self.rotate_x(proportion * self.rotation[0])
		self.rotate_y(proportion * self.rotation[1])
		self.rotate_z(proportion * self.rotation[2])
		self.add_mul_vector(proportion, self.velocity)

	def begin_round(self):
		soya.Body.begin_round(self)		

class FollowBody(Body):
	def __init__(self,filename,target):
		Body.__init__(self,filename)
		self.target = target
		self.target_distance = [0.2,1.0,2.2]
		self.target_springfactor = 100
		self.target_speed = -1
		self.begin_round()
		self.advance_time(2)
		
	def begin_round(self):
		Body.begin_round(self)		
		self.look_at(self.target)
		distance = self.distance_to(self.target)
		if distance < self.target_distance[1]: 
			_min = self.target_distance[0]
			_med = self.target_distance[1]
			_width = self.target_distance[1] - self.target_distance[0]
			if distance < _min: 
				self.velocity.z =  (_min - distance) 
			else:
				factor = ( distance - _min ) / _width
				self.velocity.z =  (self.velocity.z * self.target_springfactor * factor + distance - _med) / (self.target_springfactor * factor + 1 )
				
		if distance > self.target_distance[2]: 
			_max = self.target_distance[2]
			_med = self.target_distance[1]
			_width = self.target_distance[2] - self.target_distance[1]
			if distance > _max: 
				self.velocity.z =  distance - _max 
			else:
				factor = ( _max - distance ) / _width
				self.velocity.z =  (self.velocity.z * self.target_springfactor * factor + distance - _med) / (self.target_springfactor * factor + 1 )
				
		self.velocity.z *= self.target_speed
		
	
