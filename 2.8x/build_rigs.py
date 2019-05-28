import bpy
from bpy.types import Operator
from rna_prop_ui import rna_idprop_ui_prop_get
from math import radians

# =========================================================================
# Define the function to build the Dolly Rig
# =========================================================================


def build_dolly_rig(context):
    # Define some useful variables:
    boneLayer = (False, True, False, False, False, False, False, False,
                 False, False, False, False, False, False, False, False,
                 False, False, False, False, False, False, False, False,
                 False, False, False, False, False, False, False, False)

    # Add the new armature object:
    bpy.ops.object.armature_add()
    rig = context.active_object

    # it will try to name the rig "Dolly_Rig" but if that name exists it will
    # add 000 to the name
    if "Dolly_Rig" not in context.scene.objects:
        rig.name = "Dolly_Rig"
    else:
        rig.name = "Dolly_Rig.000"
    rig["rig_id"] = "Dolly_Rig"

    bpy.ops.object.mode_set(mode='EDIT')

    # Remove default bone:
    bones = rig.data.edit_bones
    bones.remove(bones[0])

    # Add new bones:
    root = bones.new("Root")
    root.tail = (0.0, 0.0, -5.0)
    root.roll = radians(90)

    bpy.ops.object.mode_set(mode='EDIT')
    ctrlAimChild = bones.new("AIM_child")
    ctrlAimChild.head = (0.0, 5.0, 3.0)
    ctrlAimChild.tail = (0.0, 7.0, 3.0)
    ctrlAimChild.layers = boneLayer

    ctrlAim = bones.new("AIM")
    ctrlAim.head = (0.0, 5.0, 3.0)
    ctrlAim.tail = (0.0, 7.0, 3.0)

    ctrl = bones.new("CTRL")
    ctrl.head = (0.0, 0.0, 3.0)
    ctrl.tail = (0.0, 2.0, 3.0)

    # Setup hierarchy:
    ctrl.parent = root
    ctrlAim.parent = root
    ctrlAimChild.parent = ctrlAim

    # jump into pose mode and change bones to euler
    bpy.ops.object.mode_set(mode='POSE')
    for x in bpy.context.object.pose.bones:
        x.rotation_mode = 'XYZ'

    # jump into pose mode and add the custom bone shapes
    bpy.ops.object.mode_set(mode='POSE')
    bpy.context.object.pose.bones["Root"].custom_shape = bpy.data.objects[
        "WDGT_Camera_Root"]  # add the widget as custom shape
    # set the wireframe checkbox to true
    bpy.context.object.data.bones["Root"].show_wire = True
    bpy.context.object.pose.bones[
        "AIM"].custom_shape = bpy.data.objects["WDGT_AIM"]
    bpy.context.object.data.bones["AIM"].show_wire = True
    bpy.context.object.pose.bones["AIM"].custom_shape_transform = bpy.data.objects[
        rig.name].pose.bones["AIM_child"]  # sets the "At" field to the child
    bpy.context.object.pose.bones[
        "CTRL"].custom_shape = bpy.data.objects["WDGT_CTRL"]
    bpy.context.object.data.bones["CTRL"].show_wire = True

    # jump into object mode
    bpy.ops.object.mode_set(mode='OBJECT')

    # Add constraints to bones:
    con = rig.pose.bones['AIM_child'].constraints.new('COPY_ROTATION')
    con.target = rig
    con.subtarget = "CTRL"

    con = rig.pose.bones['CTRL'].constraints.new('TRACK_TO')
    con.target = rig
    con.subtarget = "AIM"
    con.use_target_z = True

    # Add custom Bone property to CTRL bone
    ob = bpy.context.object.pose.bones['CTRL']
    prop = rna_idprop_ui_prop_get(ob, "Lock", create=True)
    ob["Lock"] = 1.0
    prop["soft_min"] = prop["min"] = 0.0
    prop["soft_max"] = prop["max"] = 1.0

    # Add Driver to Lock/Unlock Camera from Aim Target
    rig = bpy.context.scene.objects.active
    pose_bone = bpy.data.objects[rig.name].pose.bones['CTRL']

    constraint = pose_bone.constraints["Track To"]
    inf_driver = constraint.driver_add('influence')
    inf_driver.driver.type = 'SCRIPTED'
    var = inf_driver.driver.variables.new()
    var.name = 'var'
    var.type = 'SINGLE_PROP'

    # Target the Custom bone property
    var.targets[0].id = bpy.data.objects[rig.name]
    var.targets[0].data_path = 'pose.bones["CTRL"]["Lock"]'
    inf_driver.driver.expression = 'var'

    # Add the camera object:
    bpy.ops.object.mode_set(mode='OBJECT')

    bpy.ops.object.camera_add(
        view_align=False, enter_editmode=False, location=(0, 0, 0), rotation=(0, 0, 0))
    cam = bpy.context.active_object

    # Name the Camera Object
    if 'Dolly_Camera' not in context.scene.objects:
        cam.name = "Dolly_Camera"
    else:
        cam.name = "Dolly_Camera.000"

    # this will name the camera Data Object
    if "Dolly_Camera" not in bpy.context.scene.objects.data.camera:
        cam.data.name = "Dolly_Camera"
    else:
        cam.data.name = "Dolly_Camera.000"

    cam_data_name = bpy.context.object.data.name
    bpy.data.cameras[cam_data_name].draw_size = 1.0
    cam.rotation_euler[0] = 1.5708  # rotate the camera 90 degrees in x
    cam.location = (0.0, -2.0, 0.0)  # move the camera to the correct postion
    cam.parent = rig
    cam.parent_type = "BONE"
    cam.parent_bone = "CTRL"

    # Add blank drivers to lock the camera loc, rot scale
    cam.driver_add('location', 0)
    cam.driver_add('location', 1)
    cam.driver_add('location', 2)
    cam.driver_add('rotation_euler', 0)
    cam.driver_add('rotation_euler', 1)
    cam.driver_add('rotation_euler', 2)
    cam.driver_add('scale', 0)
    cam.driver_add('scale', 1)
    cam.driver_add('scale', 2)

    # Set new camera as active camera
    bpy.context.scene.camera = cam

    # make sure the camera is selectable by default (this can be locked in the UI)
    bpy.context.object.hide_select = False

    # make the rig the active object before finishing
    bpy.context.scene.objects.active = rig
    cam.select = False
    rig.select = True

    return rig

