#!/usr/bin/python 
import sys,os
sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), '..', 'src')))

import pyworlds.worlds as w
import pyworlds.basics.body as b
import soya.sdlconst as c
import soya 

w.init()

sword = b.PhysicsBody(mesh_file="sword")


def game_logic():
    global sword
    mouse = w.camera.coord2d_to_3d(w.MOUSE_X, w.MOUSE_Y,-3)
    sword.move(mouse)


@sword.addloopcall
def swordloop(t):
    if t==0: return 0;	

    if c.K_UP in w.KEY: sword.rotation[0]+=200*t
    if c.K_DOWN in w.KEY: sword.rotation[0]-=200*t
    if c.K_LEFT in w.KEY: sword.rotation[1]+=200*t
    if c.K_RIGHT in w.KEY: sword.rotation[1]-=200*t
    if c.K_RSHIFT in w.KEY: sword.rotation[2]+=200*t
    if c.K_RCTRL in w.KEY: sword.rotation[2]-=200*t

    sword.rotation[0]/=1+0.50*t
    sword.rotation[1]/=1+0.50*t
    sword.rotation[2]/=1+0.50*t
    return t


w.begin_loop(callbackround=game_logic)
