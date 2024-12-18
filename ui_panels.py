# SPDX-FileCopyrightText: 2019 Wayne Dixon
#
# SPDX-License-Identifier: GPL-3.0-or-later

import bpy
from bpy.types import Menu, Panel

from .operators import get_rig_and_cam, poll_base


class CameraRigUIMixin():
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Item'

    @classmethod
    def poll(cls, context):
        return poll_base(cls, context)


class ADD_CAMERA_RIGS_MT_lens_ops(Menu):
    bl_label = "Camera Rig Lens Specials"

    def draw(self, context):
        active_object = context.active_object
        _rig, cam = get_rig_and_cam(active_object)
        cam_data = cam.data
        layout = self.layout

        drv = cam_data.animation_data.drivers[0]
        if drv.driver.expression == "lens":
            layout.operator("add_camera_rigs.set_dolly_zoom")
        else:
            layout.operator("add_camera_rigs.remove_dolly_zoom")

        layout.operator("add_camera_rigs.shift_to_pivot")
        layout.operator("add_camera_rigs.swap_lens")


class ADD_CAMERA_RIGS_PT_camera_rig_ui(Panel, CameraRigUIMixin):
    bl_label = "Camera Rig"

    def draw(self, context):
        active_object = context.active_object
        rig, cam = get_rig_and_cam(active_object)
        pose_bones = rig.pose.bones
        cam_data = cam.data
        layout = self.layout
        layout.use_property_split = True

        # Camera lens
        if rig["rig_id"].lower() in ("dolly_rig", "crane_rig"):
            col = layout.column(align=True)
            row = col.row(align=False)
            drv = cam_data.animation_data.drivers[0]
            if cam_data.type == 'ORTHO':
                row.prop(cam_data, "ortho_scale")
            elif drv.driver.expression == "lens":
                row.prop(pose_bones["Camera"], '["lens"]', text="Focal Length")
            else:
                row.prop(pose_bones["Camera"], '["lens_offset"]',
                        text="Lens Offset")
                sub = col.row(align=False)
                sub.enabled = False
                sub.prop(cam_data, "lens")
            row.menu("ADD_CAMERA_RIGS_MT_lens_ops", icon='DOWNARROW_HLT', text="")

            col = layout.column(align=True)
            col.prop(cam_data, "shift_x", text="Shift X")
            col.prop(cam_data, "shift_y", text="Y")

        # 2D rig stuff
        elif rig["rig_id"].lower() == "2d_rig":
            col = layout.column(align=True)
            col.prop(pose_bones["Camera"], '["rotation_shift"]',
                    text="Rotation/Shift")
            if cam.data.sensor_width != 36:
                col.label(text="Please set Camera Sensor Width to 36", icon="ERROR")

        sub = layout.column(align=True)
        sub.prop(cam_data, "clip_start", text="Clip Start")
        sub.prop(cam_data, "clip_end", text="End")

        layout.prop(cam_data, "type")


class ADD_CAMERA_RIGS_PT_camera_rig_ui_dof(Panel, CameraRigUIMixin):
    bl_label = "Depth of Field"
    bl_parent_id = "ADD_CAMERA_RIGS_PT_camera_rig_ui"

    def draw_header(self, context):
        active_object = context.active_object
        _rig, cam = get_rig_and_cam(active_object)

        layout = self.layout
        layout.prop(cam.data.dof, "use_dof", text="")

    def draw(self, context):
        active_object = context.active_object
        rig, cam = get_rig_and_cam(active_object)
        pose_bones = rig.pose.bones
        cam_data = cam.data
        layout = self.layout
        layout.use_property_split = True

        col = layout.column(align=False)
        col.active = cam_data.dof.use_dof
        if cam_data.dof.focus_object is None:
            col.operator("add_camera_rigs.set_dof_bone")
        sub = col.column(align=True)
        sub.prop(cam_data.dof, "focus_object", text="Focus on Object")
        if (cam_data.dof.focus_object is not None
                and cam_data.dof.focus_object.type == 'ARMATURE'):
            sub.prop_search(cam_data.dof, "focus_subtarget",
                            cam_data.dof.focus_object.data, "bones")

        row = col.row(align=True)
        row.active = cam_data.dof.focus_object is None
        row.prop(pose_bones["Camera"],
                '["focus_distance"]', text="Focus Distance")
        col.prop(pose_bones["Camera"],
                '["aperture_fstop"]', text="F-Stop")


