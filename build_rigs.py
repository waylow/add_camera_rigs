# SPDX-FileCopyrightText: 2019 Wayne Dixon
#
# SPDX-License-Identifier: GPL-3.0-or-later

import bpy
from bpy.types import Operator
from bpy_extras import object_utils
from mathutils import Vector
from math import pi

from .create_widgets import (
    create_root_widget,
    create_camera_widget,
    create_camera_offset_widget,
    create_aim_widget,
    create_corner_widget,
    create_star_widget,
    create_cross_widget,
)


def create_prop_driver(rig, cam, prop_from, prop_to):
    """Create driver to a property on the rig"""
    driver = cam.data.driver_add(prop_to)
    driver.driver.type = 'SCRIPTED'
    var = driver.driver.variables.new()
    var.name = prop_from
    var.type = 'SINGLE_PROP'

    # Target the custom bone property
    var.targets[0].id = rig
    var.targets[0].data_path = 'pose.bones["Camera"]["%s"]' % prop_from
    driver.driver.expression = prop_from

    return driver


def create_dolly_bones(rig):
    """Create bones for the dolly camera rig"""
    bones = rig.data.edit_bones

    # Add new bones
    root = bones.new("Root")
    root.tail = (0.0, 1.0, 0.0)
    root.show_wire = True
    rig.data.collections.new(name="Controls")
    rig.data.collections['Controls'].assign(root)

    ctrl_aim_child = bones.new("MCH-Aim_shape_rotation")
    ctrl_aim_child.head = (0.0, 10.0, 1.7)
    ctrl_aim_child.tail = (0.0, 11.0, 1.7)
    # Create bone collection and assign bone
    rig.data.collections.new(name="MCH")
    rig.data.collections['MCH'].assign(ctrl_aim_child)
    rig.data.collections['MCH'].is_visible = False

    ctrl_aim = bones.new("Aim")
    ctrl_aim.head = (0.0, 10.0, 1.7)
    ctrl_aim.tail = (0.0, 11.0, 1.7)
    ctrl_aim.show_wire = True
    rig.data.collections['Controls'].assign(ctrl_aim)

    ctrl = bones.new("Camera")
    ctrl.head = (0.0, 0.0, 1.7)
    ctrl.tail = (0.0, 1.0, 1.7)
    ctrl.show_wire = True
    rig.data.collections['Controls'].assign(ctrl)

    ctrl_offset = bones.new("Camera_Offset")
    ctrl_offset.head = (0.0, 0.0, 1.7)
    ctrl_offset.tail = (0.0, 1.0, 1.7)
    ctrl_offset.show_wire = True
    rig.data.collections['Controls'].assign(ctrl_offset)


    # Setup hierarchy
    ctrl.parent = root
    ctrl_offset.parent = ctrl
    ctrl_aim.parent = root
    ctrl_aim_child.parent = ctrl_aim

    # Jump into object mode
    bpy.ops.object.mode_set(mode='OBJECT')
    pose_bones = rig.pose.bones
    # Lock the relevant scale channels of the Camera_offset bone
    pose_bones["Camera_Offset"].lock_scale = (True,) * 3


