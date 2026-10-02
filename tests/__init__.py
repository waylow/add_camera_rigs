# SPDX-FileCopyrightText: 2026 Wayne Dixon
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Utility file for running unittest with Blender executable."""

# you can run these tests in a terminal or shell script with:
# path/to/blender.exe --background --factory-startup --python tests/__init__.py

from pathlib import Path
import unittest


if __name__ == '__main__':
    loader = unittest.TestLoader()
    suite = loader.discover(Path(__file__).parent.as_posix())
    unittest.TextTestRunner(buffer=True).run(suite)