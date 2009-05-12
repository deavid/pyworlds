#!/usr/bin/python 
import sys,os
sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), '..', 'src')))

import pyworlds.worlds as w
import pyworlds.basics.body as b
import pyworlds.basics.wbody as wb
import soya.sdlconst as c
import soya 

w.init()
rounds=0
diffuse1=[0.0, 0.3, 0.8, 1.00]

w.scene.atmosphere = soya.Atmosphere()
w.scene.atmosphere.bg_color = (1.0, 1.0, 1.0, 1.0)

material = soya.Material()
# Cellshaded materials in soya MUST have a texture.
material.texture = soya.Image.get("snow.png")
material.shininess = 0.5
material.diffuse   = tuple(diffuse1)
material.specular  = (0.2, 0.3, 0.6, 1.0)

material2 = soya.Material()
material2.texture = soya.Image.get("snow.png")
material2.shininess = 18
material2.diffuse   = (0.8,0.4, 0.0, 1.0)
material2.specular  = (0.3,0.0, 0.0, 1.0)



shader = soya.Material()
shader.texture = soya.Image.get("shader3.png")

cellshading = soya.CellShadingModelBuilder()

cellshading.shader              = shader
cellshading.outline_color       = (0.0, 0.0, 0.0, 0.5)
cellshading.outline_width       = 5.0
cellshading.outline_attenuation = 1.0



light2 = soya.Light(w.scene)
light2.set_xyz(22.0, 15.0, 0.0)

light3 = soya.Light(w.scene)
light3.set_xyz(-22.0, -20.0, 15.0)

box_model = soya.World(None)
box_model.model_builder = cellshading
w.Box(1,1,1,material=material,insert_into=box_model)
box_mesh = box_model.to_model()

box_model1 = soya.World(None)
box_model1.model_builder = cellshading
w.Box(1,1,1,material=material,insert_into=box_model1)
box_mesh1 = box_model1.to_model()



box_model2 = soya.World(None)
box_model2.model_builder = cellshading
w.Box(1,1,1,material=material2,insert_into=box_model2)
box_mesh2 = box_model2.to_model()


box1 = wb.wPhysicsBody(mesh=box_mesh)
box1.set_xyz(-2,0,-5)
box1.rotate_x(40)
box1.rotation[2]=20
box1.rotation[1]=5
box1.speed.y=-1

box2 = wb.wPhysicsBody(mesh=box_mesh)
box2.set_xyz(-1.5,0,-8)
box2.rotate_x(30)
box2.rotation[2]=50
box2.speed.y=-1


box3 = wb.wPhysicsBody(mesh=box_mesh)
box3.set_xyz(-1,0,-10)
box3.rotate_x(50)
box3.rotation[2]=30
box3.speed.y=-0.6

box4 = wb.wPhysicsBody(mesh=box_mesh)
box4.set_xyz(0,0,-12)
box4.rotate_x(60)
box4.rotation[2]=40
box4.speed.y=-0.5


        


label1 = wb.wLabel3DFlat(follows = box1, text = "Pabellon 1")

label2 = wb.wLabel3DFlat(follows = box2, text = "Pabellon 2")

label3 = wb.wLabel3DFlat(follows = box3, text = "Pabellon 3")

label4 = wb.wLabel3DFlat(follows = box4, text = "Pabellon 4")

#cursor = b.PhysicsBody(mesh=box_mesh2, parent=box1)



def game_logic():
    if c.K_a in w.KEY: w.camera.rotate_y(1)
    if c.K_s in w.KEY: w.camera.rotate_y(-1)
    
    if c.K_LEFT in w.KEY: w.camera.add_xyz(-.1,0,0)
    if c.K_RIGHT in w.KEY: w.camera.add_xyz(.1,0,0)
    if c.K_UP in w.KEY: w.camera.add_xyz(0,.1,0)
    if c.K_DOWN in w.KEY: w.camera.add_xyz(0,-.1,0)
    if c.K_RSHIFT in w.KEY: w.camera.add_xyz(0,0,.1)
    if c.K_RCTRL in w.KEY: w.camera.add_xyz(0,0,-.1)
    
    if 1 in w.MOUSE_BUTTON:
        button = w.MOUSE_BUTTON[1]
        box1.model = box_mesh1
        box2.model = box_mesh1
        box3.model = box_mesh1
        box4.model = box_mesh1
        mouse = w.camera.coord2d_to_3d(w.MOUSE_X, w.MOUSE_Y,-3)
        result = w.scene.raypick(w.camera, w.camera.vector_to(mouse))
        if result:
            impact, normal = result
            body_selected = impact.parent
            try:
                if body_selected.model == box_mesh1:
                    body_selected.model = box_mesh2
            except:
                pass            
            
        
        

def render_frame(proportion):
    global rounds, material
    diffuse1=[0,0,0,0]
    diffuse2=[0,0,0,0]
    rounds += proportion / 100.0
    import math
    diffuse1[0]=math.sin(rounds/10)/2+0.49
    diffuse1[1]=math.sin(rounds/3)/2+0.49
    diffuse1[2]=math.sin(rounds)/2+0.49
    material.diffuse   = tuple(diffuse1)

    diffuse2[0]=math.sin(rounds/10)/2+0.39
    diffuse2[1]=math.sin(rounds/6)/2+0.39
    diffuse2[2]=math.sin(rounds/2)/2+0.39
    material2.diffuse   = tuple(diffuse2)
    

w.begin_loop(callbackround=game_logic, callbackadvance=render_frame)
