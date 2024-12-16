Add Camera Rigs
../../_images/addons_camera_camera-rigs_ui.png
This add-on extends the functionality of a camera by creating control rigs with widgets and adds a panel to quickly access the camera’s settings from the 3D Viewport.

Activation
Open Blender and go to Preferences then the Add-ons tab.

Click Camera then Add Camera Rigs to enable the script.

Description
After activating the add-on, it will place three menu items in the Add ‣ Camera menu. They are Dolly Rig, Crane Rig and 2D Camera Rig.

The first two rigs are very similar except the “Crane Rig” has two extra adjustable bones (Arm Height and Arm Length) to make it easier to achieve a cinematic crane shot.

The 2D Camera Rig is mostly useful for 2D shots, when the camera is static and the action happens in front of it (like a theater stage).

Usage
Add a Add ‣ Camera ‣ Dolly Camera Rig, Crane Camera Rig or 2D Camera Rig. This will build the rig at the cursor location, add a new camera, making it the new active scene camera.

When the Rig is selected, the camera properties will be displayed in the Sidebar.

3D Rigs (Dolly & Crane)
Root Bone
This is the parent of the entire rig.

Control Bone
This is the bone (named Camera) that will translate the camera around. By default it will track to the aim bone.

Aim Bone
The camera will point at this bone (named Aim). You can also tilt the camera by rotating the aim on the Y axis.

2D Rig
This rig is designed to provide fine controls over the framing while aiming at one direction. With it, you can frame the action by moving two of the corners of the camera, instead of moving and rotating it. It produces smooth movements that would be hard to achieve without it, by using complex drivers to calculate the appropriate camera settings.

Root Bone
This is the parent of the entire rig. It is the only bone that you should rotate to aim approximately at the action.

Left_corner and Right_corner Bones
These are the most important bones in this rig. You can move them to quickly set and animate a framing. The camera will adjust its parameters to adapt to this framing (focal length, rotation / shift). They should always be at the same height (Y axis in the camera’s coordinate system).

Camera Bone
You can move the camera around, and it will compensate its settings to frame the two corners. For instance, if you leave the corners fixed on both sides of the subject and move the camera forward, you will achieve an efficient dolly zoom effect.

Modes
There are two modes of operation for the 2D rig: Rotation and Shift. You can switch between the two modes in the add-on’s interface.

Rotation is the default mode, and will rotate the camera to aim at and keep the corners in its frame. Shift mode, on the other hand, uses the Shift properties on the Camera to achieve a cropping effect instead of a pan.

Limitations
When moving the corners too far to the side in rotation mode, perspective makes the rig much less accurate.

Rotation mode is unsupported for orthographic cameras.

Interface
Widgets
When a rig is built, the add-on will create a collection for all the custom bone shapes (named Widgets). When the custom shapes (widgets) are built they will use the prefix WGT-. If you have more than one rig in the scene, it will use the same widgets in the same collection rather than duplicating them. The default collection name and the widget prefix can be set in the preferences of the add-on. (This will not change the name of any existing widgets or collection, only ones that are created after you change the setting.)

../../_images/addons_camera_camera-rigs_prefs.png
Panel
Reference

Mode:
All Modes

Panel:
3D Viewport ‣ Sidebar ‣ Item ‣ Camera Rig

The panel will display the most used camera settings. Only the added features will be explain here, for more information refer to the Cameras section.

Set DOF Bone
The Set DOF Bone button will automatically set up the camera so that it uses the camera rig’s Aim bone as a target for the depth of field (DOF).

Focal Distance/F-Stop/Focal Length
These are custom properties on the camera bone that drive the equivalent setting on the actual camera. This makes it animatable inside the armature object rather than having to animate the armature and the camera.

Show in Front
Will make the rig object visible through all other geometry. (Useful if you have a fly through scene or if other meshes are in the way.)

Lock Camera Select
The Lock Camera Select is a toggle button to make the camera unselectable (so you can’t accidentally delete it).

Tracking (Aim Lock)
This slider controls the Track To constraint on the control bone. Turn it off and the bone will not point to the aim bone anymore.

../../_images/addons_camera_camera-rigs_crane-arm.png
Crane Rig Height, Arm Length
The Arm Height and Arm Length sliders at the bottom of the UI show the Y axis scale of the relevant bone. By default, both the height and the arm length are at 1 unit in size. These values only show in the interface when a crane rig is selected, they are also animatable.

Rotation/Shift
The Rotation/Shift slider lets you switch between Rotation and Shift modes for the 2D Camera rig. You can also choose an intermediate value to have a bit of both.

Multiple Cameras
It is possible to add as many rigs as your scene needs. The Make Camera Active will appear if the camera attached to the selected rig is not the active camera. By pressing this, it will make this camera the active one.

Camera Switching
If you wish to switch cameras during an animation, you can do this with the Add Marker and Bind button. This uses Blender’s built-in camera binding tool to a Timeline marker. When pressed, it will add a marker to the Timeline and bind it to the camera controlled by the selected rig. Go to another frame, select a different camera rig and press it again. Now you have two markers and when you scrub the Timeline you will see the active camera switch accordingly. (Repeat this process as many times as needed). These markers can then also be dragged around in the Timeline to change the frame at which they will switch.

Troubleshooting
If the Aim tracking or 2D rig are not functioning, check that you have “Auto Run Python Scripts” enabled in the Preferences Preferences ‣ Save & Load ‣ Auto Run Python Scripts.

See also

The author’s Github repository.

A blog post explaining the 2D rig by its authors.
