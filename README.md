Add_Camera_Rigs
===============

Blender Add-on which adds 2 rigs and UI into the Add >  Armature menu

Author: Wayne Dixon, Brian Raschko, Kris Wittig

Old Video Demo: https://vimeo.com/85884210
Old wikipage: http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Rigging/Add_Camera_Rigs
bugtracking: https://github.com/waylow/add_camera_rigs/issues



NOTES:
-I added the comp guides back
-the lens is now controlled by the rig and not the camera

==========
==TO DO:==
==========
-see if the devs can change it so you can use a bone to drive the focal_distance

Bugs:
-if the current collection is hidden it throws an error when you try to add a camera rig
-if the objects don't exist but the data does it gets out of sync with the naming
