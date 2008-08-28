#!/usr/bin/python 
import worlds
from worlds import sdlconst,soya
worlds.init()

head = worlds.Body("caterpillar_head")

new_springfactor = springfactor = 0

pieces = {}
previous = head
for i in range(100):
	pieces[i] = worlds.FollowBody("caterpillar",previous)
	previous = pieces[i]

worlds.camera = soya.TravelingCamera(worlds.scene)

traveling = soya.ThirdPersonTraveling(pieces[5])
traveling.distance = 35.0
#traveling.offset_y = 20.0
#traveling.offset_y2 = 10.0

worlds.camera.add_traveling(traveling)
worlds.camera.speed = 0.05
vel = 0

def mainloop():
	global head, new_springfactor, springfactor, vel
	
	if sdlconst.K_UP in worlds.KEY: 		
		head.velocity.z=-vel
		#vel *= 1.001
		vel += .001
	else:
		head.velocity.z/=1.1
		vel = 0.2
	if sdlconst.K_DOWN in worlds.KEY:	
		head.velocity.z=0.2
	if sdlconst.K_LEFT in worlds.KEY:	head.rotation[1]+=1
	if sdlconst.K_RIGHT in worlds.KEY:	head.rotation[1]-=1
	
	head.rotation[1]/=1.05

	if sdlconst.K_1 in worlds.KEY:	new_springfactor=0
	if sdlconst.K_2 in worlds.KEY:	new_springfactor=50
	if sdlconst.K_3 in worlds.KEY:	new_springfactor=65
	if sdlconst.K_4 in worlds.KEY:	new_springfactor=75
	if sdlconst.K_5 in worlds.KEY:	new_springfactor=80
	if sdlconst.K_6 in worlds.KEY:	new_springfactor=85
	if sdlconst.K_7 in worlds.KEY:	new_springfactor=90
	if sdlconst.K_8 in worlds.KEY:	new_springfactor=95

	if new_springfactor != springfactor:
		global pieces
		for i in pieces:
			pieces[i].set_springfactor(new_springfactor)
		springfactor =	new_springfactor 
		
def renderloop(proportion):
	pass





worlds.begin_loop(mainloop, renderloop)


