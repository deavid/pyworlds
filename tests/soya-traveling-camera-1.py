#!/usr/bin/python 
# -*- indent-tabs-mode: t -*-

# Soya 3D tutorial
# Copyright (C) 2004 Jean-Baptiste LAMY
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


# traveling-camera-1: Traveling camera : a keyboard-controlled caterpillar, followed by the camera!

# In this lesson, our caterpillar will obey you !


# Import the Soya module.
# The soya.sdlconst module contains all the SDL constants.

import sys, os, os.path, soya, soya.sdlconst

soya.init()
soya.path.append(os.path.join(os.path.dirname(sys.argv[0]), "data"))

# Creates a scene.

scene = soya.World()


# The CaterpillarHead class is very similar to the CaterpillarHead class of the basic-*
# lessons.

class CaterpillarHead(soya.Body):
        def __init__(self, parent):
                soya.Body.__init__(self, parent, soya.Model.get("caterpillar_head"))
                self.speed                  = soya.Vector(self, 0.0, 0.0, 0.0)
                self.rotation_y_speed = 0.0
                
                # VERY IMPORTANT!
                #
                # The TravelingCamera use raypicking for determining through what the camera can go or not.
                # We thus have to DISABLE raypicking on the caterpillar itself!
                # This can be done by setting the caterpillar's solid attribute to 0.
                
                #self.solid = 0
                
        def begin_round(self):
                soya.Body.begin_round(self)
                
                for event in soya.process_event():
                        if event[0] == soya.sdlconst.KEYDOWN:
                                if   event[1] == soya.sdlconst.K_UP:     self.speed.z = -1.2
                                elif event[1] == soya.sdlconst.K_DOWN:   self.speed.z =  0.1
                                elif event[1] == soya.sdlconst.K_LEFT:   self.rotation_y_speed =  10.0
                                elif event[1] == soya.sdlconst.K_RIGHT:  self.rotation_y_speed = -10.0
                                elif event[1] == soya.sdlconst.K_q:      soya.MAIN_LOOP.stop()
                                elif event[1] == soya.sdlconst.K_ESCAPE: soya.MAIN_LOOP.stop()
                        
                        if event[0] == soya.sdlconst.KEYUP:
                                if   event[1] == soya.sdlconst.K_UP:     self.speed.z = 0.0
                                elif event[1] == soya.sdlconst.K_DOWN:   self.speed.z = 0.0
                                elif event[1] == soya.sdlconst.K_LEFT:   self.rotation_y_speed = 0.0
                                elif event[1] == soya.sdlconst.K_RIGHT:  self.rotation_y_speed = 0.0
                                
                self.rotate_y(self.rotation_y_speed)
                
        def advance_time(self, proportion):
                soya.Body.advance_time(self, proportion)
                self.add_mul_vector(proportion, self.speed)


class CaterpillarPiece(soya.Body):
        def __init__(self, parent, previous):
                soya.Body.__init__(self, parent, soya.Model.get("caterpillar"))
                self.previous = previous
                self.speed = soya.Vector(self, 0.0, 0.0, -0.2)
                
                # VERY IMPORTANT!
                #
                # See above.
                
                # self.solid = 0
                
        def begin_round(self):
                soya.Body.begin_round(self)
                self.look_at(self.previous)
                if self.distance_to(self.previous) < 1.5: self.speed.z =  0.0
                else:                                     self.speed.z = -1.2
                
        def advance_time(self, proportion):
                soya.Body.advance_time(self, proportion)
                self.add_mul_vector(proportion, self.speed)
                

caterpillar_head = CaterpillarHead(scene)
caterpillar_head.rotate_y(90.0)

previous_caterpillar_piece = caterpillar_head
for i in range(10):
        previous_caterpillar_piece = CaterpillarPiece(scene, previous_caterpillar_piece)
        previous_caterpillar_piece.x = i + 1
        
# Creates a light.

light = soya.Light(scene)
light.set_xyz(2.0, 5.0, 0.0)

# Creates a camera.

camera = soya.TravelingCamera(scene)

traveling = soya.ThirdPersonTraveling(caterpillar_head)
traveling.distance = 35.0

camera.add_traveling(traveling)
camera.speed = 0.1
camera.set_xyz(0.0, 35.0, 35.0)
camera.look_at(caterpillar_head)
soya.set_root_widget(camera)

soya.MainLoop(scene).main_loop()


 