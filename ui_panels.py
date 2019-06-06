import bpy
from bpy.types import Panel


class VIEW3D_PT_dolly_camera_ui(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "Dolly Camera UI"
    bl_category = "Camera Rig"

    @classmethod
    def poll(self, context):
        try:
            ob = bpy.context.active_object
            return (ob["rig_id"] == "Dolly_rig")
        except (AttributeError, KeyError, TypeError):
            return False

    def draw(self, context):
        layout = self.layout
        ob = bpy.context.active_object
        pose_bones = context.active_object.pose.bones
        # find the children on the rig (the camera name)
        active_cam = ob.children[0].name

        cam = bpy.data.cameras[bpy.data.objects[active_cam].data.name]
        box = layout.box()
        col = box.column()
        col.separator()

        # Display Camera Properties
        col.label(text="Clipping:")
        col.prop(cam, "clip_start", text="Start")
        col.prop(cam, "clip_end", text="End")
        col.prop(cam, "type")
        col.prop(cam.dof, "use_dof")
#        col.prop(cam, "dof_object")

#        if cam.dof_object is None:
#        col.operator("add.dof_empty", text="Add DOF Empty")
#        col.prop(cam, "dof_distance")
        # added the comp guides here
#        col.prop_menu_enum(cam, "show_guide", text="Compostion Guides")
        col.prop(bpy.data.objects[active_cam],
                 "hide_select", text="Make Camera Unselectable")

        col.operator("add.marker_bind", text="Add Marker and Bind")

        if bpy.context.scene.camera.name != active_cam:
            col.operator("scene.make_camera_active",
                         text="Make Active Camera", icon='CAMERA_DATA')

        col.prop(context.active_object,
                 'show_in_front', toggle=False, text='Show in front')
        col.prop(cam, "show_limits")
        col.prop(cam, "show_safe_areas")
        col.prop(cam, "show_passepartout")
        col.prop(cam, "passepartout_alpha")

        # Camera Lens
        col.label(text="Focal Length:")
        col.prop(cam, "lens", text="Angle")

        # Track to Constraint
        col.label(text="Tracking:")
        col.prop(pose_bones["Camera"], '["lock"]', text="Aim Lock", slider=True)


# =========================================================================
# This is the UI for the Crane Rig Camera
# =========================================================================
class VIEW3D_PT_crane_camera_ui(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "Crane Camera UI"
    bl_category = "Camera Rig"

    @classmethod
    def poll(self, context):
        try:
            ob = bpy.context.active_object
            return (ob["rig_id"] == "Crane_rig")
        except (AttributeError, KeyError, TypeError):
            return False

    def draw(self, context):
        layout = self.layout
        ob = bpy.context.active_object
        pose_bones = context.active_object.pose.bones
        # find the children on the rig (camera)
        active_cam = ob.children[0].name
        cam = bpy.data.cameras[bpy.data.objects[active_cam].data.name]

        box = layout.box()
        col = box.column()
        col.separator()

        # Display Camera Properties
        col.label(text="Clipping:")
        col.prop(cam, "clip_start", text="Start")
        col.prop(cam, "clip_end", text="End")
        col.prop(cam, "type")
#        col.prop(cam, "dof_object")
        ob = bpy.context.object
#        if cam.dof_object is None:
#           col.operator("add.dof_empty", text="Add DOF object")
#           col.prop(cam, "dof_distance")
        # added the comp guides here
#        col.prop_menu_enum(cam, "show_guide", text="Compostion Guides")
        col.prop(bpy.data.objects[active_cam],
                 "hide_select", text="Make Camera Unselectable")
        col.operator("add.marker_bind", text="Add Marker and Bind")

        if bpy.context.scene.camera.name != active_cam:
            col.operator(
                "scene.make_camera_active", text="Make Active Camera", icon='CAMERA_DATA')
        col.prop(
            context.active_object, 'show_in_front', toggle=False, text='Show in front')
        col.prop(cam, "show_limits")
        col.prop(cam, "show_safe_areas")
        col.prop(cam, "show_passepartout")
        col.prop(cam, "passepartout_alpha")

        # Camera Lens
        col.label(text="Focal Length:")
        col.prop(cam, "lens", text="Angle")

        # Track to Constraint
        col.label(text="Tracking:")
        col.prop(pose_bones["Camera"], '["lock"]', text="Aim Lock", slider=True)

        # make this camera active if more than one camera exists
        """
        if cam != bpy.context.scene.camera:
            col.op(, text="Make Active Camera", toggle=True)
        """

        box = layout.box()
        col = box.column()
        col.separator()

        # Crane arm stuff
        col.label(text="Crane Arm:")
        col.prop(pose_bones["Crane_height"], 'scale', index=1, text="Arm Height")
        col.prop(pose_bones["Crane_Arm"], 'scale', index=1, text="Arm Length")

# =========================================================================
# Registration:
# =========================================================================


classes = (
    VIEW3D_PT_dolly_camera_ui,
    VIEW3D_PT_crane_camera_ui,
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
