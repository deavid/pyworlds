#!/usr/bin/python 

import sys, os, os.path, soya
import soya.widget as widget
from soya import sdlconst
import soya.widget
import math


global scene,camera,light
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

try:
		import psyco
		psyco.full()
		print "Psyco found and started -- Python code accelerated."
except ImportError:
		print "I can't find PsyCo for Python acceleration."
		pass



def is_pyWorlds_installed():
	print "pyWorlds seem to be installed and working."
	return True
	
	
def init(create_basic=True):
	# Import Psyco if available
	global scene
	soya.init()
	soya.path.append(os.path.join(os.path.dirname(sys.argv[0]), "data"))
	scene = soya.World()
	if create_basic:
		init_basicscene()

def init_basicscene():
	global scene, light, camera, mainloop
	light = soya.Light(scene)
	light.directional = 1
	light.rotate_x(-90)
	mainloop=soya.MainLoop(scene)
	mainloop.round_duration=.06
	

	camera = soya.Camera(scene)
	camera.set_xyz(0,2,5)
	camera.rotate_x(-15)
	camera.back = 200
	#camera = soya.TravelingCamera(scene)

def xy_toangle(x1,y1):
	h_xz=math.sqrt(x1*x1+y1*y1)
	x=x1/h_xz
	z=y1/h_xz
	angle=math.asin(z)*180/math.pi
	if x<0:
		angle+=90  # place 0 degrees up
		angle=-angle # mirror the result
		angle-=90  # restore it.
		
	if angle<0: angle+=360
	
	return angle


def begin_loop(callbackround=None, callbackadvance=None ):
	global scene, callback_round, callback_advance, camera,mainloop
	callback_round = callbackround
	callback_advance = callbackadvance 
	soya.set_root_widget(soya.widget.Group())
	soya.root_widget.add(camera)
	if enable_fps: soya.root_widget.add(soya.widget.FPSLabel())
	scene_body = SceneBody(scene,None)
	mainloop.main_loop()

def init_gui():
	global root,viewport
	import soya.gui
	
	root = soya.gui.RootLayer(None)
	viewport = soya.gui.CameraViewport(root, camera)
	
	

def begin_guiloop(callbackround=None, callbackadvance=None ):
	global root, mainloop
	global scene, callback_round, callback_advance, camera
	callback_round = callbackround
	callback_advance = callbackadvance 


	soya.set_root_widget(root)
	scene_body = SceneBody(scene,None)
	mainloop=soya.MainLoop(scene)
	mainloop.round_duration=.04
	mainloop.main_loop()

def begin_puddingloop(callbackround=None, callbackadvance=None ):
	global scene, callback_round, callback_advance, camera
	import soya.pudding as pudding
	import soya.pudding.ext.fpslabel
	import soya.pudding.ext.meter
	pudding.init()
	callback_round = callbackround
	callback_advance = callbackadvance 
	soya.set_root_widget(pudding.core.RootWidget())
	soya.root_widget.add_child(camera)
	pudding.ext.fpslabel.FPSLabel(soya.root_widget, position = pudding.TOP_RIGHT)

	health_bar = pudding.ext.meter.MeterLabel(soya.root_widget, "score:", 
				left = 10, top = 10, width = 1000,height = 20)
	health_bar.anchors = pudding.ANCHOR_TOP_LEFT
	health_bar.meter.max = 100
	health_bar.meter.width = 1000
	
	health_bar.meter.calc_step()
	
	#health_bar.meter.user_change = False                                      
	health_bar.meter.border_color = (1,1,1,0.8)
	health_bar.label.color = health_bar.meter.border_color

	logo = pudding.control.Logo(soya.root_widget, 'little-dunk.png')

	button = pudding.control.Button(soya.root_widget, 'Quit', left = 10, width = 50, height = 40)
	button.set_pos_bottom_right(bottom = 10)
	button.anchors = pudding.ANCHOR_BOTTOM | pudding.ANCHOR_LEFT
	button.on_click = sys.exit

	# Creates and run an "main_loop" (=an object that manage time and regulate FPS)
	# By default, FPS is locked at 40.

	scene_body = SceneBody(scene,None)
	pudding.main_loop.MainLoop(scene).main_loop()

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
		global mainloop
		soya.Body.advance_time(self, proportion)
		elapsed = mainloop.round_duration * proportion
		if elapsed==0: elapsed=0.001
		
		self.add_mul_vector(elapsed, self.velocity)
		self.rotate_x(elapsed * self.rotation[0])
		self.rotate_y(elapsed * self.rotation[1])
		self.rotate_z(elapsed * self.rotation[2])

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
		self.look_at_speed = 10
		
	def advance_time(self, proportion):
		soya.Body.advance_time(self, proportion)
		elapsed = mainloop.round_duration * proportion
		if elapsed==0: elapsed=0.001
		self.angle = self.get_absoluteangleXZ()
		if self.desiredangle >= 360: self.desiredangle-=360
		if self.desiredangle < 0: self.desiredangle+=360
		
		anglediff = self.desiredangle - self.angle
		if anglediff > 180:	anglediff-=360
		if anglediff < -180:	anglediff+=360
		factor = self.look_at_speed
		if factor > 1/elapsed : factor = 1/elapsed 
		anglemov = anglediff * factor
		
		if abs(self.rotation[1])>abs(anglemov): 
			self.rotation[1]=(self.rotation[1]-anglemov)/2.0
		else:
			self.rotation[1]=(self.rotation[1]*5-anglemov)/6.0
		if abs(anglediff)<1:
			self.rotation[1]=-anglediff
		
		self.add_mul_vector(elapsed , self.velocity)
		self.rotate_x(elapsed * self.rotation[0])
		self.rotate_y(elapsed * self.rotation[1])
		self.rotate_z(elapsed * self.rotation[2])
		
	def get_absoluteangleXZ(self,vector=None):
		if vector == None:
			vector = soya.Vector(self,0,0,-1)

		q=vector % scene # I mean an upper container.
		
		return xy_toangle(q.x,q.z)

	def character_setstate(self,newstate):
		if newstate==self.state: return False
		if not hasattr(self.mesh,"animations"): return False
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
		self.target = target
		self.target_distance = [0.5,1.0,2]
		self.set_springfactor(16)
		self.target_velocity = 1

		for i in range(25):
			self.begin_round()
			self.advance_time(0.5)
	
	def set_springfactor(self,factor):
		self.target_springfactor = factor / 100.0
		
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
			
	def advance_time(self, proportion):
		Body.advance_time(self, proportion)
		distance = self.distance_to(self.target)
		_min = self.target_distance[0]
		_med = self.target_distance[1]
		_max = self.target_distance[2]
		f3 = (distance - _med) / (_max - _med)
		f1 = self.target_springfactor * 100 + 1
		if f3>1: 
			f3=1
			
		f3*=proportion
		self.x = (self.x * f1 + self.target.x * f3) / (f1+f3)
		self.y = (self.y * f1 + self.target.y * f3) / (f1+f3)
		self.z = (self.z * f1 + self.target.z * f3) / (f1+f3)

					



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