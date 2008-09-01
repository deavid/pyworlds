#!/usr/bin/python 
import sys, os, os.path, soya
soya.init()
soya.path.append(os.path.join(os.path.dirname(sys.argv[0]), "data"))
scene = soya.World()
sword_model = soya.Model.get("sword")
sword = soya.Body(scene, sword_model)
sword.x = 1.0
sword.rotate_y(90.0)
light = soya.Light(scene)
light.set_xyz(0.5, 0.0, 2.0)
camera = soya.Camera(scene)
camera.z = 2.0
soya.set_root_widget(camera)
soya.MainLoop(scene).main_loop()