import bpy


def set_scene_camera():
    '''Makes the camera the active and sets it to the scene camera'''
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
    bl_idname = "ADD_CAMERA_RIGS_OT_set_scene_camera"
    bl_label = "Make Camera Active"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        set_scene_camera()
        return {'FINISHED'}


def markerBind():
    '''Defines the function to add a marker to timeling and bind camera'''
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
    '''Add marker to current frame then bind rig camera to it (for camera switching)'''
    bl_idname = "ADD_CAMERA_RIGS_OT_add_marker_bind"
    bl_label = "Add Marker and Bind Camera"

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
    """Create Empty and add as DOF Object"""
    bl_idname = "ADD_CAMERA_RIGS_OT_add_dof_object"
    bl_label = "Add DOF Object"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        add_DOF_object()
        return {'FINISHED'}


classes = (
    ADD_CAMERA_RIGS_OT_set_scene_camera,
    ADD_CAMERA_RIGS_OT_add_marker_bind,
    ADD_CAMERA_RIGS_OT_add_dof_object,
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class
    for cls in classes:
        unregister_class(cls)


if __name__ == "__main__":
    register()
