#!/usr/bin/python 
#   The next 2 lines are only to tell python where are the sources for 
# PyWorlds modules. When you code your games probably you don't want these two.
import sys,os
sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), '..', 'src')))
# ---------------------

import pyworlds.worlds as w
import pyworlds.basics.body as wbody

w.init()

w.camera.set_xyz(-1,0,2)

sword = wbody.PhysicsBody(mesh_file="sword")
sword.rotate_y(90)
sword.rotation[2]=10

w.begin_loop()