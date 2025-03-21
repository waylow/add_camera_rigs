# SPDX-FileCopyrightText: 2019 Wayne Dixon
#
# SPDX-License-Identifier: GPL-3.0-or-later

from bpy.types import AddonPreferences
from bpy.props import StringProperty


class AddCameraRigsPreferences(AddonPreferences):
    bl_idname = __package__

    # Widget prefix
    widget_prefix: StringProperty(
        name="Camera Widget prefix",
        description="Prefix for the widget objects",
        default="WGT-",
    )

    # Collection name
    camera_widget_collection_name: StringProperty(
        name="Bone Widget collection name",
        description="Name for the collection the widgets will appear",
        default="Widgets",
    )

    def draw(self, context):
        layout = self.layout

        col = layout.column()
        col.prop(self, "widget_prefix", text="Widget Prefix")
        col.prop(self, "camera_widget_collection_name", text="Collection name")


classes = (
    AddCameraRigsPreferences,
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class
    for cls in classes:
        unregister_class(cls)
