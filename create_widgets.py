is notimport bpy


def create_widget(self, name):
    """ Creates an empty widget object and returns the object."""
    widget_prefix = bpy.context.preferences.addons["add_camera_rigs"].preferences.widget_prefix
    obj_name = widget_prefix + name
    scene = bpy.context.scene

    mesh = bpy.data.meshes.new(obj_name)
    obj = bpy.data.objects.new(obj_name, mesh)

    # create a new collection for the wigets
    collection_name = bpy.context.preferences.addons["add_camera_rigs"].preferences.camera_widget_collection_name
    c = bpy.data.collections.get(collection_name)
    if c is not None:
        c.objects.link(obj)
    else:
        c = bpy.data.collections.new(collection_name)
        c.hide_viewport = True
        c.hide_render = True

        # link the collection
        scene.collection.children.link(c)
        c.objects.link(obj)

    return obj


def create_root_widget(self, name):
    # Creates a compass-shaped widget
    obj = create_widget(self, name)
    if obj is not None:
        verts = [(0.210255, 0.209045, 0), (0.113789, 0.273501, -2.98023e-08),
                 (-3.07015e-08, 0.296135, 0), (-0.113789, 0.273501, 0),
                 (-0.210255, 0.209045, 0), (-0.274712, 0.112579, 7.45058e-09),
                 (-0.297346, -0.00121052, 1.48165e-08), (0.297346, -0.00121046, -1.49858e-08),
                 (0.274711, 0.112579, 7.45058e-09), (0.071529, 0.505864, 0),
                 (-0.0715289, 0.505864, 0), (-0.071529, 0.379091, 2.98023e-08),
                 (0.071529, 0.379091, 0), (-0.132587, 0.505864, 0),
                 (0.132587, 0.505864, 0), (-3.07015e-08, 0.667601, 1.19209e-07),
                 (-0.274712, -0.115, 2.23517e-08), (0.274712, -0.115, -7.45058e-09),
                 (0.210255, -0.211466, 0), (0.113789, -0.275922, 0),
                 (-9.03062e-08, -0.298556, 0), (-0.113789, -0.275922, 2.98023e-08),
                 (-0.210255, -0.211466, 0), (-0.668811, -0.00121029, 4.46188e-08),
                 (-0.507075, 0.131377, 4.47035e-08), (-0.507075, -0.133798, -1.49012e-08),
                 (-0.380301, 0.0703187, 1.49012e-08), (-0.380301, -0.0727393, 1.49012e-08),
                 (-0.507075, -0.0727393, -1.49012e-08), (-0.507075, 0.0703187, 4.47035e-08),
                 (0.507075, -0.0727393, -1.49012e-08), (0.507075, 0.0703187, -1.49012e-08),
                 (0.380301, 0.0703187, 1.49012e-08), (0.380301, -0.0727393, -1.49012e-08),
                 (0.507075, 0.131377, -1.49012e-08), (0.507075, -0.133798, -1.49012e-08),
                 (0.668811, -0.0012103, -1.49858e-08), (1.48112e-07, -0.670021, 0),
                 (-0.132587, -0.508285, 0), (0.132587, -0.508285, 0),
                 (-0.0715289, -0.381512, 2.98023e-08), (0.0715291, -0.381512, -2.98023e-08),
                 (0.0715291, -0.508285, 0), (-0.0715289, -0.508285, 0),
                 ]

        edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (7, 8), (0, 8), (10, 11), (9, 12),
                 (11, 12), (10, 13), (9, 14), (13, 15), (14, 15), (16,
                                                                   22), (17, 18), (18, 19), (19, 20), (20, 21),
                 (21, 22), (7, 17), (6, 16), (23, 24), (23, 25), (24,
                                                                  29), (25, 28), (26, 27), (26, 29), (27, 28),
                 (31, 32), (30, 33), (32, 33), (31, 34), (30, 35), (34,
                                                                    36), (35, 36), (37, 38), (37, 39), (38, 43),
                 (39, 42), (40, 41), (40, 43), (41, 42), ]

        faces = []

        mesh = obj.data
        mesh.from_pydata(verts, edges, [])
        mesh.update()


