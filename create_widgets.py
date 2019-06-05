import bpy


def create_widget(self, name):
    """ Creates an empty widget object for a bone, and returns the object."""
    obj_name = "WDGT_" + name
    scene = bpy.context.scene

    mesh = bpy.data.meshes.new(obj_name)
    obj = bpy.data.objects.new(obj_name, mesh)

    # create a new collection for the wigets
    collection_name = "camera_widgets"
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
    """ Creates a compass-shaped widget."""
    obj = create_widget(self, name)
    if obj != None:
        verts = [(0.2102552056312561, -0.0012103617191314697, 0.21025514602661133),
                 (0.11378927528858185, -0.001210339367389679, 0.274711549282074),
                 (-3.070153553608179e-08, -0.0012103626504540443, 0.29734566807746887),
                 (-0.11378933489322662, -0.0012103542685508728, 0.27471157908439636),
                 (-0.2102552056312561, -0.0012103617191314697, 0.21025516092777252),
                 (-0.27471160888671875, -0.0012103617191314697, 0.11378928273916245),
                 (-0.29734569787979126, -0.0012103617191314697, -1.6809221392577456e-07),
                 (0.29734572768211365, -0.001210331916809082, -1.0901101177296368e-07),
                 (0.2747114598751068, -0.0012103617191314697, 0.11378948390483856),
                 (0.07152898609638214, -0.0012103691697120667, 0.5070746541023254),
                 (-0.07152895629405975, -0.0012103617191314697, 0.5070746541023254),
                 (-0.07152898609638214, -0.0012103915214538574, 0.38030144572257996),
                 (0.07152898609638214, -0.0012103691697120667, 0.38030144572257996),
                 (-0.1325872540473938, -0.0012103617191314697, 0.5070746541023254),
                 (0.13258719444274902, -0.0012103617191314697, 0.5070746541023254),
                 (-3.070154264150915e-08, -0.0012104818597435951, 0.6688110828399658),
                 (-0.274711549282074, -0.0012103617191314697, -0.11378948390483856),
                 (0.274711549282074, -0.001210331916809082, -0.1137893795967102),
                 (0.21025514602661133, -0.001210331916809082, -0.21025525033473969),
                 (0.11378927528858185, -0.001210339367389679, -0.27471160888671875),
                 (-9.030617320604506e-08, -0.0012103328481316566, -0.29734572768211365),
                 (-0.11378933489322662, -0.0012103542685508728, -0.27471157908439636),
                 (-0.2102552056312561, -0.001210331916809082, -0.21025516092777252),
                 (-0.6688110828399658, -0.0012103915214538574, 5.982118267411352e-08),
                 (-0.5070747137069702, -0.0012103915214538574, 0.13258729875087738),
                 (-0.5070747137069702, -0.001210331916809082, -0.1325872540473938),
                 (-0.38030147552490234, -0.0012103617191314697, 0.07152903825044632),
                 (-0.38030147552490234, -0.0012103617191314697, -0.07152897119522095),
                 (-0.5070747137069702, -0.001210331916809082, -0.07152896374464035),
                 (-0.5070747137069702, -0.0012103915214538574, 0.07152900844812393),
                 (0.5070745944976807, -0.001210331916809082, -0.07152891904115677),
                 (0.5070745944976807, -0.001210331916809082, 0.07152905315160751),
                 (0.38030144572257996, -0.0012103617191314697, 0.07152903825044632),
                 (0.38030141592025757, -0.001210331916809082, -0.07152897119522095),
                 (0.5070745944976807, -0.001210331916809082, 0.13258734345436096),
                 (0.5070745944976807, -0.001210331916809082, -0.13258720934391022),
                 (0.6688110828399658, -0.001210331916809082, 5.279173720396102e-08),
                 (1.4811239168466273e-07, -0.001210303045809269, -0.6688110828399658),
                 (-0.13258716464042664, -0.0012103021144866943, -0.5070746541023254),
                 (0.13258737325668335, -0.0012103021144866943, -0.5070746541023254),
                 (-0.07152889668941498, -0.0012103617191314697, -0.38030150532722473),
                 (0.07152910530567169, -0.0012103095650672913, -0.38030150532722473),
                 (0.07152910530567169, -0.0012103095650672913, -0.5070746541023254),
                 (-0.07152886688709259, -0.0012103021144866943, -0.5070746541023254)]

        edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (7, 8), (0, 8),
                 (10, 11), (9, 12), (11, 12), (10, 13), (9, 14), (13, 15), (14, 15),
                 (16, 22), (17, 18), (18, 19), (19, 20), (20, 21), (21, 22), (7, 17),
                 (6, 16), (23, 24), (23, 25), (24, 29), (25, 28), (26, 27), (26, 29),
                 (27, 28), (31, 32), (30, 33), (32, 33), (31, 34), (30, 35), (34, 36),
                 (35, 36), (37, 38), (37, 39), (38, 43), (39, 42), (40, 41), (40, 43), (41, 42)]

        mesh = obj.data
        mesh.from_pydata(verts, edges, [])
        mesh.update()


def create_camera_widget(self, name):
    """Creates a camera ctrl widget."""

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

        mesh = obj.data
        mesh.from_pydata(verts, edges, [])
        mesh.update()


def create_aim_widget(self, name):
    """ Creates a camera aim widget."""

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

        mesh = obj.data
        mesh.from_pydata(verts, edges, [])
        mesh.update()
