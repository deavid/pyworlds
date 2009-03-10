#!/usr/bin/python 
import sys,os
sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), '..', 'src')))

import pyworlds.worlds as w
from pyworlds.basics.body import *
import soya

w.init()

head = PhysicsBody(mesh_file="sword")

head.rotation[1]=5.0
head.speed.z=-0.1

new_springfactor = springfactor = 16

pieces = {}
previous = head
for i in range(100):
	pieces[i] = w.FollowBody("sword",previous)
	previous = pieces[i]

w.camera.set_xyz(0,35,25)
w.camera.look_at(head)

def mainloop():
	global head, new_springfactor, springfactor
	if soya.sdlconst.K_UP in w.KEY: 		
		head.speed.z-=1; head.speed.z*=0.99
	else:
		head.speed.z/=1.1
	if soya.sdlconst.K_DOWN in w.KEY:	
		head.speed.z+=0.05; 
	if soya.sdlconst.K_LEFT in w.KEY:	head.rotation[1]+=200
	if soya.sdlconst.K_RIGHT in w.KEY:	head.rotation[1]-=200
	head.rotation[1]/=1.5

	if soya.sdlconst.K_1 in w.KEY:	new_springfactor=0.1
	if soya.sdlconst.K_2 in w.KEY:	new_springfactor=0.2
	if soya.sdlconst.K_3 in w.KEY:	new_springfactor=0.4
	if soya.sdlconst.K_4 in w.KEY:	new_springfactor=0.8
	if soya.sdlconst.K_5 in w.KEY:	new_springfactor=1.6
	if soya.sdlconst.K_0 in w.KEY:	new_springfactor=0

	if new_springfactor != springfactor:
		global pieces
		for i in pieces:
			pieces[i].set_springfactor(new_springfactor)
		
		new_springfactor = springfactor
		
def renderloop(proportion):
	global head
	w.camera.look_at(head) 
	pass





w.begin_loop(mainloop, renderloop)


