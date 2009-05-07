import sys, os, os.path

sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), '..', '..')))
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

class BDriver:
    def __init__(self,body):
        # Time relative to function loop:
        self.elapsed_real_time = 0

        # computational limits    
        self.min_elapse_time = 0
        self.med_elapse_time = 1 / 20.0
        self.max_elapse_time = 1 / 10.0

        self.body = body
        body.add_driver(self)
        self.userloops = []
        
        battr = self.bodyattrname()
        if battr:
            setattr(body,battr,self)


    def bodyattrname(self): return None;
            
    def userloop(self, call):
        self.userloops.append(call)
        
    def elapse_to_time(self,new_time):
        seconds = new_time - self.elapsed_real_time
        total_elapsed=0
        while seconds > self.min_elapse_time:
            if seconds > self.max_elapse_time:
                seconds = self.med_elapse_time

            seconds = self.elapsed_time(seconds)

            for elapsedcall in self.userloops:
                elapsedcall(self,seconds)

            self.elapsed_real_time += seconds
            total_elapsed += seconds
            seconds = new_time - self.elapsed_real_time
        return total_elapsed    
        
    def elapsed_time(self,seconds):
        return seconds
        

class PhysicsBDriver(BDriver):
    def bodyattrname(self): return 'physicsBDriver';

    def elapsed_time(self,seconds):
        body = self.body
        
        body.add_mul_vector(seconds, body.speed)
        body.turn_x(seconds * body.rotation[0])
        body.turn_y(seconds * body.rotation[1])
        body.turn_z(seconds * body.rotation[2])
        return seconds
        
    

class Body(soya.Body):
    def __init__(self, parent = None, model = None):
        soya.Body.__init__(self,parent,model)
        self.set_timefactor(1)
        
        # Time when was displayed:
        self.elapsed_render_time = 0
        
        # Time relative to object simulation:
        self.elapsed_round_time = 0
        
        # Time relative to function loop:
        self.elapsed_real_time = 0
        
        self.set_timesimulation(SIM_TYPE['live'])
        self.time_factor = 1
        self.state1 = soya.CoordSystState(self)
        self.state2 = soya.CoordSystState(self)
        self.state1_time = 0
        self.state2_time = 0
        self.drivers = []

        # computational limits    
        self.min_elapse_time = 0
        self.med_elapse_time = 1 / 20.0
        self.max_elapse_time = 1 / 10.0

    def add_driver(self,the_driver):
        self.drivers.append(the_driver)
    
    def set_timesimulation(self,sim_type):
        self.sim_type=sim_type
        
    def set_timefactor(self,factor):
        self.time_factor = factor
        
    def elapse_to_time(self,new_time):
        seconds = new_time - self.elapsed_real_time
        total_elapsed=0
        while seconds > self.min_elapse_time:
            if seconds > self.max_elapse_time:
                seconds = self.med_elapse_time

            self.elapsed_real_time += seconds
            for driver in self.drivers:
                driver.elapse_to_time(self.elapsed_real_time)

            total_elapsed += seconds
            seconds = new_time - self.elapsed_real_time
        return total_elapsed 
           
    def get_absoluteangleXZ(self,vector=None):
        parent = self.get_root()
        if vector == None:
            vector = soya.Vector(self,0,0,-1)

        q=vector % parent 
        
        return xy_toangle(q.x,q.z)

    def begin_round(self):
        #soya.Body.begin_round(self)
        
        
                
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
        #soya.Body.advance_time(self, proportion)
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
        self.speed  = soya.Vector(self,0,0,0)
        self.rotation = [0,0,0]
        PhysicsBDriver(self)
        
        
        
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
        self.look_at_speed = 500
        self.angle = 0 
        
    def elapsed_time(self, body, seconds):
        PhysicsBody.elapsed_time(self, body, seconds)

        self.angle = self.get_absoluteangleXZ()
        if self.desiredangle >= 360: self.desiredangle-=360
        if self.desiredangle < 0: self.desiredangle+=360
        
        anglediff = self.desiredangle - self.angle
        if anglediff > 180:    anglediff-=360
        if anglediff < -180:    anglediff+=360
        factor = self.look_at_speed * seconds
        # -> we can't handle computing limit in this way:
        #if factor > 1/elapsed : factor = 1/elapsed 
        if factor > 1/seconds: 
            factor = 1/seconds
        
        anglemov = anglediff * factor
        
        if abs(self.rotation[1])>abs(anglemov): 
            self.rotation[1]=(self.rotation[1]-anglemov)/2.0
        else:
            self.rotation[1]=(self.rotation[1]*5-anglemov)/6.0
        if abs(anglediff)<1:
            self.rotation[1]=-anglediff
            
        return seconds
        
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
        




class Label3DFlat(soya.label3d.Label3D):
    def __init__(self, size = 0.01, compensation = 0.02, follows = None, offset = (0.0,1.0,1.0), *args, **kwargs):
        if 'parent' not in kwargs:
            kwargs['parent']=pyworlds.worlds.scene
        soya.label3d.Label3D.__init__(self, *args, **kwargs)
        self.flat_follows = follows
        self.flat_offset = offset
        self.flat_size = size
        self.flat_compensation = compensation
        self.size = size
        self.lit = 0

    def advance_time(self,proportion):
        if self.flat_follows:
            self.move(self.flat_follows)
            self.size = self.flat_size + self.flat_compensation * self.flat_size * self.distance_to(pyworlds.worlds.camera)
            
        matrix = list(self.matrix)
        for x in range(3):
            for y in range(3):
                matrix[x+y*4] = pyworlds.worlds.camera.matrix[x+y*4]
        self.matrix = tuple(matrix)
        self.add_vector(soya.Vector(self,self.flat_offset[0],self.flat_offset[1],self.flat_offset[2]))
        