def create_crane_bones(rig):
    """Create bones for the crane camera rig"""
    bones = rig.data.edit_bones

    # Add new bones
    root = bones.new("Root")
    root.tail = (0.0, 1.0, 0.0)
    root.show_wire = True
    rig.data.collections.new(name="Controls")
    rig.data.collections['Controls'].assign(root)

    ctrl_aim_child = bones.new("MCH-Aim_shape_rotation")
    ctrl_aim_child.head = (0.0, 10.0, 1.7)
    ctrl_aim_child.tail = (0.0, 11.0, 1.7)
    rig.data.collections.new(name="MCH")
    rig.data.collections['MCH'].assign(ctrl_aim_child)
    rig.data.collections['MCH'].is_visible = False

    ctrl_aim = bones.new("Aim")
    ctrl_aim.head = (0.0, 10.0, 1.7)
    ctrl_aim.tail = (0.0, 11.0, 1.7)
    ctrl_aim.show_wire = True
    rig.data.collections['Controls'].assign(ctrl_aim)

    ctrl = bones.new("Camera")
    ctrl.head = (0.0, 1.0, 1.7)
    ctrl.tail = (0.0, 2.0, 1.7)
    rig.data.collections['Controls'].assign(ctrl)

    ctrl_offset = bones.new("Camera_Offset")
    ctrl_offset.head = (0.0, 1.0, 1.7)
    ctrl_offset.tail = (0.0, 2.0, 1.7)
    rig.data.collections['Controls'].assign(ctrl_offset)

    arm = bones.new("Crane_Arm")
    arm.head = (0.0, 0.0, 1.7)
    arm.tail = (0.0, 1.0, 1.7)
    rig.data.collections['Controls'].assign(arm)

    height = bones.new("Crane_Height")
    height.head = (0.0, 0.0, 0.0)
    height.tail = (0.0, 0.0, 1.7)
    rig.data.collections['Controls'].assign(height)

    # Setup hierarchy
    ctrl.parent = arm
    ctrl_offset.parent = ctrl
    ctrl.use_inherit_rotation = False
    ctrl.inherit_scale = "NONE"
    ctrl.show_wire = True

    arm.parent = height
    arm.inherit_scale = "NONE"

    height.parent = root
    ctrl_aim.parent = root
    ctrl_aim_child.parent = ctrl_aim

    # Jump into object mode
    bpy.ops.object.mode_set(mode='OBJECT')
    pose_bones = rig.pose.bones

    # Lock the relevant loc, rot and scale
    pose_bones["Crane_Arm"].lock_rotation = (False, True, False)
    pose_bones["Crane_Arm"].lock_scale = (True, False, True)
    pose_bones["Crane_Height"].lock_location = (True,) * 3
    pose_bones["Crane_Height"].lock_rotation = (True,) * 3
    pose_bones["Crane_Height"].lock_scale = (True, False, True)
    pose_bones["Camera_Offset"].lock_scale = (True,) * 3


def setup_3d_rig(rig, cam):
    """Finish setting up Dolly and Crane rigs"""
    # Jump into object mode and change bones to euler
    bpy.ops.object.mode_set(mode='OBJECT')
    pose_bones = rig.pose.bones
    for bone in pose_bones:
        bone.rotation_mode = 'XYZ'

    # Lens property
    pb = pose_bones['Camera']
    pb["lens"] = 50.0
    ui_data = pb.id_properties_ui("lens")
    ui_data.update(min=1.0, max=1000000.0, soft_max=5000.0, default=50.0, subtype="DISTANCE_CAMERA")

    # lens offset property
    pb = pose_bones['Camera']
    pb["lens_offset"] = 0.0
    ui_data = pb.id_properties_ui("lens_offset")
    ui_data.update(min=-1000000.0, max=1000000.0, soft_max = 5000.0, soft_min = -5000.0,default=0.0)

    # Build the widgets
    root_widget = create_root_widget("Camera_Root")
    camera_widget = create_camera_widget("Camera")
    camera_offset_widget = create_camera_offset_widget("Camera_Offset")
    aim_widget = create_aim_widget("Aim")

    # Add the custom bone shapes
    pose_bones["Root"].custom_shape = root_widget
    pose_bones["Aim"].custom_shape = aim_widget
    pose_bones["Camera"].custom_shape = camera_widget
    pose_bones["Camera_Offset"].custom_shape = camera_offset_widget

    # Set the "Override Transform" field to the mechanism position
    pose_bones["Aim"].custom_shape_transform = pose_bones["MCH-Aim_shape_rotation"]

    # Add constraints to bones
    con = pose_bones['MCH-Aim_shape_rotation'].constraints.new('COPY_ROTATION')
    con.target = rig
    con.subtarget = "Camera"

    con = pose_bones['Camera'].constraints.new('TRACK_TO')
    con.track_axis = 'TRACK_Y'
    con.up_axis = 'UP_Z'
    con.target = rig
    con.subtarget = "Aim"
    con.use_target_z = True

    cam.data.display_size = 1.0
    cam.rotation_euler[0] = pi / 2.0  # Rotate the camera 90 degrees in x

    drv = create_prop_driver(rig, cam, "lens", "lens")

    # create driver variables (for Dolly Zoom switching)
    var = drv.driver.variables.new()
    var.name = 'lens_offset'
    var.type = 'SINGLE_PROP'
    var.targets[0].id = rig
    var.targets[0].data_path = 'pose.bones["Camera"]["lens_offset"]'

    var = drv.driver.variables.new()
    var.name = 'distance'
    var.type = 'LOC_DIFF'
    var.targets[0].id = rig
    var.targets[0].bone_target = 'Camera'
    var.targets[1].id = rig
    var.targets[1].bone_target = 'Aim'

    var = drv.driver.variables.new()
    var.name = 'root_scale'
    var.type = 'TRANSFORMS'
    var.targets[0].id = rig
    var.targets[0].transform_type = 'SCALE_AVG'
    var.targets[0].bone_target = 'Root'


