#!/usr/bin/python 
import sys,os
sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), '..', 'src')))

import pyworlds.worlds as w
from pyworlds.basics.body import *
from soya.sdlconst import *

w.init()

sword = PhysicsBody(mesh_file="sword")

sword.rotation[1]=90.0
sword.rotation[0]=17.0
sword.rotation[2]=3.0
w.camera.set_xyz(0,0,5)

def mainloop():
	global sword
	if K_UP in w.KEY: sword.rotation[0]+=10
	if K_DOWN in w.KEY: sword.rotation[0]-=10
	if K_LEFT in w.KEY: sword.rotation[1]+=10
	if K_RIGHT in w.KEY: sword.rotation[1]-=10
	if K_RSHIFT in w.KEY: sword.rotation[2]+=10
	if K_RCTRL in w.KEY: sword.rotation[2]-=10
	
	sword.rotation[0]/=1.05
	sword.rotation[1]/=1.05
	sword.rotation[2]/=1.05

w.begin_loop(callbackround=mainloop)
