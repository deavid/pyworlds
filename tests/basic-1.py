#!/usr/bin/python 

import worlds

worlds.init()

sword = worlds.load_body("sword")

sword.rotate_y(60.0)

worlds.begin_loop()