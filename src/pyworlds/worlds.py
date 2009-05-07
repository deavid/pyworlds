import sys, os, os.path, soya
import soya.widget as widget
from soya import sdlconst
import soya.widget
import math

from utils import *
import basics.scene

global scene,camera,light

scene = None
camera = None
light = None
pyworlds_engine = ""
# TODO: Create a full-camera class to handle several kinds of performance for cameras

animated_meshes = {}
meshes = {}
KEY = {}
MOUSE_X = 0
MOUSE_Y = 0
MOUSE_BUTTON = {}

# TODO: Place functions to access KEY, and return float or bool values. x>0.5 => True
callback_round = None
callback_advance = None
# TODO: Add the user-callback
scene_body = None
# TODO: Delete scene_body and use main Soya callbacks

enable_fps = False

# Import Psyco if available
try:
		import psyco
		psyco.full()
		print "Psyco found and started -- Python code accelerated."
except ImportError:
		print "I can't find PsyCo -- install it to get more speed"
		pass



def is_pyWorlds_installed():
	print "pyWorlds seem to be installed and working."
	return True
	
	
def init(create_basic=True):
	global scene,mainloop,pyworlds_engine
	pyworlds_engine = "soya"
	soya.init()
	soya.path.append(os.path.join(os.path.dirname(sys.argv[0]), "data"))
	scene = basics.scene.scene
	mainloop=soya.MainLoop(scene)
	scene.mainloop=mainloop
	scene.round_duration=.04
	mainloop.round_duration=.04
	if create_basic:
		init_basicscene()

def init_basicscene():
	global scene, light, camera
	light = soya.Light(scene)
	light.directional = 1
	light.rotate_x(-90)

	camera = soya.Camera(scene)
	#camera.set_xyz(0,2,5)
	#camera.rotate_x(-15)
	camera.back = 200
	#camera = soya.TravelingCamera(scene)


def begin_loop(callbackround=None, callbackadvance=None, engine="soya" ):
	global scene, callback_round, callback_advance, camera,mainloop
        import soya.pudding as pudding
	callback_round = callbackround
	callback_advance = callbackadvance 
	if engine=="soya":
            soya.set_root_widget(camera)
        elif engine=="pudding":
            pass
        else:
            print "error engine %s unknown" % engine
	#soya.set_root_widget(soya.widget.Group())
	#soya.root_widget.add(camera)
	#if enable_fps: soya.root_widget.add(soya.widget.FPSLabel())
	scene_body = SceneBody(scene,None)
	mainloop.main_loop()

def init_gui():
	global root,viewport
	import soya.gui
	
	root = soya.gui.RootLayer(None)
	viewport = soya.gui.CameraViewport(root, camera)
	

def init_pudding(width = 500,height = 500, options = {}):
	global root,viewport,camera,scene,mainloop, pyworlds_engine
        soya.path.append(os.path.join(os.path.dirname(sys.argv[0]), "data"))
	pyworlds_engine = "pudding"
        import soya.pudding as pudding
        soya.init()
	pudding.init()
	scene = basics.scene.scene
	mainloop=pudding.main_loop.MainLoop(scene)
	scene.mainloop=mainloop
	scene.round_duration=.04
	mainloop.round_duration=.04
        
	
        init_basicscene()
        soya.set_root_widget(pudding.core.RootWidget(width = width,height = height))
        if 'nochild' not in options: soya.root_widget.add_child(camera)
	
        

def begin_guiloop(callbackround=None, callbackadvance=None ):
	global root, mainloop
	global scene, callback_round, callback_advance, camera
	callback_round = callbackround
	callback_advance = callbackadvance 


	soya.set_root_widget(root)
	scene_body = SceneBody(scene,None)
	mainloop.main_loop()



