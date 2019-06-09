import bpy
from bpy.types import Panel


class cameraRigs(Panel):
    bl_idname = "CAMERARIGS_PT_cameraRigs"
    bl_label = "Camera UI"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    _ACTIVE_OBJECT: object = None

    _ACTIVE_RIG_TYPE: str = None

    @classmethod
    def poll(self, context):
        self._ACTIVE_OBJECT = bpy.context.active_object

        if self._ACTIVE_OBJECT != None and "rig_id" in self._ACTIVE_OBJECT:
            rigType = self._ACTIVE_OBJECT["rig_id"]

            if rigType == "Dolly_Rig" or rigType == "Crane_Rig":
                self._ACTIVE_RIG_TYPE = rigType
                return True

        return False

    def draw(self, context):
        arm = self._ACTIVE_OBJECT.data
        poseBones = self._ACTIVE_OBJECT.pose.bones
        activeCameraName = self._ACTIVE_OBJECT.children[0].name

        cam = bpy.data.cameras[bpy.data.objects[activeCameraName].data.name]

        layout = self.layout.box().column()
        layout.label(text="Clipping:")
        layout.prop(cam, "clip_start", text="Start")
        layout.prop(cam, "clip_end", text="End")
        layout.prop(cam, "type")
        layout.prop(cam, "dof_object")

        if cam.dof_object is None:
            layout.operator("add.dof_object", text="Add DOF Empty")
            layout.prop(cam, "dof_distance")

        # added the comp guides here
        layout.prop_menu_enum(cam, "show_guide", text="Compostion Guides")
        layout.prop(bpy.data.objects[activeCameraName],
                    "hide_select", text="Make Camera Unselectable")

        layout.operator("add.marker_bind", text="Add Marker and Bind")

        if bpy.context.scene.camera.name != activeCameraName:
            layout.operator("scene.make_camera_active",
                            text="Make Active Camera", icon='CAMERA_DATA')

        layout.prop(self._ACTIVE_OBJECT, 'show_in_front', toggle=False, text='Show in front')
        layout.prop(cam, "show_limits")
        layout.prop(cam, "show_safe_areas")
        layout.prop(cam, "show_passepartout")
        layout.prop(cam, "passepartout_alpha")

        # Camera Lens
        layout.label(text="Focal Length:")
        layout.prop(cam, "lens", text="Angle")

        # Track to Constraint
        layout.label(text="Tracking:")
        layout.prop(poseBones["Camera"], '["lock"]', text="Aim Lock", slider=True)

        if self._ACTIVE_RIG_TYPE == "Crane_rig":
            layout = layout.box().column()

            # Crane arm stuff
            layout.label(text="Crane Arm:")
            layout.prop(poseBones["Crane_height"], 'scale', index=1, text="Arm Height")
            layout.prop(poseBones["Crane_Arm"], 'scale', index=1, text="Arm Length")


def register():
    bpy.utils.register_class(cameraRigs)


def unregister():
    bpy.utils.unregister_class(cameraRigs)