class ADD_CAMERA_RIGS_PT_camera_rig_ui_viewport(Panel, CameraRigUIMixin):
    bl_label = "Viewport Display"
    bl_parent_id = "ADD_CAMERA_RIGS_PT_camera_rig_ui"

    def draw(self, context):
        active_object = context.active_object
        _rig, cam = get_rig_and_cam(active_object)
        cam_data = cam.data
        layout = self.layout
        layout.use_property_split = True

        col = layout.column(align=False, heading="Show")
        col.prop(active_object, 'show_in_front',
                    toggle=False, text='In Front')
        col.prop(cam_data, "show_limits", text="Limits")

        col = layout.column(align=False, heading="Passepartout")
        col.use_property_decorate = False
        row = col.row(align=True)
        sub = row.row(align=True)
        sub.prop(cam_data, "show_passepartout", text="")
        sub = sub.row(align=True)
        sub.active = cam_data.show_passepartout
        sub.prop(cam_data, "passepartout_alpha", text="")
        row.prop_decorator(cam_data, "passepartout_alpha")

        # Composition guides
        col.separator()
        col.popover(
            panel="ADD_CAMERA_RIGS_PT_composition_guides",
            text="Composition Guides",
        )


class ADD_CAMERA_RIGS_PT_camera_rig_ui_visibility(Panel, CameraRigUIMixin):
    bl_label = "Rig Properties"
    bl_parent_id = "ADD_CAMERA_RIGS_PT_camera_rig_ui"

    def draw(self, context):
        active_object = context.active_object
        rig, cam = get_rig_and_cam(active_object)
        pose_bones = rig.pose.bones
        layout = self.layout

        col = layout.column(align=True)
        col.prop(cam, "hide_select", text="Make Camera Unselectable")
        col.operator("add_camera_rigs.add_marker_bind",
                     text="Add Marker and Bind", icon="MARKER_HLT")
        col.operator("add_camera_rigs.set_scene_camera",
                     text="Make Camera Active", icon='CAMERA_DATA')

        if rig["rig_id"].lower() in ("dolly_rig", "crane_rig"):
            layout.use_property_split = True

            # Track to Constraint
            track_to_constraint = None
            for con in pose_bones["Camera"].constraints:
                if con.type == 'TRACK_TO':
                    track_to_constraint = con
                    break
            if track_to_constraint is not None:
                col = layout.column(align=True)
                col.prop(track_to_constraint, 'influence',
                         text="Aim Lock", slider=True)

            # Crane arm stuff
            if rig["rig_id"].lower() == "crane_rig":
                col = layout.column(align=True)
                col.prop(pose_bones["Crane_Height"],
                         'scale', index=1, text="Crane Arm Height")
                col.prop(pose_bones["Crane_Arm"],
                         'scale', index=1, text="Length")


def register():

    bpy.utils.register_class(ADD_CAMERA_RIGS_MT_lens_ops)
    bpy.utils.register_class(ADD_CAMERA_RIGS_PT_camera_rig_ui)
    bpy.utils.register_class(ADD_CAMERA_RIGS_PT_camera_rig_ui_dof)
    bpy.utils.register_class(ADD_CAMERA_RIGS_PT_camera_rig_ui_viewport)
    bpy.utils.register_class(ADD_CAMERA_RIGS_PT_camera_rig_ui_visibility)


def unregister():
    bpy.utils.unregister_class(ADD_CAMERA_RIGS_MT_lens_ops)
    bpy.utils.unregister_class(ADD_CAMERA_RIGS_PT_camera_rig_ui)
    bpy.utils.unregister_class(ADD_CAMERA_RIGS_PT_camera_rig_ui_dof)
    bpy.utils.unregister_class(ADD_CAMERA_RIGS_PT_camera_rig_ui_viewport)
    bpy.utils.unregister_class(ADD_CAMERA_RIGS_PT_camera_rig_ui_visibility)