def create_2d_bones(rig, cam):
    """Create bones for the 2D camera rig"""
    bones = rig.data.edit_bones

    # Add bone collections
    collection_controls = rig.data.collections.new(name="Controls")
    collection_offsets = rig.data.collections.new(name="Offsets")
    collection_extras = rig.data.collections.new(name="Extras")
    collection_mch = rig.data.collections.new(name="MCH")
    collection_extras.is_visible = False
    collection_mch.is_visible = False

    # Add new bones
    bones = rig.data.edit_bones
    root = bones.new("Root")
    root.tail = (0.0, 0.0, 1.0)
    root.show_wire = True
    root.color.palette = 'THEME02'
    collection_controls.assign(root)

    ctrl_offset = bones.new("Camera_Offset")
    ctrl_offset.head = (0.0, 0.0, 1.7)
    ctrl_offset.tail = (0.0, 0.0, 2.7)
    ctrl_offset.show_wire = True
    ctrl_offset.color.palette = 'THEME04'
    collection_offsets.assign(ctrl_offset)

    ctrl_noise = bones.new("Noise")
    ctrl_noise.head = (0.0, 0.0, 1.7)
    ctrl_noise.tail = (0.0, 0.0, 2.7)
    ctrl_noise.show_wire = True
    ctrl_noise.color.palette = 'THEME09'
    collection_extras.assign(ctrl_noise)

    ctrl_camera = bones.new("Camera")
    ctrl_camera.head = (0.0, 0.0, 1.7)
    ctrl_camera.tail = (0.0, 0.0, 2.7)
    ctrl_camera.show_wire = True
    ctrl_camera.color.palette = 'THEME02'
    collection_controls.assign(ctrl_camera)

    ctrl_aim = bones.new("Aim")
    ctrl_aim.head = (0.0, 10.0, 1.7)
    ctrl_aim.tail = (0.0, 10.0, 2.7)
    ctrl_aim.show_wire = True
    ctrl_aim.color.palette = 'THEME04'
    collection_offsets.assign(ctrl_aim)

    left_corner = bones.new("Left_Corner")
    left_corner.head = (-3.0, 10.0, 0.0)
    left_corner.tail = left_corner.head + Vector((0.0, 0.0, 1.0))
    left_corner.show_wire = True
    left_corner.color.palette = 'THEME02'
    collection_controls.assign(left_corner)

    right_corner = bones.new("Right_Corner")
    right_corner.head = (3.0, 10.0, 0.0)
    right_corner.tail = right_corner.head + Vector((0.0, 0.0, 1.0))
    right_corner.show_wire = True
    right_corner.color.palette = 'THEME02'
    collection_controls.assign(right_corner)

    corner_distance_x = (left_corner.head - right_corner.head).length
    corner_distance_y = ctrl_camera.head.z - left_corner.head.z
    corner_distance_z = left_corner.head.y
    collection_controls.assign(root)

    center = bones.new("MCH-Center")
    center.head = ((right_corner.head + left_corner.head) / 2.0)
    center.tail = center.head + Vector((0.0, 0.0, 1.0))
    center.show_wire = True
    collection_mch.assign(center)

    dof = bones.new("DOF")
    dof.head = ctrl_aim.head
    dof.tail = ctrl_aim.tail
    dof.show_wire = True
    dof.color.palette = 'THEME09'
    collection_extras.assign(dof)

    dof_parent = bones.new("MCH-DOF_Parent")
    dof_parent.head = ctrl_aim.head
    dof_parent.tail = ctrl_aim.tail
    dof_parent.show_wire = True
    collection_mch.assign(dof_parent)

    # Setup hierarchy
    ctrl_offset.parent = root
    ctrl_noise.parent = ctrl_offset
    ctrl_camera.parent = ctrl_noise
    ctrl_aim.parent = ctrl_noise
    left_corner.parent = ctrl_aim
    right_corner.parent = ctrl_aim
    center.parent = ctrl_noise
    dof_parent.parent = root
    dof.parent = dof_parent

    # Jump into object mode and change bones to euler
    bpy.ops.object.mode_set(mode='OBJECT')
    pose_bones = rig.pose.bones
    for bone in pose_bones:
        bone.rotation_mode = 'XYZ'

    # Bone drivers
    center_drivers = pose_bones["MCH-Center"].driver_add("location")

    # Center X driver
    driver = center_drivers[0].driver
    driver.expression = "aim + (left + right) / 2.0"

    for corner in ("left", "right"):
        var = driver.variables.new()
        var.name = corner
        var.type = 'TRANSFORMS'
        var.targets[0].id = rig
        var.targets[0].bone_target = corner.capitalize() + "_Corner"
        var.targets[0].transform_type = 'LOC_X'
        var.targets[0].transform_space = 'TRANSFORM_SPACE'

    var = driver.variables.new()
    var.name = "aim"
    var.type = 'TRANSFORMS'
    var.targets[0].id = rig
    var.targets[0].bone_target = "Aim"
    var.targets[0].transform_type = 'LOC_X'
    var.targets[0].transform_space = 'TRANSFORM_SPACE'

    # Center Y driver
    driver = center_drivers[1].driver
    driver.expression = "({distance_x} - (left_x-right_x))*(res_y/res_x)/2 + aim_y + (left_y + right_y)/2".format(
        distance_x=corner_distance_x)

    for corner in ("left", "right"):
        for direction in ("x", "y"):
            var = driver.variables.new()
            var.name = "%s_%s" % (corner, direction)
            var.type = 'TRANSFORMS'
            var.targets[0].id = rig
            var.targets[0].bone_target = corner.capitalize() + "_Corner"
            var.targets[0].transform_type = 'LOC_' + direction.upper()
            var.targets[0].transform_space = 'TRANSFORM_SPACE'

    for direction in ("x", "y"):
        var = driver.variables.new()
        var.name = "aim_%s" % direction
        var.type = 'TRANSFORMS'
        var.targets[0].id = rig
        var.targets[0].bone_target = "Aim"
        var.targets[0].transform_type = 'LOC_' + direction.upper()
        var.targets[0].transform_space = 'TRANSFORM_SPACE'

    for direction in ("x", "y"):
        var = driver.variables.new()
        var.name = "res_" + direction
        var.type = 'CONTEXT_PROP'
        var.targets[0].context_property = 'ACTIVE_SCENE'
        var.targets[0].data_path = "render.resolution_" + direction

    # Center Z driver
    driver = center_drivers[2].driver
    driver.expression = "aim + (left + right) / 2.0"

    for corner in ("left", "right"):
        var = driver.variables.new()
        var.name = corner
        var.type = 'TRANSFORMS'
        var.targets[0].id = rig
        var.targets[0].bone_target = corner.capitalize() + "_Corner"
        var.targets[0].transform_type = 'LOC_Z'
        var.targets[0].transform_space = 'TRANSFORM_SPACE'

    var = driver.variables.new()
    var.name = "aim"
    var.type = 'TRANSFORMS'
    var.targets[0].id = rig
    var.targets[0].bone_target = "Aim"
    var.targets[0].transform_type = 'LOC_Z'
    var.targets[0].transform_space = 'TRANSFORM_SPACE'

    # Bone constraints
    center_con = pose_bones['Camera'].constraints.new('DAMPED_TRACK')
    center_con.target = rig
    center_con.subtarget = "MCH-Center"
    center_con.track_axis = 'TRACK_NEGATIVE_Z'

    dof_con = pose_bones["MCH-DOF_Parent"].constraints.new('COPY_LOCATION')
    dof_con.target = rig
    dof_con.subtarget = "MCH-Center"
    dof_con.target_space = 'POSE'
    dof_con.owner_space = 'POSE'

    # Build the widgets
    root_widget = create_root_widget("Camera_Root")
    camera_offset_widget = create_camera_offset_widget("Camera_Offset")
    noise_widget = create_star_widget("Noise", radius=0.48)
    camera_widget = create_camera_widget("Camera")
    aim_widget = create_aim_widget("Aim")
    left_widget = create_corner_widget("Left_Corner", reverse=True)
    right_widget = create_corner_widget("Right_Corner")
    dof_widget = create_cross_widget("DOF")

    # Add the custom bone shapes
    pose_bones["Root"].custom_shape = root_widget
    pose_bones["Camera_Offset"].custom_shape = camera_offset_widget
    pose_bones["Noise"].custom_shape = noise_widget
    pose_bones["Camera"].custom_shape = camera_widget
    pose_bones["Aim"].custom_shape = aim_widget
    pose_bones["Left_Corner"].custom_shape = left_widget
    pose_bones["Right_Corner"].custom_shape = right_widget
    pose_bones["DOF"].custom_shape = dof_widget

    # Set bone shape transforms
    pose_bones["Camera_Offset"].custom_shape_rotation_euler.x = pi / 2.0
    pose_bones["Camera"].custom_shape_rotation_euler.x = pi / 2.0
    pose_bones["Aim"].custom_shape_rotation_euler.x = pi / 2.0

    # Lock the relevant loc, rot and scale
    pose_bones["Root"].lock_scale = (True,) * 3
    pose_bones["Camera_Offset"].lock_scale = (True,) * 3
    pose_bones["Noise"].lock_scale = (True,) * 3
    pose_bones["Camera"].lock_rotation = (True,) * 3
    pose_bones["Camera"].lock_scale = (True,) * 3
    pose_bones["Aim"].lock_rotation = (True,) * 3
    pose_bones["Left_Corner"].lock_rotation = (True,) * 3
    pose_bones["Right_Corner"].lock_rotation = (True,) * 3

    # Camera settings

    cam.data.sensor_fit = "HORIZONTAL"  # Avoids distortion in portrait format
    cam.data.dof.focus_object = rig
    cam.data.dof.focus_subtarget = "DOF"

    # Property to switch between rotation and switch mode
    pose_bones["Camera"]["rotation_shift"] = 0.0
    ui_data = pose_bones["Camera"].id_properties_ui("rotation_shift")
    ui_data.update(min=0.0, max=1.0, description="rotation_shift")

    # Rotation / shift switch driver
    driver = center_con.driver_add('influence').driver
    driver.expression = '1 - rotation_shift'

    var = driver.variables.new()
    var.name = 'rotation_shift'
    var.type = 'SINGLE_PROP'
    var.targets[0].id = rig
    var.targets[0].data_path = 'pose.bones["Camera"]["rotation_shift"]'

    # Focal length driver
    driver = cam.data.driver_add("lens").driver
    driver.expression = "abs({distance_z} - (left_z + right_z)/2 - aim_z + cam_z) * 36 / frame_width".format(
        distance_z=corner_distance_z)

    var = driver.variables.new()
    var.name = 'frame_width'
    var.type = 'LOC_DIFF'
    var.targets[0].id = rig
    var.targets[0].bone_target = "Left_Corner"
    var.targets[0].transform_space = 'WORLD_SPACE'
    var.targets[1].id = rig
    var.targets[1].bone_target = "Right_Corner"
    var.targets[1].transform_space = 'WORLD_SPACE'

    for corner in ("left", "right"):
        var = driver.variables.new()
        var.name = corner + "_z"
        var.type = 'TRANSFORMS'
        var.targets[0].id = rig
        var.targets[0].bone_target = corner.capitalize() + '_Corner'
        var.targets[0].transform_type = 'LOC_Z'
        var.targets[0].transform_space = 'TRANSFORM_SPACE'

    var = driver.variables.new()
    var.name = "cam_z"
    var.type = 'TRANSFORMS'
    var.targets[0].id = rig
    var.targets[0].bone_target = "Camera"
    var.targets[0].transform_type = 'LOC_Z'
    var.targets[0].transform_space = 'TRANSFORM_SPACE'

    var = driver.variables.new()
    var.name = "aim_z"
    var.type = 'TRANSFORMS'
    var.targets[0].id = rig
    var.targets[0].bone_target = "Aim"
    var.targets[0].transform_type = 'LOC_Z'
    var.targets[0].transform_space = 'TRANSFORM_SPACE'

    # Orthographic scale driver
    driver = cam.data.driver_add("ortho_scale").driver
    driver.expression = "abs({distance_x} - (left_x - right_x))".format(distance_x=corner_distance_x)

    for corner in ("left", "right"):
        var = driver.variables.new()
        var.name = corner + "_x"
        var.type = 'TRANSFORMS'
        var.targets[0].id = rig
        var.targets[0].bone_target = corner.capitalize() + "_Corner"
        var.targets[0].transform_type = 'LOC_X'
        var.targets[0].transform_space = 'TRANSFORM_SPACE'

    # Shift driver X
    driver = cam.data.driver_add("shift_x").driver
    driver.expression = "rotation_shift * (((left_x + right_x)/2 + aim_x - cam_x) / frame_width)"

    var = driver.variables.new()
    var.name = 'rotation_shift'
    var.type = 'SINGLE_PROP'
    var.targets[0].id = rig
    var.targets[0].data_path = 'pose.bones["Camera"]["rotation_shift"]'

    var = driver.variables.new()
    var.name = 'frame_width'
    var.type = 'LOC_DIFF'
    var.targets[0].id = rig
    var.targets[0].bone_target = "Left_Corner"
    var.targets[0].transform_space = 'WORLD_SPACE'
    var.targets[1].id = rig
    var.targets[1].bone_target = "Right_Corner"
    var.targets[1].transform_space = 'WORLD_SPACE'

    for direction in ('x', 'z'):
        for corner in ('left', 'right'):
            var = driver.variables.new()
            var.name = '%s_%s' % (corner, direction)
            var.type = 'TRANSFORMS'
            var.targets[0].id = rig
            var.targets[0].bone_target = corner.capitalize() + '_Corner'
            var.targets[0].transform_type = 'LOC_' + direction.upper()
            var.targets[0].transform_space = 'TRANSFORM_SPACE'

    var = driver.variables.new()
    var.name = "aim_x"
    var.type = 'TRANSFORMS'
    var.targets[0].id = rig
    var.targets[0].bone_target = "Aim"
    var.targets[0].transform_type = 'LOC_X'
    var.targets[0].transform_space = 'TRANSFORM_SPACE'

    var = driver.variables.new()
    var.name = "cam_x"
    var.type = 'TRANSFORMS'
    var.targets[0].id = rig
    var.targets[0].bone_target = "Camera"
    var.targets[0].transform_type = "LOC_X"
    var.targets[0].transform_space = 'TRANSFORM_SPACE'

    # Shift driver Y
    driver = cam.data.driver_add('shift_y').driver
    driver.expression = (
        "rotation_shift * -("
        "({distance_y} - (left_y + right_y)/2 - aim_y + cam_y)"
        " / frame_width - (res_y/res_x)/2)"
    ).format(distance_y=corner_distance_y)

    var = driver.variables.new()
    var.name = 'rotation_shift'
    var.type = 'SINGLE_PROP'
    var.targets[0].id = rig
    var.targets[0].data_path = 'pose.bones["Camera"]["rotation_shift"]'

    var = driver.variables.new()
    var.name = 'frame_width'
    var.type = 'LOC_DIFF'
    var.targets[0].id = rig
    var.targets[0].bone_target = "Left_Corner"
    var.targets[0].transform_space = 'WORLD_SPACE'
    var.targets[1].id = rig
    var.targets[1].bone_target = "Right_Corner"
    var.targets[1].transform_space = 'WORLD_SPACE'

    for corner in ("left", "right"):
        var = driver.variables.new()
        var.name = "%s_y" % corner
        var.type = 'TRANSFORMS'
        var.targets[0].id = rig
        var.targets[0].bone_target = corner.capitalize() + "_Corner"
        var.targets[0].transform_type = 'LOC_Y'
        var.targets[0].transform_space = 'TRANSFORM_SPACE'

    var = driver.variables.new()
    var.name = "aim_y"
    var.type = 'TRANSFORMS'
    var.targets[0].id = rig
    var.targets[0].bone_target = "Aim"
    var.targets[0].transform_type = 'LOC_Y'
    var.targets[0].transform_space = 'TRANSFORM_SPACE'

    var = driver.variables.new()
    var.name = "cam_y"
    var.type = 'TRANSFORMS'
    var.targets[0].id = rig
    var.targets[0].bone_target = "Camera"
    var.targets[0].transform_type = 'LOC_Y'
    var.targets[0].transform_space = 'TRANSFORM_SPACE'

    for direction in ('x', 'y'):
        var = driver.variables.new()
        var.name = 'res_' + direction
        var.type = 'SINGLE_PROP'
        var.type = 'CONTEXT_PROP'
        var.targets[0].context_property = 'ACTIVE_SCENE'
        var.targets[0].data_path = 'render.resolution_' + direction


