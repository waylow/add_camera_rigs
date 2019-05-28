import bpy


class ADD_CAMERA_RIGS_PT_DollyCameraUI(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "Dolly Camera UI"

    @classmethod
    def poll(self, context):
        try:
            ob = bpy.context.active_object
            return (ob["rig_id"] == "Dolly_Rig")
        except (AttributeError, KeyError, TypeError):
            return False

    def draw(self, context):
        layout = self.layout
        ob = bpy.context.active_object
        arm = context.active_object.data
        pose_bones = context.active_object.pose.bones
        # find the children on the rig (the camera name)
        active_cam = ob.children[0].name

        cam = bpy.data.cameras[bpy.data.objects[active_cam].data.name]
        box = layout.box()
        col = box.column()
        row = col.row()

        # Display Camera Properties
        col.label(text="Clipping:")
        col.prop(cam, "clip_start", text="Start")
        col.prop(cam, "clip_end", text="End")
        col.prop(cam, "type")
        col.prop(cam, "dof_object")
        if cam.dof_object is None:
            col.operator("add.dof_object", text="Add DOF Empty")
            col.prop(cam, "dof_distance")
        # added the comp guides here
        col.prop_menu_enum(cam, "show_guide", text="Compostion Guides")
        col.prop(bpy.data.objects[active_cam],
                 "hide_select", text="Make Camera Unselectable")
        col.operator("add.marker_bind", text="Add Marker and Bind")
        if bpy.context.scene.camera.name != active_cam:
            col.operator(
                "scene.make_camera_active", text="Make Active Camera", icon='CAMERA_DATA')
        col.prop(
            context.active_object, 'show_x_ray', toggle=False, text='X Ray')
        col.prop(cam, "show_limits")
        col.prop(cam, "show_safe_areas")
        col.prop(cam, "show_passepartout")
        col.prop(cam, "passepartout_alpha")

        # Camera Lens
        col.label(text="Focal Length:")
        col.prop(cam, "lens", text="Angle")

        # Track to Constraint
        col.label(text="Tracking:")
        col.prop(pose_bones["CTRL"], '["Lock"]', text="Aim Lock", slider=True)


class ADD_CAMERA_RIGS_OT_CraneCameraUI(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "Crane Camera UI"

    @classmethod
    def poll(self, context):
        try:
            ob = bpy.context.active_object
            return (ob["rig_id"] == "Crane_Rig")
        except (AttributeError, KeyError, TypeError):
            return False

    def draw(self, context):
        layout = self.layout
        ob = bpy.context.active_object
        arm = context.active_object.data
        pose_bones = context.active_object.pose.bones
        # find the children on the rig (camera)
        active_cam = ob.children[0].name
        cam = bpy.data.cameras[bpy.data.objects[active_cam].data.name]

        box = layout.box()
        col = box.column()
        row = col.row()

        # Display Camera Properties
        col.label(text="Clipping:")
        col.prop(cam, "clip_start", text="Start")
        col.prop(cam, "clip_end", text="End")
        col.prop(cam, "type")
        col.prop(cam, "dof_object")
        if cam.dof_object is None:
            col.operator("add.dof_object", text="Add DOF object")
            col.prop(cam, "dof_distance")
        # added the comp guides here
        col.prop_menu_enum(cam, "show_guide", text="Compostion Guides")
        col.prop(bpy.data.objects[active_cam],
                 "hide_select", text="Make Camera Unselectable")
        col.operator("add.marker_bind", text="Add Marker and Bind")
        if bpy.context.scene.camera.name != active_cam:
            col.operator(
                "scene.make_camera_active", text="Make Active Camera", icon='CAMERA_DATA')
        col.prop(
            context.active_object, 'show_x_ray', toggle=False, text='X Ray')
        col.prop(cam, "show_limits")
        col.prop(cam, "show_safe_areas")
        col.prop(cam, "show_passepartout")
        col.prop(cam, "passepartout_alpha")

        # Camera Lens
        col.label(text="Focal Length:")
        col.prop(cam, "lens", text="Angle")

        # Track to Constraint
        col.label(text="Tracking:")
        col.prop(pose_bones["CTRL"], '["Lock"]', text="Aim Lock", slider=True)

        # make this camera active if more than one camera exists
        '''if cam != bpy.context.scene.camera:
                col.op(, text="Make Active Camera", toggle=True)'''

        box = layout.box()
        col = box.column()
        row = col.row()

        # Crane arm stuff
        col.label(text="Crane Arm:")
        col.prop(pose_bones["Height"], 'scale', index=1, text="Arm Height")
        col.prop(pose_bones["Crane_Arm"], 'scale', index=1, text="Arm Length")


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


def register():
    bpy.types.VIEW3D_MT_camera_add.append(add_dolly_button)
    bpy.types.VIEW3D_MT_camera_add.append(add_crane_button)


def unregister():
    bpy.types.VIEW3D_MT_camera_add.remove(add_dolly_button)
    bpy.types.VIEW3D_MT_camera_add.remove(add_crane_button)
