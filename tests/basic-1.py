#!/usr/bin/python 
import sys,os
sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), '..', 'src')))

import pyworlds.worlds as worlds

worlds.init()

sword = worlds.Body("sword")

sword.rotate_y(60.0)

worlds.begin_loop()