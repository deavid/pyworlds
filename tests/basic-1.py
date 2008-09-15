#!/usr/bin/python 
import sys,os
sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), '..', 'src')))

import pyworlds.worlds as worlds

worlds.init()

sword = worlds.Body("sword")

worlds.camera.set_xyz(0,0,5)
sword.rotate_y(60.0)

worlds.begin_loop()