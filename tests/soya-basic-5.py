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


# basic-5: Event management : a keyboard-controlled caterpillar

# In this lesson, our caterpillar will obey you !
# You'll learn how to use SDL events with Soya.
# Use the cursor arrows to control the caterpillar.


# Import the Soya module.
# The soya.sdlconst module contains all the SDL constants.

import sys, os, os.path, soya, soya.sdlconst

soya.init()
soya.path.append(os.path.join(os.path.dirname(sys.argv[0]), "data"))

# Creates a scene.

scene = soya.World()


# The CaterpillarHead class is very similar to the CaterpillarHead class of the previous
# lesson.

class CaterpillarHead(soya.Body):
        def __init__(self, parent):
                soya.Body.__init__(self, parent, soya.Model.get("caterpillar_head"))
                self.speed                  = soya.Vector(self, 0.0, 0.0, 0.0)
                self.rotation_y_speed = 0.0
                
        def begin_round(self):
                soya.Body.begin_round(self)
                
                # Loops over all Soya / SDL events.
                # Each event is a tuple ; the first value indicates the event type and the other
                # values depend on the type. The following event types exist :
                #  - (KEYDOWN, keysym, modifier) where keysym is the key's code (a K_* constant)
                #    and modifier is a flag combining some of the MOD_* constant (to test the presence
                #    of a modifier, do e.g. for left shift: modifier & soya.sdlconst.MOD_LSHIFT).
                #  - (KEYUP, keysym, modifier)
                #  - (MOUSEMOTION, x, y, xrel, yrel) where x and y are the mouse coordinates (in
                #    pixel) ; xrel and yrel are the relative mouse coordinates (the difference since
                #    next mouse motion event).
                #  - (MOUSEBUTTONDOWN, button, x, y) where button is the mouse button number and
                #    x and y are the mouse coordinates. Mouse buttons are :
                #    - 1 : left
                #    - 2 : middle
                #    - 3 : right
                #    - 4 : roll up
                #    - 5 : roll down
                #  - (MOUSEBUTTONUP, button, x, y)
                #  - (JOYAXISMOTION, axis, value) XXX
                #  - (JOYBUTTONDOWN, button) XXX
                #  - (VIDEORESIZE, new_width, new_height)
                
                for event in soya.process_event():
                        
                        # Checks for key down (press) events.
                        
                        if event[0] == soya.sdlconst.KEYDOWN:
                                
                                # The up and down arrows set the caterpillar speed to a negative or positive value.
                                
                                if   event[1] == soya.sdlconst.K_UP:     self.speed.z = -0.2
                                elif event[1] == soya.sdlconst.K_DOWN:   self.speed.z =  0.1
                                
                                # The left and right arrow modify the rotation speed.
                                
                                elif event[1] == soya.sdlconst.K_LEFT:   self.rotation_y_speed =  10.0
                                elif event[1] == soya.sdlconst.K_RIGHT:  self.rotation_y_speed = -10.0
                                
                                # Pressing the escape or 'q' key will exit the main_loop mainloop, and thus terminate
                                # the program. soya.MAIN_LOOP.stop() is the right way to end your application, and
                                # causes the MainLoop.main_loop() method to return.
                                
                                elif event[1] == soya.sdlconst.K_q:      soya.MAIN_LOOP.stop()
                                elif event[1] == soya.sdlconst.K_ESCAPE: soya.MAIN_LOOP.stop()
                                
                        # Checks for key up (release) events.
                        
                        elif event[0] == soya.sdlconst.KEYUP:
                                
                                # When up or down arrows are released, the speed is set to zero.
                                
                                if   event[1] == soya.sdlconst.K_UP:     self.speed.z = 0.0
                                elif event[1] == soya.sdlconst.K_DOWN:   self.speed.z = 0.0
                                
                                # When left or right arrows are released, the rotation speed is set to zero.
                                
                                elif event[1] == soya.sdlconst.K_LEFT:   self.rotation_y_speed = 0.0
                                elif event[1] == soya.sdlconst.K_RIGHT:  self.rotation_y_speed = 0.0

                        elif event[0] == soya.sdlconst.QUIT:
                                soya.MAIN_LOOP.stop()
                                
                # Do the rotation.
                
                self.rotate_y(self.rotation_y_speed)
                
        def advance_time(self, proportion):
                soya.Body.advance_time(self, proportion)
                self.add_mul_vector(proportion, self.speed)


# CaterpillarPiece hasn't changed since the previous tutorial.

class CaterpillarPiece(soya.Body):
        def __init__(self, parent, previous):
                soya.Body.__init__(self, parent, soya.Model.get("caterpillar"))
                self.previous = previous
                self.speed = soya.Vector(self, 0.0, 0.0, -0.2)
                
        def begin_round(self):
                soya.Body.begin_round(self)
                self.look_at(self.previous)
                if self.distance_to(self.previous) < 1.5: self.speed.z =  0.0
                else:                                     self.speed.z = -0.2
                
        def advance_time(self, proportion):
                soya.Body.advance_time(self, proportion)
                self.add_mul_vector(proportion, self.speed)
                

# Creates a caterpillar head and 10 caterpillar piece of body.

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

camera = soya.Camera(scene)
camera.set_xyz(0.0, 15.0, 15.0)
camera.look_at(caterpillar_head)
soya.set_root_widget(camera)

soya.MainLoop(scene).main_loop()


 