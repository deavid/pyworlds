#!/usr/bin/python 
import sys,os,random
sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), '..', 'src')))
import soya 

"""import pyworlds.worlds as w
from pyworlds.basics.body import *
from soya.sdlconst import *

w.init(RPS=30,FPS=60)
w.enable_fps = True
class bSword(PhysicsBody):

    def swordloop(self,driver,t):
        body = driver.body
        body.rotation[0]/=1+0.50*t
        body.rotation[1]/=1+0.50*t
        body.rotation[2]/=1+0.50*t

        if K_UP in w.KEY: body.rotation[0]+=10
        if K_DOWN in w.KEY: body.rotation[0]-=10
        if K_LEFT in w.KEY: body.rotation[1]+=10
        if K_RIGHT in w.KEY: body.rotation[1]-=10
        if K_RSHIFT in w.KEY: body.rotation[2]+=10
        if K_RCTRL in w.KEY: body.rotation[2]-=10

    def initialize_vars(self):
        super(bSword,self).initialize_vars()
        
        self.physicsBDriver.userloop(self.swordloop)    



import random
"""
soya.init()
soya.path.append(os.path.join(os.path.dirname(sys.argv[0]), "data"))
scene = soya.World()

mesh = soya.Model.get("sword")
for n in range(1000):
#    sword = bSword(mesh_file="sword")
        
    sword =  soya.Body(scene,mesh)
#    sword.rotation[1]=random.randint(-90,90)
#    sword.rotation[0]=random.randint(-90,90)
#    sword.rotation[2]=random.randint(-90,90)
    sword.set_xyz(random.randint(-10,10),random.randint(-10,10),random.randint(-20,-10))
#    sword.set_timefactor(random.randint(5,50)/10.0)

light = soya.Light(scene)
light.set_xyz(0.5, 0.0, 2.0)
camera = soya.Camera(scene)
camera.z = 2.0
soya.set_root_widget(camera)
soya.MainLoop(scene).main_loop()

