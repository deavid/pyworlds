#!/usr/bin/python 

import sys,os
sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), '..', 'src')))

import pyworlds.worlds as worlds

ret=False
try:
	ret=worlds.is_pyWorlds_installed()
except:
	print "ERROR: pyWorlds doesn't seem to be installed on your system."

if ret:
	print "All seems to be ok."
else:
	print "Something has gone wrong"
