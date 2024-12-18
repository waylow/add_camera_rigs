# SPDX-FileCopyrightText: 2019 Wayne Dixon
#
# SPDX-License-Identifier: GPL-3.0-or-later

import bpy
from mathutils import Vector
from math import cos, sin, pi


def create_widget(name):
    """Create an empty widget object and return the object"""
    prefs = bpy.context.preferences.addons[__package__].preferences
    widget_prefix = prefs.widget_prefix
    obj_name = widget_prefix + name
    scene = bpy.context.scene

    obj = bpy.data.objects.get(obj_name)

    if obj is None:
        mesh = bpy.data.meshes.new(obj_name)
        obj = bpy.data.objects.new(obj_name, mesh)

        # Create a new collection for the widgets
        collection_name = prefs.camera_widget_collection_name
        coll = bpy.data.collections.get(collection_name)
        if coll is None:
            coll = bpy.data.collections.new(collection_name)
            scene.collection.children.link(coll)
            coll.hide_viewport = True
            coll.hide_render = True

        # Link the collection
        coll.objects.link(obj)

    return obj


def create_corner_widget(name, reverse=False):
    """Create a wedge-shaped widget"""
    obj = create_widget(name)
    if not obj.data.vertices:
        reverse = -1 if reverse else 1
        verts = (Vector((reverse * 0.0, 0.0, 0.0)),
                 Vector((reverse * 0.0, 1.0, 0.0)),
                 Vector((reverse * -0.1, 1.0, 0.0)),
                 Vector((reverse * -0.1, 0.1, 0.0)),
                 Vector((reverse * -1.0, 0.1, 0.0)),
                 Vector((reverse * -1.0, 0.0, 0.0)),
                 )
        edges = [(n, (n+1) % len(verts)) for n in range(len(verts))]

        mesh = obj.data
        mesh.from_pydata(verts, edges, ())
        mesh.update()
    return obj


def create_circle_widget(name, radius=1.0):
    """Create a circle-shaped widget"""
    obj = create_widget(name)
    if not obj.data.vertices:
        vert_n = 16
        verts = []
        for n in range(vert_n):
            angle = n / vert_n * 2*pi
            verts.append(Vector((cos(angle) * radius,
                                 0.0,
                                 sin(angle) * radius,
                                 )))
        edges = [(n, (n+1) % len(verts)) for n in range(len(verts))]

        mesh = obj.data
        mesh.from_pydata(verts, edges, ())
        mesh.update()
    return obj


def create_star_widget(name, radius=1.0):
    """Create a star-shaped widget"""
    obj = create_widget(name)
    if not obj.data.vertices:
        vert_n = 32
        verts = []
        for n in range(vert_n):
            angle = n / vert_n * 2*pi
            loc = Vector((cos(angle) * radius, sin(angle) * radius, 0.0))
            if n % 2:
                loc.length = radius * 0.83
            verts.append(loc)
        edges = [(n, (n+1) % len(verts)) for n in range(len(verts))]

        mesh = obj.data
        mesh.from_pydata(verts, edges, ())
        mesh.update()
    return obj


