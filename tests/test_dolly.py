# SPDX-FileCopyrightText: 2026 Wayne Dixon
#
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
from pathlib import Path
import unittest

import bl_ext  # required to load add-on functions
import bpy

TEST_MODULE_PATH = 'bl_ext.test.add_camera_rigs'


def get_rig_and_cam(*args):
    return eval(TEST_MODULE_PATH).operators.get_rig_and_cam(*args)

def get_lens_without_breathing(*args):
    return eval(TEST_MODULE_PATH).operators.get_lens_without_breathing(*args)


class TestDollyCamera(unittest.TestCase):
    RIG_HAS_BREATHING = True

    @classmethod
    def setUpClass(cls):
        bpy.context.preferences.extensions.repos.new(
            name="Test",
            module="test",
            custom_directory=Path(__file__).parent.parent.parent.as_posix(),
        )
        bpy.ops.preferences.addon_enable(module=TEST_MODULE_PATH)

    def setUp(self):
        bpy.ops.wm.read_homefile()
        bpy.ops.object.build_camera_rig(mode='DOLLY')
        bpy.context.object.location = (0, -10, 0)

    def test_disable_enable(self):
        bpy.ops.preferences.addon_disable(module=TEST_MODULE_PATH)
        bpy.ops.preferences.addon_enable(module=TEST_MODULE_PATH)

    def test_lens_breathing(self):
        if not self.RIG_HAS_BREATHING:
            self.skipTest('Breathing not available/tested')
        
        rig, cam = get_rig_and_cam(bpy.context.object)
        lens_without_breathing = cam.data.lens
        rig.pose.bones["Camera"]["lens_breathing_scale"] = 0.5
        bpy.context.view_layer.update()
        self.assertLess(cam.data.lens, lens_without_breathing)

    def test_swap_lens(self):
        NEW_LENS_VALUE = 31.4
        ROUND_TO_DIGITS = 4

        rig, cam = get_rig_and_cam(bpy.context.object)
        prev_lens = get_lens_without_breathing(rig, cam)
        bpy.ops.add_camera_rigs.swap_lens(camera_lens=NEW_LENS_VALUE)
        new_lens = get_lens_without_breathing(rig, cam)
        assert new_lens != prev_lens
        self.assertNotAlmostEqual(new_lens, prev_lens, places=ROUND_TO_DIGITS)
        self.assertAlmostEqual(new_lens, NEW_LENS_VALUE, places=ROUND_TO_DIGITS)

    def test_set_dof(self):
        rig, cam = get_rig_and_cam(bpy.context.object)

        if self.RIG_HAS_BREATHING:
            rig.pose.bones["Camera"]["lens_breathing_scale"] = 1.0

        bpy.ops.add_camera_rigs.set_dof_bone()
        lens = cam.data.lens

        # updating the focus distance should not fail
        with self.assertNoLogs(
            logger=logging.getLogger('add_camera_rigs'),
            level=logging.ERROR
        ):
            bpy.ops.object.mode_set(mode='POSE')
            rig.pose.bones["Aim"].location.y -= 3.0
            bpy.ops.object.mode_set(mode='OBJECT')

        if self.RIG_HAS_BREATHING:
            self.assertLess(cam.data.lens, lens)

    def test_dolly_zoom(self):
        rig, cam = get_rig_and_cam(bpy.context.object)
        focal_length = get_lens_without_breathing(rig, cam)
        bpy.ops.add_camera_rigs.set_dolly_zoom()

        bpy.ops.object.mode_set(mode='POSE')
        rig.pose.bones["Camera"].location.y += 1.0
        bpy.context.view_layer.update()
        bpy.ops.object.mode_set(mode='OBJECT')

        updated_focal_length = get_lens_without_breathing(rig, cam)
        self.assertLess(updated_focal_length, focal_length)
        bpy.ops.add_camera_rigs.remove_dolly_zoom()
        self.assertAlmostEqual(get_lens_without_breathing(rig, cam), updated_focal_length)

    @classmethod
    def tearDownClass(cls):
        """Disable add-on"""
        import bpy
        bpy.ops.preferences.addon_disable(module=TEST_MODULE_PATH)

class TestDollyCameraRegression(TestDollyCamera):
    """Check rigs prior to lens breathing, for backwards compatibility."""

    RIG_HAS_BREATHING = False

    def setUp(self):
        v1_blendfile = (
            Path(__file__).parent / 'v1_test.blend'
        ).resolve().as_posix()
        bpy.ops.wm.open_mainfile(filepath=v1_blendfile)
