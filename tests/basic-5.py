#!/usr/bin/python 
	
import worlds
import soya

worlds.init()

head = worlds.Body("caterpillar_head")

head.rotation[1]=5.0
head.velocity.z=-0.1

piece = {}
previous = head
for i in range(10):
	piece[i] = worlds.FollowBody("caterpillar",previous)
	previous = piece[i]

worlds.camera.set_xyz(0,15,15)
worlds.camera.look_at(head)

def mainloop():
	global head
	if soya.sdlconst.K_UP in worlds.KEY: 		head.velocity.z-=0.01
	if soya.sdlconst.K_DOWN in worlds.KEY:	head.velocity.z+=0.01
	if soya.sdlconst.K_LEFT in worlds.KEY:	head.rotation[1]+=1
	if soya.sdlconst.K_RIGHT in worlds.KEY:	head.rotation[1]-=1
	head.rotation[1]/=1.1
		
		
def renderloop(proportion):
	# worlds.camera.look_at(head) # This looks buggy





worlds.begin_loop(mainloop, renderloop)