def create_root_widget(name):
    """Create a compass-shaped widget"""
    obj = create_widget(name)
    if not obj.data.vertices:
        verts = [(0.636, 0.636, 0.0),
                 (0.344, 0.831, 0.0),
                 (0.0, 0.9, 0.0),
                 (-0.344, 0.831, 0.0),
                 (-0.636, 0.636, 0.0),
                 (-0.831, 0.344, 0.0),
                 (-0.9, 0.0, 0.0),
                 (0.9, 0.0, 0.0),
                 (0.831, 0.344, 0.0),
                 (0.2, 1.52, 0.0),
                 (-0.2, 1.52, 0.0),
                 (-0.2, 1.15, 0.0),
                 (0.2, 1.15, 0.0),
                 (-0.4, 1.52, 0.0),
                 (0.4, 1.52, 0.0),
                 (0.0, 2.0, 0.0),
                 (-0.831, -0.344, 0.0),
                 (0.831, -0.344, 0.0),
                 (0.636, -0.636, 0.0),
                 (0.344, -0.831, 0.0),
                 (0.0, -0.9, 0.0),
                 (-0.344, -0.831, 0.0),
                 (-0.636, -0.636, 0.0),
                 (-2.0, 0.0, 0.0),
                 (-1.52, 0.4, 0.0),
                 (-1.52, -0.4, 0.0),
                 (-1.15, 0.2, 0.0),
                 (-1.15, -0.2, 0.0),
                 (-1.52, -0.2, 0.0),
                 (-1.52, 0.2, 0.0),
                 (1.52, -0.2, 0.0),
                 (1.52, 0.2, 0.0),
                 (1.15, 0.2, 0.0),
                 (1.15, -0.2, 0.0),
                 (1.52, 0.4, 0.0),
                 (1.52, -0.4, 0.0),
                 (2.0, 0.0, 0.0),
                 (0.0, -2.0, 0.0),
                 (-0.4, -1.52, 0.0),
                 (0.4, -1.52, 0.0),
                 (-0.2, -1.15, 0.0),
                 (0.2, -1.15, 0.0),
                 (0.2, -1.52, 0.0),
                 (-0.2, -1.52, 0.0)]

        edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (7, 8), (0, 8),
                 (10, 11), (9, 12), (11, 12), (10, 13), (9, 14), (13, 15), (14, 15),
                 (16, 22), (17, 18), (18, 19), (19, 20), (20, 21), (21, 22), (7, 17),
                 (6, 16), (23, 24), (23, 25), (24, 29), (25, 28), (26, 27), (26, 29),
                 (27, 28), (31, 32), (30, 33), (32, 33), (31, 34), (30, 35), (34, 36),
                 (35, 36), (37, 38), (37, 39), (38, 43), (39, 42), (40, 41), (40, 43),
                 (41, 42)]

        mesh = obj.data
        mesh.from_pydata(verts, edges, [])
        mesh.update()
    return obj


def create_camera_widget(name):
    """Create a camera control widget"""
    obj = create_widget(name)
    if not obj.data.vertices:
        verts = [(0.275, 0.0, -0.275), (0.360, 0.0, -0.149),
                 (0.389, 0.0, 0.0), (0.360, 0.0, 0.149),
                 (0.275, 0.0, 0.275), (0.149, 0.0, 0.360),
                 (0.0, 0.0, 0.389), (0.0, 0.0, -0.389),
                 (0.149, 0.0, -0.360), (0.663, 0.0, -0.093),
                 (0.663, 0.0, 0.093), (0.497, 0.0, 0.093),
                 (0.497, 0.0, -0.093), (0.663, 0.0, 0.173),
                 (0.663, 0.0, -0.173), (0.875, 0.0, 0.0),
                 (-0.149, 0.0, 0.360), (-0.149, 0.0, -0.360),
                 (-0.275, 0.0, -0.275), (-0.360, 0.0, -0.149),
                 (-0.389, 0.0, 0.0), (-0.360, 0.0, 0.149),
                 (-0.275, 0.0, 0.275), (0.0, 0.0, 0.875),
                 (0.173, 0.0, 0.663), (-0.173, 0.0, 0.663),
                 (0.093, 0.0, 0.497), (-0.093, 0.0, 0.497),
                 (-0.093, 0.0, 0.663), (0.093, 0.0, 0.663),
                 (-0.093, 0.0, -0.663), (0.093, 0.0, -0.663),
                 (0.093, 0.0, -0.497), (-0.093, 0.0, -0.497),
                 (0.173, 0.0, -0.663), (-0.173, 0.0, -0.663),
                 (0.0, 0.0, -0.875), (-0.875, 0.0, 0.0),
                 (-0.663, 0.0, 0.173), (-0.663, 0.0, -0.173),
                 (-0.497, 0.0, 0.093), (-0.497, 0.0, -0.093),
                 (-0.663, 0.0, -0.093), (-0.663, 0.0, 0.093)]

        edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (7, 8), (0, 8),
                 (10, 11), (9, 12), (11, 12), (10, 13), (9, 14), (13, 15), (14, 15),
                 (16, 22), (17, 18), (18, 19), (19, 20), (20, 21), (21, 22), (7, 17),
                 (6, 16), (23, 24), (23, 25), (24, 29), (25, 28), (26, 29), (27, 28),
                 (31, 32), (30, 33), (32, 33), (31, 34), (30, 35), (34, 36), (35, 36),
                 (37, 38), (37, 39), (38, 43), (39, 42), (40, 41), (40, 43), (41, 42),
                 (27, 26)]

        mesh = obj.data
        mesh.from_pydata(verts, edges, [])
        mesh.update()
    return obj


