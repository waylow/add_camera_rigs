Add_Camera_Rigs
===============

Blender Add-on which adds 2 rigs and UI into the Add >  Armature menu

Author: Wayne Dixon, Brian Raschko, Kris Wittig, Damien Picard

Old Video Demo: https://vimeo.com/85884210
Old wikipage: http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Rigging/Add_Camera_Rigs
bugtracking: https://github.com/waylow/add_camera_rigs/issues

[1.2]
-Updated most of the code to work with the 2.80 api
-spilt to code into modules, partially optimised it
-removed the composition guides as it is not functioning the same in 2.80

[1.3]
-added the composition guides back
-added drivers on the armature to control the focal length/focal distance and f-stop with the rig so you don't have to animate 2 objects.

[1.4]
-reoriented the Root control to match the world orientation.  (nicer to animate)
-edited the WDGT_camera_root code to reflect this change too
-added the GPL code block
-formatted some code neater (a few clean ups)

[1.4.3]
-Damien did a massive refactor of the code and added the 2d camera rig

[1.4.4]
-added an offset control for the camera

==========
==TO DO:==
==========
-see if the devs can open up access for the focal object to be a bone,  at the moment you have to create an empty and then parent this to the aim controller.

Bugs:
-if the current collection is hidden it throws an error when you try to add a camera rig
-if the objects don't exist but the data does it gets out of sync with the naming
