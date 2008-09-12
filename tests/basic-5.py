#!/usr/bin/python 
import sys,os
sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), '..', 'src')))

import pyworlds.worlds as worlds
import soya

worlds.init()

head = worlds.Body("sword")

head.rotation[1]=5.0
head.velocity.z=-0.1

new_springfactor = springfactor = 0

pieces = {}
previous = head
for i in range(100):
	pieces[i] = worlds.FollowBody("sword",previous)
	previous = pieces[i]

worlds.camera.set_xyz(0,35,25)
worlds.camera.look_at(head)

def mainloop():
	global head, new_springfactor, springfactor
	if soya.sdlconst.K_UP in worlds.KEY: 		
		head.velocity.z-=0.05; head.velocity.z*=1.01
	else:
		head.velocity.z/=1.1
	if soya.sdlconst.K_DOWN in worlds.KEY:	
		head.velocity.z+=0.05; 
	if soya.sdlconst.K_LEFT in worlds.KEY:	head.rotation[1]+=1
	if soya.sdlconst.K_RIGHT in worlds.KEY:	head.rotation[1]-=1
	head.rotation[1]/=1.05

	if soya.sdlconst.K_1 in worlds.KEY:	new_springfactor=1
	if soya.sdlconst.K_2 in worlds.KEY:	new_springfactor=10
	if soya.sdlconst.K_3 in worlds.KEY:	new_springfactor=25
	if soya.sdlconst.K_4 in worlds.KEY:	new_springfactor=50
	if soya.sdlconst.K_5 in worlds.KEY:	new_springfactor=75
	if soya.sdlconst.K_0 in worlds.KEY:	new_springfactor=0

	if new_springfactor != springfactor:
		global pieces
		for i in pieces:
			pieces[i].set_springfactor(new_springfactor)
		
		new_springfactor = springfactor
		
def renderloop(proportion):
	pass
	# worlds.camera.look_at(head) # This looks buggy





worlds.begin_loop(mainloop, renderloop)