def create_aim_widget(name):
    """Create a camera aim widget"""
    obj = create_widget(name)
    if not obj.data.vertices:
        verts = [(0.311, 0.0, 0.311),
                 (0.406, 0.0, 0.168),
                 (0.44, 0.0, 0.0),
                 (0.406, 0.0, -0.168),
                 (0.311, 0.0, -0.311),
                 (0.168, 0.0, -0.406),
                 (0.0, 0.0, -0.44),
                 (0.0, 0.0, 0.44),
                 (0.168, 0.0, 0.406),
                 (0.8, 0.0, 0.1),
                 (0.8, 0.0, -0.1),
                 (1.0, 0.0, -0.1),
                 (1.0, 0.0, 0.1),
                 (0.8, 0.0, -0.2),
                 (0.8, 0.0, 0.2),
                 (0.56, 0.0, 0.0),
                 (-0.168, 0.0, -0.406),
                 (-0.168, 0.0, 0.406),
                 (-0.311, 0.0, 0.311),
                 (-0.406, 0.0, 0.168),
                 (-0.44, 0.0, 0.0),
                 (-0.406, 0.0, -0.168),
                 (-0.311, 0.0, -0.311),
                 (0.0, 0.0, 0.56),
                 (-0.2, 0.0, 0.8),
                 (0.2, 0.0, 0.8),
                 (-0.1, 0.0, 1.0),
                 (0.1, 0.0, 1.0),
                 (0.1, 0.0, 0.8),
                 (-0.1, 0.0, 0.8),
                 (0.1, 0.0, -0.8),
                 (-0.1, 0.0, -0.8),
                 (-0.1, 0.0, -1.0),
                 (0.1, 0.0, -1.0),
                 (-0.2, 0.0, -0.8),
                 (0.2, 0.0, -0.8),
                 (0.0, 0.0, -0.56),
                 (-0.56, 0.0, 0.0),
                 (-0.8, 0.0, -0.2),
                 (-0.8, 0.0, 0.2),
                 (-1.0, 0.0, -0.1),
                 (-1.0, 0.0, 0.1),
                 (-0.8, 0.0, 0.1),
                 (-0.8, 0.0, -0.1),
                 (-0.127, 0.0, -0.127),
                 (-0.166, 0.0, -0.068),
                 (-0.18, 0.0, 0.0),
                 (-0.166, 0.0, 0.068),
                 (-0.127, 0.0, 0.127),
                 (-0.068, 0.0, 0.166),
                 (-0.068, 0.0, -0.166),
                 (0.068, 0.0, 0.166),
                 (0.0, 0.0, 0.18),
                 (0.0, 0.0, -0.18),
                 (0.068, 0.0, -0.166),
                 (0.127, 0.0, -0.127),
                 (0.166, 0.0, -0.068),
                 (0.18, 0.0, 0.0),
                 (0.166, 0.0, 0.068),
                 (0.127, 0.0, 0.127),
                 (0.0, 0.0, 0.06),
                 (0.0, 0.0, -0.06),
                 (-0.06, 0.0, 0.0),
                 (0.06, 0.0, 0.0)]

        edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (7, 8), (0, 8),
                 (10, 11), (9, 12), (11, 12), (10, 13), (9, 14), (13, 15), (14, 15),
                 (16, 22), (17, 18), (18, 19), (19, 20), (20, 21), (21, 22), (7, 17),
                 (6, 16), (23, 24), (23, 25), (24, 29), (25, 28), (26, 29), (27, 28),
                 (31, 32), (30, 33), (32, 33), (31, 34), (30, 35), (34, 36), (35, 36),
                 (37, 38), (37, 39), (38, 43), (39, 42), (40, 41), (40, 43), (41, 42),
                 (50, 53), (49, 52), (44, 45), (45, 46), (46, 47), (47, 48), (48, 49),
                 (44, 50), (51, 59), (51, 52), (53, 54), (54, 55), (55, 56), (56, 57),
                 (57, 58), (58, 59), (27, 26), (60, 61), (62, 63)]

        mesh = obj.data
        mesh.from_pydata(verts, edges, [])
        mesh.update()
    return obj