def build_camera_rig(context, mode):
    """Create stuff common to all camera rigs."""
    # Add the camera object
    cam_name = "%s_Camera" % mode.capitalize()
    cam_data = bpy.data.cameras.new(cam_name)
    cam = object_utils.object_data_add(context, cam_data, name=cam_name)
    context.scene.camera = cam

    # Add the rig object
    rig_name = mode.capitalize() + "_Rig"
    rig_data = bpy.data.armatures.new(rig_name)
    rig = object_utils.object_data_add(context, rig_data, name=rig_name)
    rig["rig_id"] = rig_name
    rig.location = context.scene.cursor.location

    bpy.ops.object.mode_set(mode='EDIT')

    # Add new bones and setup specific rigs
    if mode == "DOLLY":
        create_dolly_bones(rig)
        setup_3d_rig(rig, cam)
    elif mode == "CRANE":
        create_crane_bones(rig)
        setup_3d_rig(rig, cam)
    elif mode == "2D":
        create_2d_bones(rig, cam)

    # Parent the camera to the rig
    cam.location = (0.0, -1.0, 0.0)  # Move the camera to the correct position
    cam.parent = rig
    cam.parent_type = "BONE"
    cam.parent_bone = "Camera"

    # Change display to BBone: it just looks nicer
    rig.data.display_type = 'BBONE'
    # Change display to wire for object
    rig.display_type = 'WIRE'

    # Lock camera transforms
    cam.lock_location = (True,) * 3
    cam.lock_rotation = (True,) * 3
    cam.lock_scale = (True,) * 3

    # Add custom properties to the armature’s Camera bone,
    # so that all properties may be animated in a single action

    pose_bones = rig.pose.bones

    # DOF Focus Distance property
    pb = pose_bones['Camera']
    pb["focus_distance"] = 10.0
    ui_data = pb.id_properties_ui('focus_distance')
    ui_data.update(min=0.0, default=10.0)

    # DOF F-Stop property
    pb = pose_bones['Camera']
    pb["aperture_fstop"] = 2.8
    ui_data = pb.id_properties_ui('aperture_fstop')
    ui_data.update(min=0.0, soft_min=0.1, soft_max=128.0, default=2.8)

    # Add drivers to link the camera properties to the custom props
    # on the armature
    create_prop_driver(rig, cam, "focus_distance", "dof.focus_distance")
    create_prop_driver(rig, cam, "aperture_fstop", "dof.aperture_fstop")

    # Make the rig the active object
    view_layer = context.view_layer
    for obj in view_layer.objects:
        obj.select_set(False)
    rig.select_set(True)
    view_layer.objects.active = rig


