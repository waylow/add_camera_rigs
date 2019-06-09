bl_info = {
    "name": "Add Camera Rigs",
    "author": "Wayne Dixon, Brian Raschko, Kris Wittig",
    "version": (1, 3),
    "blender": (2, 80, 0),
    "location": "View3D > Add > Camera > Dolly or Crane Rig",
    "description": "Adds a Camera Rig with UI",
    "warning": "Enable Auto Run Python Scripts in User Preferences > File",
    "tracker_url": "https://developer.blender.org/maniphest/task/edit/form/2/",
    "category": "Camera",
}

import bpy
import os

from . import build_rigs
from . import operators
from . import ui_panels
from . import prefs

# =========================================================================
# Registration:
# =========================================================================

def register():
    build_rigs.register()
    operators.register()
    ui_panels.register()
    prefs.register()


def unregister():
    build_rigs.unregister()
    operators.unregister()
    ui_panels.unregister()
    prefs.unregister()


if __name__ == "__main__":
    register()
