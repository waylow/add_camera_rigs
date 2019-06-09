bl_info = {
  "name"       : "Add Camera Rigs",
  "author"     : "Wayne Dixon, Brian Raschko, Kris Wittig",
  "version"    : (1, 2),
  "blender"    : (2, 80, 0),
  "location"   : "View3D > Add > Camera > Dolly or Crane Rig",
  "description": "Adds a Camera Rig with UI",
  "warning"    : "Enable Auto Run Python Scripts in User Preferences > File",
  "wiki_url"   : "http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Rigging/Add_Camera_Rigs",
  "tracker_url": "https://developer.blender.org/maniphest/task/edit/form/2/",
  "category"   : "Camera"
}

import bpy
from   bpy.types import Panel
from   bpy.utils import register_class, unregister_class

class CameraRigs(Panel):

  bl_idname      = "CAMERARIGS_PT_CameraRigs"
  bl_label       = "Camera UI"
  bl_space_type  = 'VIEW_3D'
  bl_region_type = 'UI'

  _ACTIVE_OBJECT: object = None

  _ACTIVE_RIG_TYPE: str = None

  @classmethod
  def poll(this, context):

    this._ACTIVE_OBJECT = bpy.context.active_object

    if this._ACTIVE_OBJECT != None and "rig_id" in this._ACTIVE_OBJECT:

      rigType = this._ACTIVE_OBJECT["rig_id"]

      if rigType == "Dolly_Rig" or rigType == "Crane_Rig":

        this._ACTIVE_RIG_TYPE = rigType

        return True

    return False

  def draw(self, context):

    arm              = self._ACTIVE_OBJECT.data
    poseBones        = self._ACTIVE_OBJECT.pose.bones
    activeCameraName = self._ACTIVE_OBJECT.children[0].name

    cam = bpy.data.cameras[bpy.data.objects[activeCameraName].data.name]

    layout = self.layout.box().column()

    layout.label(text = "Clipping:")

    layout.prop(cam, "clip_start", text = "Start")
    layout.prop(cam, "clip_end"  , text = "End"  )
    layout.prop(cam, "type"                      )
    layout.prop(cam, "dof_object"                )

    if cam.dof_object is None:
      layout.operator("add.dof_object", text = "Add DOF Empty")
      layout.prop    (cam             , "dof_distance"        )

    # added the comp guides here
    layout.prop_menu_enum(cam                               , "show_guide" , text = "Compostion Guides"       )
    layout.prop          (bpy.data.objects[activeCameraName], "hide_select", text = "Make Camera Unselectable")

    layout.operator("add.marker_bind", text = "Add Marker and Bind")

    if bpy.context.scene.camera.name != activeCameraName:
      layout.operator("scene.make_camera_active", text = "Make Active Camera", icon = 'CAMERA_DATA')

    layout.prop(self._ACTIVE_OBJECT, 'show_x_ray', toggle = False, text = 'X Ray')

    layout.prop(cam, "show_limits"       )
    layout.prop(cam, "show_safe_areas"   )
    layout.prop(cam, "show_passepartout" )
    layout.prop(cam, "passepartout_alpha")

    # Camera Lens
    layout.label(             text = "Focal Length:")
    layout.prop (cam, "lens", text = "Angle"        )

    # Track to Constraint
    layout.label(                               text = "Tracking:"               )
    layout.prop (poseBones["CTRL"], '["Lock"]', text = "Aim Lock" , slider = True)

    if self._ACTIVE_RIG_TYPE == "Crane_Rig":

      layout = layout.box().column()

      # Crane arm stuff
      layout.label(                                            text = "Crane Arm:")
      layout.prop (poseBones["Height"   ], 'scale', index = 1, text = "Arm Height")
      layout.prop (poseBones["Crane_Arm"], 'scale', index = 1, text = "Arm Length")

  @staticmethod
  def addGeneratorButtons(panel, context):
    # Put "Build dolly / crane" buttons in Armature menu

    if context.mode == 'OBJECT':

      panel.layout.operator(BuildDollyRig.bl_idname, text = "Dolly Camera Rig", icon = 'CAMERA_DATA')
      panel.layout.operator(BuildCraneRig.bl_idname, text = "Crane Camera Rig", icon = 'CAMERA_DATA')

def register():
  register_class(CameraRigs)
  bpy.types.VIEW3D_MT_camera_add.append(CameraRigs.addGeneratorButtons)

def unregister():
  unregister_class(CameraRigs)
  bpy.types.VIEW3D_MT_camera_add.remove(CameraRigs.addGeneratorButtons)

if __name__ == "__main__": register()
