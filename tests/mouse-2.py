#!/usr/bin/python 
import sys,os
sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), '..', 'src')))

import pyworlds.worlds as w
import pyworlds.basics.body as b
import soya.sdlconst as c
import soya 

w.init()


material = soya.Material()
material.shininess = 0.5
material.diffuse   = (0.1, 0.2, 0.5, 1.0)
material.specular  = (0.2, 0.3, 0.6, 1.0)

material2 = soya.Material()
material2.shininess = 0.5
material2.diffuse   = (0.7,0.0, 0.2, 1.0)
material2.specular  = (1.0,0.2, 0.7, 1.0)



shader = soya.Material()
shader.texture = soya.Image.get("shader.png")

cellshading = soya.CellShadingModelBuilder()

cellshading.shader              = shader
cellshading.outline_color       = (0.0, 0.0, 0.0, 1.0)
cellshading.outline_width       = 7.0
cellshading.outline_attenuation = 1.0



box_model = soya.World(None)
w.Box(1,1,1,material=material,insert_into=box_model)
box_model.model_builder = cellshading
box_mesh = box_model.to_model()

box_model2 = soya.World(None)
w.Box(1,1,1,material=material2,insert_into=box_model2)
box_model2.model_builder = cellshading
box_mesh2 = box_model2.to_model()


box1 = b.PhysicsBody(mesh=box_mesh)
box1.set_xyz(-2,0,-5)
box1.rotate_x(40)
box1.rotation[2]=20
box1.speed.y=-1

box2 = b.PhysicsBody(mesh=box_mesh)
box2.set_xyz(-1.5,0,-8)
box2.rotate_x(30)
box2.rotation[2]=50
box2.speed.y=-1


box3 = b.PhysicsBody(mesh=box_mesh)
box3.set_xyz(-1,0,-10)
box3.rotate_x(50)
box3.rotation[2]=30
box3.speed.y=-0.6


box4 = b.PhysicsBody(mesh=box_mesh)
box4.set_xyz(0,0,-12)
box4.rotate_x(60)
box4.rotation[2]=40
box4.speed.y=-0.5



#cursor = b.PhysicsBody(mesh=box_mesh2, parent=box1)


def game_logic():
    if 1 in w.MOUSE_BUTTON:
        button = w.MOUSE_BUTTON[1]
        box1.model = box_mesh
        box2.model = box_mesh
        box3.model = box_mesh
        box4.model = box_mesh
        mouse = w.camera.coord2d_to_3d(w.MOUSE_X, w.MOUSE_Y,-3)
        result = w.scene.raypick(w.camera, w.camera.vector_to(mouse))
        if result:
            impact, normal = result
            body_selected = impact.parent
            body_selected.model = box_mesh2
            
        
        

    if c.K_0 in w.KEY: 
        box1.model = box_mesh
        box2.model = box_mesh
        box3.model = box_mesh
        box4.model = box_mesh

    if c.K_1 in w.KEY: 
        box1.model = box_mesh2
        box2.model = box_mesh
        box3.model = box_mesh
        box4.model = box_mesh

    if c.K_2 in w.KEY: 
        box1.model = box_mesh
        box2.model = box_mesh2
        box3.model = box_mesh
        box4.model = box_mesh

    if c.K_3 in w.KEY: 
        box1.model = box_mesh
        box2.model = box_mesh
        box3.model = box_mesh2
        box4.model = box_mesh

    if c.K_4 in w.KEY: 
        box1.model = box_mesh
        box2.model = box_mesh
        box3.model = box_mesh
        box4.model = box_mesh2



w.begin_loop(callbackround=game_logic)
