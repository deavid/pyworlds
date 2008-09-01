#!/usr/bin/python 

import sys, os, os.path, soya

scene = None

meshes = {}

def is_pyWorlds_installed():
	print "pyWorlds seem to be installed and working."
	return True
	
	
def init(create_basic=True):
	global scene
	soya.init()
	soya.path.append(os.path.join(os.path.dirname(sys.argv[0]), "data"))
	scene = soya.World()
	if create_basic:
		init_basicscene()

def init_basicscene():
	global scene
	light = soya.Light(scene)
	light.set_xyz(5.0,0.0,20.0)

	camera = soya.Camera(scene)
	camera.z = 10.0

	soya.set_root_widget(camera)
	
def begin_loop():
	global scene
	soya.MainLoop(scene).main_loop()
	



def load_body(filename):
	global scene
	if filename in meshes:
		mesh = meshes[filename]
	else:
		mesh = soya.Model.get(filename)
		meshes[filename] = mesh
	
	body = soya.Body(scene,mesh)
	
	return body
	

