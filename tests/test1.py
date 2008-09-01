#!/usr/bin/python 

import worlds

ret=False
try:
	ret=worlds.is_pyWorlds_installed()
except:
	print "ERROR: pyWorlds doesn't seem to be installed on your system."

if ret:
	print "All seems to be ok."
else:
	print "Something has gone wrong"
