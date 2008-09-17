#!/usr/bin/python 
import sys,os
sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), '..', 'src')))

import pyworlds.worlds as w
from pyworlds.basics.body import *

w.init()

sword = PhysicsBody(mesh_file="sword")

sword.rotation[1]=90.0
sword.rotation[0]=17.0
sword.rotation[2]=3.0
w.camera.set_xyz(0,0,5)

w.begin_loop()