class SceneBody(soya.Body):
  def advance_time(self, proportion):
	  global callback_advance
	  soya.Body.advance_time(self, proportion)
	  if callback_advance: callback_advance(proportion)
	
  def begin_round(self):
    global KEY,callback_round, MOUSE_X, MOUSE_Y, MOUSE_BUTTON
    soya.Body.begin_round(self)
    array_events = []
    if pyworlds_engine == "soya":
        array_events = soya.process_event()
    elif pyworlds_engine == "pudding":
        import soya.pudding as pudding
        array_events = pudding.process_event()
    
    for event in array_events:

        if event[0] == soya.sdlconst.KEYDOWN:
            if event[1] == soya.sdlconst.K_ESCAPE: soya.MAIN_LOOP.stop()
            else:
                KEY[event[1]]=event[:]

        elif event[0] == sdlconst.KEYUP:
          if event[1] in KEY:   del KEY[event[1]]

        elif event[0] == sdlconst.QUIT:
            soya.MAIN_LOOP.stop()				

        elif event[0] == soya.sdlconst.MOUSEBUTTONDOWN:
                    MOUSE_BUTTON[event[1]]=event[:]
                    MOUSE_X = event[2]			
                    MOUSE_Y = event[3]			
        
        elif event[0] == soya.sdlconst.MOUSEBUTTONUP:			
                    del MOUSE_BUTTON[event[1]] 
                    MOUSE_X = event[2]			
                    MOUSE_Y = event[3]			
        
        elif event[0] == soya.sdlconst.MOUSEMOTION:
                    MOUSE_X = event[1]			
                    MOUSE_Y = event[2]			



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




#class Character(soya.Body):
	#def __init__(self,filename):
		#global scene
		#if type(filename) == type(''):
			#if filename in animated_meshes:
				#mesh = animated_meshes[filename]
			#else:
				#mesh = soya.AnimatedModel.get(filename)
				#animated_meshes[filename] = mesh
		#else:
			## if it's not a text it is a animated-mesh.
			#mesh = filename
		#self.mesh = mesh
		## print "Available meshes    :", sorcerer_model.meshes    .keys()
		## print "Available animations:", mesh.animations.keys()
		## -> Available animations: ['marche', 'tourneD', 'chute', 'tourneG', 'attente', 'recule']

		#soya.Body.__init__(self,scene,mesh)
		#self.states = {
						#"stop" : ["garde","attente"], 
						#"walk" : ["marche"],
						#}
		#self.state = None
		#self.statecycle = None
		#self.character_setstate("stop")
		#self.velocity = soya.Vector(self,0,0,0)
		#self.rotation = [0,0,0]
		#self.desiredangle = 0
		#self.look_at_speed = 10
		
	#def advance_time(self, proportion):
		#soya.Body.advance_time(self, proportion)
		#elapsed = mainloop.round_duration * proportion
		#if elapsed==0: elapsed=0.001
		#self.angle = self.get_absoluteangleXZ()
		#if self.desiredangle >= 360: self.desiredangle-=360
		#if self.desiredangle < 0: self.desiredangle+=360
		
		#anglediff = self.desiredangle - self.angle
		#if anglediff > 180:	anglediff-=360
		#if anglediff < -180:	anglediff+=360
		#factor = self.look_at_speed
		#if factor > 1/elapsed : factor = 1/elapsed 
		#anglemov = anglediff * factor
		
		#if abs(self.rotation[1])>abs(anglemov): 
			#self.rotation[1]=(self.rotation[1]-anglemov)/2.0
		#else:
			#self.rotation[1]=(self.rotation[1]*5-anglemov)/6.0
		#if abs(anglediff)<1:
			#self.rotation[1]=-anglediff
		
		#self.add_mul_vector(elapsed , self.velocity)
		#self.rotate_x(elapsed * self.rotation[0])
		#self.rotate_y(elapsed * self.rotation[1])
		#self.rotate_z(elapsed * self.rotation[2])
		
	#def get_absoluteangleXZ(self,vector=None):
		#if vector == None:
			#vector = soya.Vector(self,0,0,-1)

		#q=vector % scene # I mean an upper container.
		
		#return xy_toangle(q.x,q.z)

	#def character_setstate(self,newstate):
		#if newstate==self.state: return False
		#if not hasattr(self.mesh,"animations"): return False
		#if len(self.states[newstate])<1: raise
		#newstatecycle=None
		#try:
			#for statecycle in self.states[newstate]:
				#if statecycle in self.mesh.animations:
					#newstatecycle=statecycle
					#break;
		#except:
			#raise
		#if not newstatecycle: 
			#print "Not found any animation for %s: " % newstate,  self.states[newstate]
			#print "Available animations:", self.mesh.animations.keys()
			#raise

		#if self.statecycle:
			#self.animate_clear_cycle(self.statecycle)			
			#self.statecycle = None
		#self.animate_blend_cycle(newstatecycle)
		#self.statecycle = newstatecycle
		#self.state=newstate
		#return True
	





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

					


