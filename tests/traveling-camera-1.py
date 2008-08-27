#!/usr/bin/python 
import worlds
from worlds import soya 

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

worlds.camera.add_traveling(traveling)
worlds.camera.speed = 0.05

def mainloop():
	global head, new_springfactor, springfactor
	if soya.sdlconst.K_UP in worlds.KEY: 		
		head.velocity.z=-1
	else:
		head.velocity.z/=1.1
	if soya.sdlconst.K_DOWN in worlds.KEY:	
		head.velocity.z=0.5
	if soya.sdlconst.K_LEFT in worlds.KEY:	head.rotation[1]+=1
	if soya.sdlconst.K_RIGHT in worlds.KEY:	head.rotation[1]-=1
	
	head.rotation[1]/=1.05

	if soya.sdlconst.K_1 in worlds.KEY:	new_springfactor=0
	if soya.sdlconst.K_2 in worlds.KEY:	new_springfactor=50
	if soya.sdlconst.K_3 in worlds.KEY:	new_springfactor=65
	if soya.sdlconst.K_4 in worlds.KEY:	new_springfactor=75
	if soya.sdlconst.K_5 in worlds.KEY:	new_springfactor=80
	if soya.sdlconst.K_6 in worlds.KEY:	new_springfactor=85
	if soya.sdlconst.K_7 in worlds.KEY:	new_springfactor=90
	if soya.sdlconst.K_8 in worlds.KEY:	new_springfactor=95

	if new_springfactor != springfactor:
		global pieces
		for i in pieces:
			pieces[i].set_springfactor(new_springfactor)
		springfactor =	new_springfactor 
		
def renderloop(proportion):
	pass





worlds.begin_loop(mainloop, renderloop)