def create_camera_widget(self, name):
    # Creates a camera ctrl widget

    obj = create_widget(self, name)
    if obj != None:
        verts = [(0.13756819069385529, 1.0706068032106941e-08, -0.13756819069385529),
                 (0.1797415018081665, 5.353034016053471e-09, -0.07445136457681656),
                 (0.19455081224441528, -6.381313819948996e-16, 8.504085435845354e-09),
                 (0.1797415018081665, -5.353034016053471e-09, 0.07445138692855835),
                 (0.13756819069385529, -1.0706068032106941e-08, 0.13756819069385529),
                 (0.07445137947797775, -2.1412136064213882e-08, 0.1797415018081665),
                 (-9.740904971522468e-08, -2.1412136064213882e-08, 0.19455081224441528),
                 (-5.87527146933553e-08, 2.1412136064213882e-08, -0.19455081224441528),
                 (0.0744515135884285, 2.1412136064213882e-08, -0.17974145710468292),
                 (0.3317747414112091, 5.353034016053471e-09, -0.04680081456899643),
                 (0.3317747414112091, -5.353034016053471e-09, 0.04680081456899643),
                 (0.24882805347442627, -5.353034016053471e-09, 0.04680081456899643),
                 (0.24882805347442627, 5.353034016053471e-09, -0.04680084437131882),
                 (0.3317747414112091, -5.353034016053471e-09, 0.08675074577331543),
                 (0.3317747414112091, 5.353034016053471e-09, -0.08675074577331543),
                 (0.43759751319885254, 0.0, 0.0), (-0.07445148378610611, -
                                                   2.1412136064213882e-08, 0.17974145710468292),
                 (-0.07445141673088074, 2.1412136064213882e-08, -0.1797415018081665),
                 (-0.13756820559501648, 1.0706068032106941e-08, -0.1375681608915329),
                 (-0.1797415018081665, 5.353034016053471e-09, -0.07445136457681656),
                 (-0.19455081224441528, -1.2762627639897992e-15, 2.0872269246297037e-08),
                 (-0.1797415018081665, -5.353034016053471e-09, 0.07445140182971954),
                 (-0.1375681608915329, -1.0706068032106941e-08, 0.13756820559501648),
                 (5.1712785165136665e-08, -4.2824272128427765e-08, 0.43759751319885254),
                 (0.08675077557563782, -2.1412136064213882e-08, 0.3317747414112091),
                 (-0.08675073087215424, -2.1412136064213882e-08, 0.3317747414112091),
                 (0.046800870448350906, -2.1412136064213882e-08, 0.24882805347442627),
                 (-0.04680079594254494, -2.1412136064213882e-08, 0.24882805347442627),
                 (-0.04680079594254494, -2.1412136064213882e-08, 0.3317747414112091),
                 (0.04680084437131882, -2.1412136064213882e-08, 0.3317747414112091),
                 (-0.04680076241493225, 2.1412136064213882e-08, -0.3317747414112091),
                 (0.046800874173641205, 2.1412136064213882e-08, -0.3317747414112091),
                 (0.04680086299777031, 2.1412136064213882e-08, -0.24882805347442627),
                 (-0.046800799667835236, 2.1412136064213882e-08, -0.24882805347442627),
                 (0.0867508053779602, 2.1412136064213882e-08, -0.3317747414112091),
                 (-0.08675070106983185, 2.1412136064213882e-08, -0.3317747414112091),
                 (4.711345980012993e-08, 4.2824272128427765e-08, -0.43759751319885254),
                 (-0.43759751319885254, 1.0210102111918393e-14, -9.882624141255292e-08),
                 (-0.3317747414112091, -5.353034016053471e-09, 0.08675065636634827),
                 (-0.3317747414112091, 5.353034016053471e-09, -0.08675083518028259),
                 (-0.24882805347442627, -5.353034016053471e-09, 0.04680076986551285),
                 (-0.24882805347442627, 5.353034016053471e-09, -0.0468008853495121),
                 (-0.3317747414112091, 5.353034016053471e-09, -0.046800896525382996),
                 (-0.3317747414112091, -5.353034016053471e-09, 0.04680073633790016),
                 (-0.08263588696718216, -7.0564780685344886e-09, 0.08263592422008514),
                 (-0.10796899348497391, -3.5282390342672443e-09, 0.04472224414348602),
                 (-0.11686481535434723, -8.411977372806655e-16, 1.2537773486087644e-08),
                 (-0.10796899348497391, 3.5282390342672443e-09, -0.04472222551703453),
                 (-0.08263592422008514, 7.0564780685344886e-09, -0.08263588696718216),
                 (-0.04472225159406662, 7.0564780685344886e-09, -0.10796899348497391),
                 (-0.0447222925722599, -7.0564780685344886e-09, 0.10796897858381271),
                 (0.0447223074734211, 7.0564780685344886e-09, -0.10796897858381271),
                 (-3.529219583242593e-08, 7.0564780685344886e-09, -0.11686481535434723),
                 (-5.8512675593647145e-08, -7.0564780685344886e-09, 0.11686481535434723),
                 (0.04472222924232483, -7.0564780685344886e-09, 0.10796899348497391),
                 (0.08263590186834335, -7.0564780685344886e-09, 0.08263590186834335),
                 (0.10796899348497391, -3.5282390342672443e-09, 0.04472223296761513),
                 (0.11686481535434723, -4.2059886864033273e-16, 5.108323541946902e-09),
                 (0.10796899348497391, 3.5282390342672443e-09, -0.04472222924232483),
                 (0.08263590186834335, 7.0564780685344886e-09, -0.08263590186834335),
                 (3.725290298461914e-08, -2.1412136064213882e-08, 0.24882805347442627)]

        edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (7, 8), (0, 8),
                 (10, 11), (9, 12), (11, 12), (10, 13), (9, 14), (13, 15), (14, 15), (16, 22),
                 (17, 18), (18, 19), (19, 20), (20, 21), (21, 22), (7, 17), (6, 16), (23, 24),
                 (23, 25), (24, 29), (25, 28), (26, 29), (27, 28), (31, 32), (30, 33), (32, 33),
                 (31, 34), (30, 35), (34, 36), (35, 36), (37, 38), (37, 39), (38, 43), (39, 42),
                 (40, 41), (40, 43), (41, 42), (50, 53), (49, 52), (44, 45), (45, 46), (46, 47),
                 (47, 48), (48, 49), (44, 50), (51, 59), (51, 52), (53, 54), (54, 55), (55, 56),
                 (56, 57), (57, 58), (58, 59), (26, 60), (27, 60), (23, 60)]

        faces = []

        mesh = obj.data
        mesh.from_pydata(verts, edges, [])
        mesh.update()


