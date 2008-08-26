#!/usr/bin/python 

import worlds

worlds.init()

sword = worlds.Body("sword")

sword.rotation[1]=5.0

worlds.begin_loop()