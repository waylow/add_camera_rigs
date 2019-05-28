bl_info = {
    "name": "Add Camera Rigs",
    "author": "Wayne Dixon, Kris Wittig",
    "version": (1, 2),
    "blender": (2, 80, 0),
    "location": "View3D > Add > Camera > Dolly or Crane Rig",
    "description": "Adds a Camera Rig with UI",
    "warning": "Enable Auto Run Python Scripts in User Preferences > File",
    "wiki_url": "http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Rigging/Add_Camera_Rigs",
    "tracker_url": "https://developer.blender.org/maniphest/task/edit/form/2/",
    "category": "Camera",
}


import bpy
import os

from . import build_rigs
from . import operators
from . import ui_panels

# =========================================================================
# Registration:
# =========================================================================

def register():
    bpy.utils.register_module(__name__)
    build_rigs.register()
    operators.register()
    ui_panels.register()


def unregister():
    bpy.utils.unregister_module(__name__)
    build_rigs.unregister()
    operators.unregister()
    ui_panels.unregister()
'''
if __name__ == "__main__":
    register()
'''