def create_aim_widget(self, name):
    # Creates a camera aim widget

    obj = create_widget(self, name)
    if obj != None:
        verts = [(0.15504144132137299, 1.4901161193847656e-08, 0.15504144132137299),
                 (0.20257140696048737, 7.450580596923828e-09, 0.0839078277349472),
                 (0.21926172077655792, -8.881784197001252e-16, -9.584233851001045e-09),
                 (0.20257140696048737, -7.450580596923828e-09, -0.0839078426361084),
                 (0.15504144132137299, -1.4901161193847656e-08, -0.15504144132137299),
                 (0.0839078351855278, -1.4901161193847656e-08, -0.20257140696048737),
                 (-1.0978147457763043e-07, -1.4901161193847656e-08, -0.21926172077655792),
                 (-6.621520043381679e-08, 1.4901161193847656e-08, 0.21926172077655792),
                 (0.08390798419713974, 1.4901161193847656e-08, 0.2025713473558426),
                 (0.39969685673713684, 3.725290298461914e-09, 0.05274524539709091),
                 (0.39969685673713684, -3.725290298461914e-09, -0.05274524167180061),
                 (0.4931790232658386, -3.725290298461914e-09, -0.05274524167180061),
                 (0.4931790232658386, 3.725290298461914e-09, 0.052745271474123),
                 (0.39969685673713684, -7.450580596923828e-09, -0.09776943176984787),
                 (0.39969685673713684, 7.450580596923828e-09, 0.09776943176984787),
                 (0.28043296933174133, 6.226862126577502e-17, -6.226862788321993e-17),
                 (-0.08390796184539795, -1.4901161193847656e-08, -0.2025713473558426),
                 (-0.08390787988901138, 1.4901161193847656e-08, 0.20257140696048737),
                 (-0.15504147112369537, 1.4901161193847656e-08, 0.1550414115190506),
                 (-0.20257140696048737, 7.450580596923828e-09, 0.08390782028436661),
                 (-0.21926172077655792, -1.7763568394002505e-15, -2.352336458955051e-08),
                 (-0.20257140696048737, -7.450580596923828e-09, -0.08390786498785019),
                 (-0.1550414115190506, -1.4901161193847656e-08, -0.15504147112369537),
                 (2.9140544199890428e-08, 2.9802322387695312e-08, 0.2804329991340637),
                 (-0.09776944667100906, 2.9802322387695312e-08, 0.3996969163417816),
                 (0.09776947647333145, 2.9802322387695312e-08, 0.3996969163417816),
                 (-0.052745264023542404, 2.9802322387695312e-08, 0.4931790828704834),
                 (0.05274529010057449, 2.9802322387695312e-08, 0.4931790828704834),
                 (0.052745264023542404, 2.9802322387695312e-08, 0.3996969163417816),
                 (-0.052745234221220016, 2.9802322387695312e-08, 0.3996969163417816),
                 (0.05274517461657524, -2.9802322387695312e-08, -0.3996969759464264),
                 (-0.052745334804058075, -2.9802322387695312e-08, -0.3996969759464264),
                 (-0.05274537205696106, -2.9802322387695312e-08, -0.49317920207977295),
                 (0.05274519696831703, -2.9802322387695312e-08, -0.49317920207977295),
                 (-0.09776955097913742, -2.9802322387695312e-08, -0.3996969163417816),
                 (0.09776940196752548, -2.9802322387695312e-08, -0.39969703555107117),
                 (-7.148475589247028e-08, -2.9802322387695312e-08, -0.2804329991340637),
                 (-0.2804330289363861, 3.552713678800501e-15, 4.234420103443881e-08),
                 (-0.3996969759464264, -7.450580596923828e-09, -0.09776938706636429),
                 (-0.39969685673713684, 7.450580596923828e-09, 0.09776950627565384),
                 (-0.4931790232658386, -3.725290298461914e-09, -0.05274520441889763),
                 (-0.4931790232658386, 3.725290298461914e-09, 0.05274531990289688),
                 (-0.3996969163417816, 3.725290298461914e-09, 0.052745312452316284),
                 (-0.3996969163417816, -3.725290298461914e-09, -0.05274519324302673),
                 (-0.06401804089546204, -7.450580596923828e-09, -0.06401806324720383),
                 (-0.0836436077952385, -3.725290298461914e-09, -0.03464633598923683),
                 (-0.09053517132997513, -8.881784197001252e-16, -9.713016169143884e-09),
                 (-0.0836436077952385, 3.725290298461914e-09, 0.03464631363749504),
                 (-0.06401806324720383, 7.450580596923828e-09, 0.06401804089546204),
                 (-0.03464633598923683, 7.450580596923828e-09, 0.0836436077952385),
                 (-0.034646373242139816, -7.450580596923828e-09, -0.0836435854434967),
                 (0.03464638441801071, 7.450580596923828e-09, 0.0836435854434967),
                 (-2.734086912425937e-08, 7.450580596923828e-09, 0.09053517132997513),
                 (-4.532979147597871e-08, -7.450580596923828e-09, -0.09053517132997513),
                 (0.034646324813365936, -7.450580596923828e-09, -0.0836436077952385),
                 (0.06401804834604263, -7.450580596923828e-09, -0.06401804834604263),
                 (0.0836436077952385, -3.725290298461914e-09, -0.034646324813365936),
                 (0.09053517132997513, -4.440892098500626e-16, -3.957419281164221e-09),
                 (0.0836436077952385, 3.725290298461914e-09, 0.03464632108807564),
                 (0.06401804834604263, 7.450580596923828e-09, 0.06401804834604263),
                 (1.1175870895385742e-08, 2.9802322387695312e-08, 0.4931790828704834),
                 (-3.3337176574832483e-08, 2.4835267176115394e-09, 0.030178390443325043),
                 (-3.9333485801762436e-08, -2.4835271617007493e-09, -0.030178390443325043),
                 (-0.030178390443325043, -7.40148665436918e-16, -7.794483281031717e-09),
                 (0.030178390443325043, -5.921189111737107e-16, -5.875951281097969e-09)]

        edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (7, 8), (0, 8),
                 (10, 11), (9, 12), (11, 12), (10, 13), (9, 14), (13, 15), (14, 15), (16, 22),
                 (17, 18), (18, 19), (19, 20), (20, 21), (21, 22), (7, 17), (6, 16), (23, 24),
                 (23, 25), (24, 29), (25, 28), (26, 29), (27, 28), (31, 32), (30, 33), (32, 33),
                 (31, 34), (30, 35), (34, 36), (35, 36), (37, 38), (37, 39), (38, 43), (39, 42),
                 (40, 41), (40, 43), (41, 42), (50, 53), (49, 52), (44, 45), (45, 46), (46, 47),
                 (47, 48), (48, 49), (44, 50), (51, 59), (51, 52), (53, 54), (54, 55), (55, 56),
                 (56, 57), (57, 58), (58, 59), (26, 60), (27, 60), (23, 60), (61, 62), (63, 64)]

        faces = []

        mesh = obj.data
        mesh.from_pydata(verts, edges, [])
        mesh.update()
