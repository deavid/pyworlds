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

class wBody(soya.World):
    def __init__(self, parent = None, model = None):
        soya.World.__init__(self,parent)

        self.body = soya.Body(self,model)
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
        self.round_duration = 0.04
        self.list_elapsecalls=[self.elapsed_time]

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

            for elapsedcall in self.list_elapsecalls:
                elapsedcall(seconds)
            # if elapsed_seconds : seconds = elapsed_seconds
            assert seconds > self.min_elapse_time / 2.0 

            self.elapsed_real_time += seconds
            total_elapsed += seconds
            seconds = new_time - self.elapsed_real_time
        return total_elapsed 
        
    def addloopcall(self, funccall):
        try:
            self.list_elapsecalls.append(funccall)
        except:
            raise
    
    def elapsed_time(self,seconds):
        return seconds
    
    def get_absoluteangleXZ(self,vector=None):
        parent = self.get_root()
        if vector == None:
            vector = soya.Vector(self,0,0,-1)

        q=vector % parent 
        
        return xy_toangle(q.x,q.z)

    def begin_round(self):
        soya.World.begin_round(self)
        
        
                
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
        soya.World.advance_time(self, proportion)
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
        soya.World.end_round(self)
        if (self.sim_type == SIM_TYPE['live'] or 
                self.sim_type == SIM_TYPE['both']):
            pass
        else:
            self.interpolate(self.state1, self.state2, 1)
        


class wPhysicsBody(wBody):
    def __init__(self, parent = 'scene', mesh = None, mesh_file = None, animatedmesh_file = None):
        if parent == 'scene':
            
            parent = pyworlds.worlds.scene
            
        if mesh_file:
            mesh = soya.Model.get(mesh_file)
        
        if animatedmesh_file:
            mesh = soya.AnimatedModel.get(animatedmesh_file)

        self.mesh = mesh
            
        wBody.__init__(self,parent,mesh)
        self.initialize_vars()
        
    def initialize_vars(self):
        self.speed  = soya.Vector(self,0,0,0)
        self.rotation = [0,0,0]
        
    def elapsed_time(self,seconds):
        self.add_mul_vector(seconds, self.speed)
        #self.rotate_x(seconds * self.rotation[0])
        #self.rotate_y(seconds * self.rotation[1])
        #self.rotate_z(seconds * self.rotation[2])

        self.turn_x(seconds * self.rotation[0])
        self.turn_y(seconds * self.rotation[1])
        self.turn_z(seconds * self.rotation[2])
        
        
        

m_black = soya.Material()
m_black.shininess = 0.1
m_black.diffuse   = (0.0, 0.0, 0.0, 0.2)
m_black.specular  = (0.0, 0.0, 0.0, 0.2)

m_red = soya.Material()
m_red.shininess = 0.1
m_red.diffuse   = (1.0, 0.0, 0.0, 0.5)
m_red.specular  = (1.0, 0.0, 0.0, 0.5)


class wLabel3DFlat(soya.World):
    def __init__(self, size = 0.01, compensation = 0.02, follows = None, offset = (0.0,1.0,1.0), *args, **kwargs):
        if 'parent' not in kwargs:
            kwargs['parent']=pyworlds.worlds.scene
        soya.World.__init__(self, kwargs['parent'])
        kwargs['parent'] = self
        text = ""
        if 'text' in kwargs:
            text =  kwargs['text']

        self.label = soya.label3d.Label3D(**kwargs)
        self.label.size = size
        self.label.lit = 0
        self.label.render()
            
        self.box =  soya.World(None)
        self.text_width, self.text_height = self.label._font.get_print_size(self.label._text)
        self.text_width+=10
        self.text_height+=10
        pyworlds.utils.Box(self.text_width*size,size*self.text_height,0,insert_into=self.box, material=m_black, origin = (0,1*size,-0.01) )
        self.box_normal = self.box.to_model()
        
        self.box =  soya.World(None)
        pyworlds.utils.Box(self.text_width*size,size*self.text_height,0,insert_into=self.box, material=m_red, origin = (0,1*size,-0.01) )
        self.box_selected = self.box.to_model()
        self.model = self.box_normal
        
        self.flat_follows = follows
        self.flat_offset = offset
        self.flat_size = size
        self.flat_compensation = compensation

        
    def advance_time(self,proportion):

        if self.flat_follows:
            self.move(self.flat_follows)
            maxparent = pyworlds.worlds.scene
            
            visible= self.flat_follows.visible
            objparent = self.flat_follows
            while objparent.is_inside(maxparent) and visible:
                if hasattr(objparent.parent,"parent") and hasattr(objparent.parent,"visible"):
                    objparent = objparent.parent

                    if objparent.visible == False: 
                        visible=False
                        break
                else:
                    break
                
            self.visible=visible
            self.solid=visible
            
        matrix = list(self.matrix)
        for x in range(3):
            for y in range(3):
                matrix[x+y*4] = pyworlds.worlds.camera.matrix[x+y*4]
        self.matrix = tuple(matrix)
        self.add_vector(soya.Vector(self,self.flat_offset[0],self.flat_offset[1],self.flat_offset[2]))
        vect = self.vector_to(pyworlds.worlds.camera)
        lenvect = vect.length()
        flat_compensation = self.flat_compensation
        if self.flat_compensation<0:
            len2 = lenvect + self.flat_compensation * 180.0 / pyworlds.worlds.camera.fov
            flat_compensation = len2 / float(lenvect)

            
        self.add_mul_vector( flat_compensation,self.vector_to(pyworlds.worlds.camera))
        