class OBJECT_OT_build_camera_rig(Operator):
    bl_idname = "object.build_camera_rig"
    bl_label = "Build Camera Rig"
    bl_description = "Build a Camera Rig"
    bl_options = {'REGISTER', 'UNDO'}

    mode: bpy.props.EnumProperty(items=(('DOLLY', 'Dolly', 'Dolly rig'),
                                        ('CRANE', 'Crane', 'Crane rig',),
                                        ('2D', '2D', '2D rig')),
                                 name="mode",
                                 description="Type of camera to create",
                                 default="DOLLY")

    def execute(self, context):
        # Build the rig
        build_camera_rig(context, self.mode)
        return {'FINISHED'}


def add_dolly_crane_buttons(self, context):
    """Dolly and crane entries in the Add Object > Camera Menu"""
    if context.mode == 'OBJECT':
        self.layout.operator(
            OBJECT_OT_build_camera_rig.bl_idname,
            text="Dolly Camera Rig",
            icon='VIEW_CAMERA'
        ).mode = "DOLLY"

        self.layout.operator(
            OBJECT_OT_build_camera_rig.bl_idname,
            text="Crane Camera Rig",
            icon='VIEW_CAMERA'
        ).mode = "CRANE"

        self.layout.operator(
            OBJECT_OT_build_camera_rig.bl_idname,
            text="2D Camera Rig",
            icon='PIVOT_BOUNDBOX'
        ).mode = "2D"


classes = (
    OBJECT_OT_build_camera_rig,
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    bpy.types.VIEW3D_MT_camera_add.append(add_dolly_crane_buttons)


def unregister():
    from bpy.utils import unregister_class
    for cls in classes:
        unregister_class(cls)

    bpy.types.VIEW3D_MT_camera_add.remove(add_dolly_crane_buttons)


if __name__ == "__main__":
    register()
