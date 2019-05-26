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
from bpy.types import Operator
from rna_prop_ui import rna_idprop_ui_prop_get
from math import radians


# =========================================================================
# Define the fuction to make the camera active
# =========================================================================
def set_scene_camera():
    ob = bpy.context.active_object
    # find the children on the rig (the camera name)
    active_cam = ob.children[0].name
    # cam = bpy.data.cameras[bpy.data.objects[active_cam]]
    scene_cam = bpy.context.scene.camera

    if active_cam != scene_cam.name:
        bpy.context.scene.camera = bpy.data.objects[active_cam]
    else:
        return None

class SetSceneCamera(Operator):
    '''Makes the camera parented to this rig the active scene camera'''
    bl_idname = "ADD_CAMERA_RIGS_OT_SetSceneCamera"
    bl_label = "Make Camera Active"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        set_scene_camera()
        return {'FINISHED'}

# =========================================================================
# Define function to add marker to timeline and bind camera
# =========================================================================
def markerBind():
    ob = bpy.context.active_object  # rig object
    active_cam = ob.children[0]  # camera object

    # switch area to timeline to add marker
    bpy.context.area.type = 'TIMELINE'
    # add marker
    bpy.ops.marker.add()
    bpy.ops.marker.rename(name="cam_" + str(bpy.context.scene.frame_current))
    # select rig camera
    bpy.context.scene.objects.active = active_cam
    # bind marker to selected camera
    bpy.ops.marker.camera_bind()
    # switch selected object back to the rig
    bpy.context.scene.objects.active = ob
    # switch back to 3d view
    bpy.context.area.type = 'VIEW_3D'

class AddMarkerBind(Operator):
    """Add marker to current frame then bind rig camera to it (for camera switching)"""
    bl_idname = "ADD_CAMERA_RIGS_OT_AddMarkerBind"
    bl_label = "Add marker and Bind Camera"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        markerBind()
        return {'FINISHED'}

# =========================================================================
# Define the function to add an Empty as DOF object
# =========================================================================
def add_DOF_object():
    smode = bpy.context.mode
    rig = bpy.context.active_object
    bone = rig.data.bones['AIM_child']
    active_cam = rig.children[0].name
    cam = bpy.data.cameras[bpy.data.objects[active_cam].data.name]

    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    # Add Empty
    bpy.ops.object.empty_add()
    obj = bpy.context.active_object

    obj.name = "Empty_DOF"
    # parent to AIM_Child
    obj.parent = rig
    obj.parent_type = "BONE"
    obj.parent_bone = "AIM_child"
    # clear loc and rot
    bpy.ops.object.location_clear()
    bpy.ops.object.rotation_clear()
    # move to bone head
    obj.location = bone.head

    # make this new empty the dof_object
    cam.dof_object = obj
    # reselect the rig
    bpy.context.scene.objects.active = rig
    obj.select = False
    rig.select = True

    bpy.ops.object.mode_set(mode=smode, toggle=False)

class AddDofObject(Operator):
    """Create empty and add as DOF Object"""
    bl_idname = "ADD_CAMERA_RIGS_OT_add.dof_object"
    bl_label = "Add DOF Object"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        add_DOF_object()
        return {'FINISHED'}


# =========================================================================
# This is the operator that will call all the functions and build the dolly rig
# =========================================================================
class BuildDollyRig(Operator):
    """Build a Camera Dolly Rig"""
    bl_idname = "ADD_CAMERA_RIGS_OT_BuildDollyRig"
    bl_label = "Build Dolly Camera Rig"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        # build the Widgets
        create_root_widget(self, "Camera_Root")
        create_camera_widget(self, "CTRL")
        create_aim_widget(self, "AIM")

        # call the function to build the rig
        build_dolly_rig(context)
        return {'FINISHED'}

# =========================================================================
# This is the operator that will call all the functions and build the crane rig
# =========================================================================
class BuildCraneRig(Operator):
    """Build a Camera Crane Rig"""
    bl_idname = "ADD_CAMERA_RIGS_OT_BuildCraneRig"
    bl_label = "Build Crane Camera Rig"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        # build the Widgets
        create_root_widget(self, "Camera_Root")
        create_camera_widget(self, "CTRL")
        create_aim_widget(self, "AIM")

        # call the function to build the rig
        build_crane_rig(context)
        return {'FINISHED'}

# =========================================================================
# Registration:
# =========================================================================
# dolly button in Armature menu
def add_dolly_button(self, context):
    if context.mode == 'OBJECT':
        self.layout.operator(
            BuildDollyRig.bl_idname,
            text="Dolly Camera Rig",
            icon='CAMERA_DATA')

# crane button in Armature menu
def add_crane_button(self, context):
    if context.mode == 'OBJECT':
        self.layout.operator(
            BuildCraneRig.bl_idname,
            text="Crane Camera Rig",
            icon='CAMERA_DATA')
''' Temp disabled this
def register():
    bpy.types.VIEW3D_MT_camera_add.append(add_dolly_button)
    bpy.types.VIEW3D_MT_camera_add.append(add_crane_button)

def unregister():
    bpy.types.VIEW3D_MT_camera_add.remove(add_dolly_button)
    bpy.types.VIEW3D_MT_camera_add.remove(add_crane_button)
'''

classes = (
    BuildDollyRig,
    BuildCraneRig,
    ADD_CAMERA_RIGS_PT_DollyCameraUI,
    ADD_CAMERA_RIGS_PT_CraneCameraUI,
    SetSceneCamera,
    AddMarkerBind,
    AddDofObject,
)

register, unregister = bpy.utils.register_classes_factory(classes)


if __name__ == "__main__":
    register()
