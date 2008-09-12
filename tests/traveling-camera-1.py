#!/usr/bin/python 
import worlds
from worlds import sdlconst,soya
worlds.init()

head = worlds.Body("sword")

new_springfactor = springfactor = 16

pieces = {}
previous = head
for i in range(100):
	pieces[i] = worlds.FollowBody("sword",previous)
	pieces[i].set_springfactor(new_springfactor)
	previous = pieces[i]

#worlds.camera = soya.TravelingCamera(worlds.scene)
#
#traveling = soya.ThirdPersonTraveling(pieces[5])
#traveling.distance = 35.0
#traveling.offset_y = 20.0
#traveling.offset_y2 = 10.0
worlds.camera.y=40
#worlds.camera.add_traveling(traveling)
#worlds.camera.speed = 0.05
vel = 0

def mainloop():
	global head, new_springfactor, springfactor, vel
	
	if sdlconst.K_UP in worlds.KEY: 		
		head.velocity.z=-vel*2
		#vel *= 1.001
		vel += .05
	else:
		head.velocity.z/=1.1
		vel = 2
	if sdlconst.K_DOWN in worlds.KEY:	
		head.velocity.z=0.2
	if sdlconst.K_LEFT in worlds.KEY:	head.rotation[1]+=vel+1
	if sdlconst.K_RIGHT in worlds.KEY:	head.rotation[1]-=vel+1
	
	head.rotation[1]/=1.05

	if sdlconst.K_1 in worlds.KEY:	new_springfactor=1
	if sdlconst.K_2 in worlds.KEY:	new_springfactor=2
	if sdlconst.K_3 in worlds.KEY:	new_springfactor=4
	if sdlconst.K_4 in worlds.KEY:	new_springfactor=8
	if sdlconst.K_5 in worlds.KEY:	new_springfactor=16
	if sdlconst.K_6 in worlds.KEY:	new_springfactor=32
	if sdlconst.K_7 in worlds.KEY:	new_springfactor=64
	if sdlconst.K_8 in worlds.KEY:	new_springfactor=80
	if sdlconst.K_0 in worlds.KEY:	new_springfactor=0

	if new_springfactor != springfactor:
		global pieces
		for i in pieces:
			pieces[i].set_springfactor(new_springfactor)
		springfactor =	new_springfactor 
		
def renderloop(proportion):
	global head
	worlds.look_at_elastic(worlds.camera, head, sqrt_from=360, factor=0.1)
	pass





worlds.begin_loop(mainloop, renderloop)


