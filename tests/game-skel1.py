#!/usr/bin/python 
import sys,os
sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), '..', 'src')))

import pyworlds.worlds as worlds
from pyworlds.worlds import sdlconst,soya
import soya.widget as widget


worlds.init()


class Level(soya.World):
        """A game level.
Level is a subclass of soya.World.
According to the game you are working on, you'll probably want to add
attributes and methods to the level class."""

def create_level():
			"""This function creates and saves the game skeleton demo level."""
			
			# Create a level object
			level = Level()
			
			# Separates static and non static parts
			# This will speed up network games, since only the non static part will be
			# sent on the network
			level_static = soya.World(level)
			
			# Load 3 materials (= textures) for files ./materials{grass|ground|snow}.data
			grass  = soya.Material.get("grass")
			ground = soya.Material.get("ground")
			snow   = soya.Material.get("snow")
			
			# Creates a terrain, from the heighmap "./images/map.png"
			# The terrain is in the static part (=level_static), because it won't change along the game.
			terrain = soya.Terrain(level_static)
			terrain.y = -65.0
			terrain.from_image(soya.Image.get("map_hfields2.jpg"))
			
			# Sets how high is the terrain
			terrain.multiply_height(200.0)
			
			# These values are trade of between quality and speed
			terrain.scale_factor = 3
			terrain.texture_factor = 0.05
			
			# Set the texture on the terrain, according to the height
			# (i.e. height 0.0 to 15.0 are textured with grass, ...)
			terrain.set_material_layer(grass,   0.0,  50.0)
			terrain.set_material_layer(ground, 40.0,  90.0)
			terrain.set_material_layer(snow,   80.0,  200.0)
			
			# Loads the model "./models/ferme.data"
			# This model has been created in Blender
			
			o_scene = worlds.scene
			worlds.scene = level_static
			# Adds 2 houses in the level
			
			house1 = worlds.Body("ferme")
			house1.set_xyz(250.0, -7.2, 182.0)
			house1.velocity.z = -0.1
			house1.rotation[1] = -1
			
			
			house2 = worlds.Body("ferme")
			house2.set_xyz(216.0, -11.25, 200.0)
			house2.rotate_y(100.0) # degrees
			
			# Creates a light in the level, similar to a sun (=a directional light)
			sun = soya.Light(level_static)
			sun.directional = 1
			sun.diffuse = (1.0, 0.8, 0.4, 1.0)
			sun.rotate_x(-45.0)
			
			# Creates a sky atmosphere, with fog
			atmosphere = soya.SkyAtmosphere()
			atmosphere.ambient = (0.3, 0.3, 0.4, 1.0)
			atmosphere.fog = 1
			atmosphere.fog_type  = 0
			atmosphere.fog_start = 50.0
			atmosphere.fog_end   = 500.0
			atmosphere.fog_color = atmosphere.bg_color = (0.2, 0.5, 0.7, 1.0)
			atmosphere.skyplane  = 1
			atmosphere.sky_color = (1.5, 1.0, 0.8, 1.0)
			
			# Set the atmosphere to the level
			level.atmosphere = atmosphere
			
			# Save the level as "./worlds/level_demo.data" (remember, levels are subclasses of worlds)
			level_static.filename = level.name = "level_demo_static"
			level_static.save()
			level.filename = level.name = "level_demo"
			level.save()

			worlds.scene = o_scene
        

# Now we just display the level



# This function must be called the first time you run game_skel.
# Then, you can comment it, since the level has been saved.
create_level()

# Loads the level, and put it in the scene
level = soya.World.get("level_demo")
worlds.scene.add(level)

worlds.camera.set_xyz(697.0,5.0,545.0)
worlds.camera.back = 500
worlds.enable_fps = True

def mainloop():
	pass
#	print worlds.camera.x,worlds.camera.y,worlds.camera.z
	

def renderloop(proportion):
	if sdlconst.K_UP in worlds.KEY:			worlds.camera.z -= 1 * proportion
	if sdlconst.K_DOWN in worlds.KEY:		worlds.camera.z += 1 * proportion
	if sdlconst.K_LEFT in worlds.KEY:		worlds.camera.x -= 1 * proportion
	if sdlconst.K_RIGHT in worlds.KEY:	worlds.camera.x += 1 * proportion
	if sdlconst.K_SPACE in worlds.KEY:	worlds.camera.y += .5 * proportion
	if sdlconst.K_LCTRL in worlds.KEY:	worlds.camera.y -= .5 * proportion
	
worlds.begin_loop(mainloop,renderloop)