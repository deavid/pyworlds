import soya
import pyworlds.worlds
from pyworlds.utils import *


SIM_TYPE= {
	# none - No simulation at all. 
	# (The body gets paused)
		'none': 0, 
		
	# Simulation done on each frame render 
	# (Good for fast-action games, live is good for games with low cpu use)
		'live': 1, 
		
	# Simulation done in each round, and the render is interpolated
	# (Good for simulation games than need to execute thins more often than once per frame)
	# (Interpolation has a penalty: the object is rendered with a lag of one round) 
		'round': 2,
		'interpolated': 2,
		
	# Simulation done in both, on rounds and on each frame.
	# (Increases CPU cost to create a simulation that doesn't need to interpolate)
		'both': 3,
		
		
	}

class Body(soya.Body):
	def __init__(self, parent = None, model = None):
		soya.Body.__init__(self,parent,model)
		self.set_timefactor(1)
		self.elapsed_render_time = 0
		self.elapsed_round_time = 0
		self.elapsed_real_time = 0
		self.set_timesimulation(SIM_TYPE['live'])
		self.time_factor = 1
		self.min_elapse_time = 1 / 80.0
		self.max_elapse_time = 1 / 20.0
		self.state1 = soya.CoordSystState(self)
		self.state2 = soya.CoordSystState(self)
		self.state1_time = 0
		self.state2_time = 0

	def set_timesimulation(self,sim_type):
		self.sim_type=sim_type
		
	def set_timefactor(self,factor):
		self.time_factor = factor
		
	def elapse_to_time(self,new_time):
		seconds = new_time - self.elapsed_real_time
		total_elapsed=0
		while seconds > self.min_elapse_time:
			if seconds > self.max_elapse_time:
				seconds = self.max_elapse_time
			elapsed_seconds = self.elapsed_time(seconds)
			if elapsed_seconds : seconds = elapsed_seconds
			assert seconds > self.min_elapse_time / 2.0 
			
			self.elapsed_real_time += seconds
			total_elapsed += seconds
			seconds = new_time - self.elapsed_real_time
		return total_elapsed 
		
	def elapsed_time(self,seconds):
		return seconds
	
	def get_absoluteangleXZ(self,vector=None):
		parent = self.get_root()
		if vector == None:
			vector = soya.Vector(self,0,0,-1)

		q=vector % parent 
		
		return xy_toangle(q.x,q.z)

	def begin_round(self):
		soya.Body.begin_round(self)
		
		
				
		self.round_duration = self.parent.round_duration * self.time_factor 
		
		seconds = 1 * self.round_duration
		self.elapsed_round_time += seconds
		elapsed = 0
		if (self.sim_type == SIM_TYPE['round'] or 
				self.sim_type == SIM_TYPE['both']):
			elapsed = self.elapse_to_time(self.elapsed_round_time)

		if elapsed > 0:
			self.state1 = soya.CoordSystState(self.state2)
			self.state2 = soya.CoordSystState(self)
			self.state1_time = self.state2_time 
			self.state2_time = self.elapsed_round_time
		
		
	def advance_time(self, proportion):
		soya.Body.advance_time(self, proportion)
		seconds = proportion * self.round_duration
		self.elapsed_render_time += seconds
		
		if (self.sim_type == SIM_TYPE['live'] or 
				self.sim_type == SIM_TYPE['both']):
			self.elapse_to_time(self.elapsed_render_time)
		else:
			time1 = self.state2_time - self.state1_time
			time2 = self.elapsed_render_time - self.state1_time
			if time1>0:
				factor = time2 / time1
				self.interpolate(self.state1, self.state2, factor)

	def end_round(self):
		if (self.sim_type == SIM_TYPE['live'] or 
				self.sim_type == SIM_TYPE['both']):
			pass
		else:
			self.interpolate(self.state1, self.state2, 1)
		


class PhysicsBody(Body):
	def __init__(self, parent = 'scene', mesh = None, mesh_file = None, animatedmesh_file = None):
		if parent == 'scene':
			
			parent = pyworlds.worlds.scene
			
		if mesh_file:
			mesh = soya.Model.get(mesh_file)
		
		if animatedmesh_file:
			mesh = soya.AnimatedModel.get(animatedmesh_file)

		self.mesh = mesh
			
		Body.__init__(self,parent,mesh)
		self.initialize_vars()
		
	def initialize_vars(self):
		self.speed  = soya.Vector(None)
		self.rotation = [0,0,0]
		
	def elapsed_time(self,seconds):
		self.add_mul_vector(seconds, self.speed)
		self.rotate_x(seconds * self.rotation[0])
		self.rotate_y(seconds * self.rotation[1])
		self.rotate_z(seconds * self.rotation[2])
		
		
		
class CharacterBody(PhysicsBody):
	def initialize_vars(self):
		PhysicsBody.initialize_vars(self)
		self.states = {
						"stop" : ["garde","attente"], 
						"walk" : ["marche"],
						}
		self.state = None
		self.statecycle = None
		self.character_setstate("stop")
		self.desiredangle = 0
		self.look_at_speed = 10
		self.angle = 0 
		
	def elapsed_time(self, seconds):
		PhysicsBody.elapsed_time(self, seconds)

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
