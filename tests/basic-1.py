#!/usr/bin/python 

import worlds

worlds.init()

sword = worlds.Body("sword")

sword.rotate_y(60.0)

worlds.begin_loop()