# =========================================================================
# This is the operator that will call all the functions and build the dolly rig
# =========================================================================


class ADD_CAMERA_RIGS_OT_build_dolly_rig(Operator):
    """Build a Camera Dolly Rig"""
    bl_idname = "object.build_dolly_rig"
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
# Define the function to build the Crane Rig
# =========================================================================
def build_crane_rig(context):
    # Define some useful variables:
    boneLayer = (False, True, False, False, False, False, False, False,
                 False, False, False, False, False, False, False, False,
                 False, False, False, False, False, False, False, False,
                 False, False, False, False, False, False, False, False)

    # Add the new armature object:
    bpy.ops.object.armature_add()
    rig = context.active_object

    # it will try to name the rig "Dolly_Rig" but if that name exists it will
    # add .000 to the name
    if "Crane_Rig" not in context.scene.objects:
        rig.name = "Crane_Rig"
    else:
        rig.name = "Crane_Rig.000"
    rig["rig_id"] = "Crane_Rig"

    bpy.ops.object.mode_set(mode='EDIT')

    # Remove default bone:
    bones = rig.data.edit_bones
    bones.remove(bones[0])

    # Add new bones:
    root = bones.new("Root")
    root.tail = (0.0, 0.0, -5.0)

    ctrlAimChild = bones.new("AIM_child")
    ctrlAimChild.head = (0.0, 10.0, 1.0)
    ctrlAimChild.tail = (0.0, 12.0, 1.0)
    ctrlAimChild.layers = boneLayer

    ctrlAim = bones.new("AIM")
    ctrlAim.head = (0.0, 10.0, 1.0)
    ctrlAim.tail = (0.0, 12.0, 1.0)

    ctrl = bones.new("CTRL")
    ctrl.head = (0.0, 1.0, 1.0)
    ctrl.tail = (0.0, 3.0, 1.0)

    arm = bones.new("Crane_Arm")
    arm.head = (0.0, 0.0, 1.0)
    arm.tail = (0.0, 1.0, 1.0)

    height = bones.new("Height")
    height.head = (0.0, 0.0, 0.0)
    height.tail = (0.0, 0.0, 1.0)

    # Setup hierarchy:
    ctrl.parent = arm
    ctrl.use_inherit_rotation = False
    ctrl.use_inherit_scale = False

    arm.parent = height
    arm.use_inherit_scale = False

    height.parent = root
    ctrlAim.parent = root
    ctrlAimChild.parent = ctrlAim

    # change display to BBone: it just looks nicer
    bpy.context.object.data.draw_type = 'BBONE'
    # change display to wire for object
    bpy.context.object.draw_type = 'WIRE'

    # jump into pose mode and change bones to euler
    bpy.ops.object.mode_set(mode='POSE')
    for x in bpy.context.object.pose.bones:
        x.rotation_mode = 'XYZ'

    # lock the relevant loc, rot and scale
    bpy.context.object.pose.bones[
        "Crane_Arm"].lock_rotation = [False, True, False]
    bpy.context.object.pose.bones["Crane_Arm"].lock_scale = [True, False, True]
    bpy.context.object.pose.bones["Height"].lock_location = [True, True, True]
    bpy.context.object.pose.bones["Height"].lock_rotation = [True, True, True]
    bpy.context.object.pose.bones["Height"].lock_scale = [True, False, True]

    # add the custom bone shapes
    bpy.context.object.pose.bones["Root"].custom_shape = bpy.data.objects[
        "WDGT_Camera_Root"]  # add the widget as custom shape
    # set the wireframe checkbox to true
    bpy.context.object.data.bones["Root"].show_wire = True
    bpy.context.object.pose.bones[
        "AIM"].custom_shape = bpy.data.objects["WDGT_AIM"]
    bpy.context.object.data.bones["AIM"].show_wire = True
    bpy.context.object.pose.bones["AIM"].custom_shape_transform = bpy.data.objects[
        rig.name].pose.bones["AIM_child"]  # sets the "At" field to the child
    bpy.context.object.pose.bones[
        "CTRL"].custom_shape = bpy.data.objects["WDGT_CTRL"]
    bpy.context.object.data.bones["CTRL"].show_wire = True

    # jump into object mode
    bpy.ops.object.mode_set(mode='OBJECT')

    # Add constraints to bones:
    con = rig.pose.bones['AIM_child'].constraints.new('COPY_ROTATION')
    con.target = rig
    con.subtarget = "CTRL"

    con = rig.pose.bones['CTRL'].constraints.new('TRACK_TO')
    con.target = rig
    con.subtarget = "AIM"
    con.use_target_z = True

    # Add custom Bone property to CTRL bone
    ob = bpy.context.object.pose.bones['CTRL']
    prop = rna_idprop_ui_prop_get(ob, "Lock", create=True)
    ob["Lock"] = 1.0
    prop["soft_min"] = prop["min"] = 0.0
    prop["soft_max"] = prop["max"] = 1.0

    # Add Driver to Lock/Unlock Camera from Aim Target
    rig = bpy.context.scene.objects.active
    pose_bone = bpy.data.objects[rig.name].pose.bones['CTRL']

    constraint = pose_bone.constraints["Track To"]
    inf_driver = constraint.driver_add('influence')
    inf_driver.driver.type = 'SCRIPTED'
    var = inf_driver.driver.variables.new()
    var.name = 'var'
    var.type = 'SINGLE_PROP'

    # Target the Custom bone property
    var.targets[0].id = bpy.data.objects[rig.name]
    var.targets[0].data_path = 'pose.bones["CTRL"]["Lock"]'
    inf_driver.driver.expression = 'var'

    # Add the camera object:
    bpy.ops.object.mode_set(mode='OBJECT')

    bpy.ops.object.camera_add(
        view_align=False, enter_editmode=False, location=(0, 0, 0), rotation=(0, 0, 0))
    cam = bpy.context.active_object

    # this will name the Camera Object
    if 'Crane_Camera' not in context.scene.objects:
        cam.name = "Crane_Camera"
    else:
        cam.name = "Crane_Camera.000"

    # this will name the camera Data Object
    if "Crane_Camera" not in bpy.context.scene.objects.data.camera:
        cam.data.name = "Crane_Camera"
    else:
        cam.data.name = "Crane_Camera.000"

    cam_data_name = bpy.context.object.data.name
    bpy.data.cameras[cam_data_name].draw_size = 1.0
    cam.rotation_euler[0] = 1.5708  # rotate the camera 90 degrees in x
    cam.location = (0.0, -2.0, 0.0)  # move the camera to the correct postion
    cam.parent = rig
    cam.parent_type = "BONE"
    cam.parent_bone = "CTRL"
    # Add blank drivers to lock the camera loc, rot scale
    cam.driver_add('location', 0)
    cam.driver_add('location', 1)
    cam.driver_add('location', 2)
    cam.driver_add('rotation_euler', 0)
    cam.driver_add('rotation_euler', 1)
    cam.driver_add('rotation_euler', 2)
    cam.driver_add('scale', 0)
    cam.driver_add('scale', 1)
    cam.driver_add('scale', 2)

    # Set new camera as active camera
    bpy.context.scene.camera = cam

    # make sure the camera is selectable by default (this can be locked in the UI)
    bpy.context.object.hide_select = False

    # make the rig the active object before finishing
    bpy.context.scene.objects.active = rig
    cam.select = False
    rig.select = True

    return rig


# =========================================================================
# This is the operator that will call all the functions and build the crane rig
# =========================================================================
class ADD_CAMERA_RIGS_OT_build_crane_rig(Operator):
    """Build a Camera Crane Rig"""
    bl_idname = "object.build_crane_rig"
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


classes = (
    ADD_CAMERA_RIGS_OT_build_dolly_rig,
    ADD_CAMERA_RIGS_OT_build_crane_rig,
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
