import sys
import os.path
import pytest
from PIL import Image

sys.path = [os.path.abspath(os.path.dirname(__file__) + '../../../src/')] + sys.path
from sc2.mapinfo import MapInfo


@pytest.mark.parametrize("test_input, expected, expected_group, input_coordinates, expected_nearest_resourses_group, main_building_position", [
    (
            'one-expand.png',
            {'gazes': [(19, 15), (26, 22)], 'minerals': [(2, 28), (4, 23), (4, 26), (4, 30), (6, 21), (8, 19), (13, 19), (15, 17)]},
            [{'gazes': [(19, 15), (26, 22)], 'minerals': [(15, 17), (13, 19), (8, 19), (4, 23), (4, 26), (4, 30), (6, 21), (2, 28)]}],
            (16, 32),
            {'gazes': [(19, 15), (26, 22)], 'minerals': [(15, 17), (13, 19), (8, 19), (4, 23), (4, 26), (4, 30), (6, 21), (2, 28)]},
            (17, 30)
    ),
    (
            'two-expand.png',
            {'gazes': [(19, 15), (26, 22), (59, 28), (84, 26)],
             'minerals': [(2, 28), (4, 23), (4, 26), (4, 30), (6, 21), (8, 19), (13, 19), (15, 17), (62, 24), (63, 23), (69, 21), (71, 19), (74, 21), (76, 19), (81, 21),
                          (83, 23)]},
            [
                {'gazes': [(59, 28), (84, 26)], 'minerals': [(83, 23), (81, 21), (76, 19), (71, 19), (74, 21), (69, 21), (63, 23), (62, 24)]},
                {'gazes': [(19, 15), (26, 22)], 'minerals': [(15, 17), (13, 19), (8, 19), (4, 23), (4, 26), (4, 30), (6, 21), (2, 28)]}

            ],
            (70, 30),
            {'gazes': [(59, 28), (84, 26)], 'minerals': [(83, 23), (81, 21), (76, 19), (71, 19), (74, 21), (69, 21), (63, 23), (62, 24)]},
            (74, 34)
    )
])
def test_map_info(test_input, expected, expected_group, input_coordinates, expected_nearest_resourses_group, main_building_position, monkeypatch):
    # some hacks for more explicit test pictures
    monkeypatch.setattr(MapInfo, 'LEFT', 0)
    monkeypatch.setattr(MapInfo, 'RIGHT', 100)
    monkeypatch.setattr(MapInfo, 'UP', 0)
    monkeypatch.setattr(MapInfo, 'BOTTOM', 100)

    map_info = MapInfo()
    map_info.parse_regions(Image.open(os.path.dirname(__file__) + '/resourses/' + test_input))

    assert expected == map_info.minimap
    assert expected_group == map_info.expand_groups
    assert expected_nearest_resourses_group == map_info.get_nearest_exp_resourses_group(*input_coordinates)
    assert main_building_position == map_info.calculate_main_building_position(expected_nearest_resourses_group)
    map_info.alarm()


def test_map_info_full_map():
    map_info2 = MapInfo()
    map_info2.parse_regions(Image.open(os.path.dirname(__file__) + '/resourses/' + 'full_map.png'))

    assert {'gazes': [(18, 49), (25, 98), (28, 164), (32, 188), (35, 32), (42, 81), (52, 113), (68, 130), (73, 47), (73, 86), (80, 40), (80, 79), (82, 236),
                      (99, 219), (123, 54), (123, 61), (149, 198), (149, 205), (173, 40), (190, 23), (192, 180), (199, 173), (204, 129), (220, 146),
                      (230, 178), (240, 71), (244, 95), (247, 161)],
            'minerals': [
                (19, 44), (21, 39), (21, 42), (21, 46), (23, 37), (23, 177), (23, 182), (24, 36), (24, 171), (24, 178), (24, 183), (26, 93), (26, 170), (26, 187),
                (28, 88), (28, 92), (28, 95), (28, 188), (29, 36), (29, 86), (31, 34), (31, 85), (36, 83), (38, 85), (54, 122), (55, 120), (55, 124), (55, 127), (57, 129),
                (59, 131), (62, 132), (64, 131), (74, 95), (76, 93), (76, 97), (76, 100), (78, 102), (79, 103), (83, 105), (85, 103), (88, 44), (90, 42), (90, 236), (91, 238),
                (95, 44), (97, 46), (97, 236), (98, 47), (98, 51), (98, 54), (98, 234), (100, 53), (100, 226), (100, 229), (100, 233), (102, 227), (126, 51), (128, 49), (129, 214),
                (131, 216), (133, 47), (135, 46), (136, 217), (138, 47), (138, 216), (140, 46), (141, 217), (143, 216), (145, 47), (147, 49), (148, 214), (150, 212), (174, 36),
                (176, 30), (176, 34), (176, 37), (178, 29), (179, 27), (179, 217), (181, 219), (185, 25), (186, 27), (191, 160), (193, 158), (195, 219), (195, 220), (195, 221),
                (195, 222),
                (195, 223),
                (196, 219), (196, 220), (196, 221), (196, 222), (196, 223), (197, 160), (198, 161), (199, 212), (199, 213), (199, 214), (199, 215), (199, 216), (200, 163),
                (200, 166), (200, 170), (200, 212), (200, 213), (200, 214), (200, 215), (200, 216), (202, 168), (212, 132), (214, 131), (217, 132), (219, 134), (221, 136),
                (221, 139),
                (221, 143), (222, 141), (238, 178), (240, 180), (245, 178), (247, 177), (248, 75), (248, 168), (248, 171), (248, 175), (250, 76), (250, 93), (250, 170), (252, 80),
                (252, 85), (252, 92), (253, 81), (253, 86)
            ]} == map_info2.minimap
    assert [{'gazes': [(240, 71), (244, 95)],
             'minerals': [(253, 86),
                          (252, 80),
                          (252, 85),
                          (252, 92),
                          (253, 81),
                          (248, 75),
                          (250, 76),
                          (250, 93)]},
            {'gazes': [(230, 178), (247, 161)],
             'minerals': [(250, 170),
                          (248, 168),
                          (248, 171),
                          (248, 175),
                          (245, 178),
                          (247, 177),
                          (240, 180),
                          (238, 178)]},
            {'gazes': [(204, 129), (220, 146)],
             'minerals': [(222, 141),
                          (221, 136),
                          (221, 139),
                          (221, 143),
                          (217, 132),
                          (219, 134),
                          (212, 132),
                          (214, 131)]},
            {'gazes': [(199, 173), (192, 180)],
             'minerals': [(202, 168),
                          (200, 163),
                          (200, 166),
                          (200, 170),
                          (197, 160),
                          (198, 161),
                          (191, 160),
                          (193, 158)]},
            {'gazes': [],
             'minerals': [(200, 216),
                          (195, 219),
                          (195, 220),
                          (195, 221),
                          (195, 222),
                          (195, 223),
                          (196, 219),
                          (196, 220),
                          (196, 221),
                          (196, 222),
                          (196, 223),
                          (199, 212),
                          (199, 213),
                          (199, 214),
                          (199, 215),
                          (199, 216),
                          (200, 212),
                          (200, 213),
                          (200, 214),
                          (200, 215)]},
            {'gazes': [(173, 40), (190, 23)],
             'minerals': [(186, 27),
                          (185, 25),
                          (179, 27),
                          (176, 30),
                          (176, 34),
                          (176, 37),
                          (178, 29),
                          (174, 36)]},
            {'gazes': [], 'minerals': [(181, 219), (179, 217)]},
            {'gazes': [(149, 205), (149, 198)],
             'minerals': [(150, 212),
                          (148, 214),
                          (143, 216),
                          (138, 216),
                          (141, 217),
                          (136, 217),
                          (131, 216),
                          (129, 214)]},
            {'gazes': [(123, 54), (123, 61)],
             'minerals': [(147, 49),
                          (145, 47),
                          (140, 46),
                          (135, 46),
                          (138, 47),
                          (133, 47),
                          (128, 49),
                          (126, 51)]},
            {'gazes': [(82, 236), (99, 219)],
             'minerals': [(102, 227),
                          (100, 226),
                          (100, 229),
                          (100, 233),
                          (97, 236),
                          (98, 234),
                          (91, 238),
                          (90, 236)]},
            {'gazes': [(80, 40), (73, 47)],
             'minerals': [(100, 53),
                          (98, 47),
                          (98, 51),
                          (98, 54),
                          (95, 44),
                          (97, 46),
                          (90, 42),
                          (88, 44)]},
            {'gazes': [(73, 86), (80, 79)],
             'minerals': [(85, 103),
                          (79, 103),
                          (83, 105),
                          (76, 97),
                          (76, 100),
                          (78, 102),
                          (74, 95),
                          (76, 93)]},
            {'gazes': [(52, 113), (68, 130)],
             'minerals': [(64, 131),
                          (59, 131),
                          (62, 132),
                          (55, 127),
                          (57, 129),
                          (54, 122),
                          (55, 120),
                          (55, 124)]},
            {'gazes': [(25, 98), (42, 81)],
             'minerals': [(38, 85),
                          (36, 83),
                          (31, 85),
                          (28, 88),
                          (28, 92),
                          (28, 95),
                          (29, 86),
                          (26, 93)]},
            {'gazes': [(18, 49), (35, 32)],
             'minerals': [(31, 34),
                          (29, 36),
                          (23, 37),
                          (24, 36),
                          (21, 39),
                          (21, 42),
                          (21, 46),
                          (19, 44)]},
            {'gazes': [(28, 164), (32, 188)],
             'minerals': [(28, 188),
                          (23, 182),
                          (24, 178),
                          (24, 183),
                          (26, 187),
                          (23, 177),
                          (24, 171),
                          (26, 170)]}] == map_info2.expand_groups
    print(map_info2.expand_groups)
    # map_info.alarm()


@pytest.mark.xfail
def test_map_info_noisy_by_green(monkeypatch):
    # some hacks for more explicit test pictures
    monkeypatch.setattr(MapInfo, 'LEFT', 0)
    monkeypatch.setattr(MapInfo, 'RIGHT', 100)
    monkeypatch.setattr(MapInfo, 'UP', 0)
    monkeypatch.setattr(MapInfo, 'BOTTOM', 100)

    map_info = MapInfo()
    map_info.parse_regions(Image.open(os.path.dirname(__file__) + '/resourses/' + 'noisy-by-green.png'))

    assert {'gazes': [], 'minerals': []} == map_info.minimap
    map_info.alarm()


@pytest.mark.xfail
def test_map_info_noisy_by_red(monkeypatch):
    # some hacks for more explicit test pictures
    monkeypatch.setattr(MapInfo, 'LEFT', 0)
    monkeypatch.setattr(MapInfo, 'RIGHT', 100)
    monkeypatch.setattr(MapInfo, 'UP', 0)
    monkeypatch.setattr(MapInfo, 'BOTTOM', 100)

    map_info = MapInfo()
    map_info.parse_regions(Image.open(os.path.dirname(__file__) + '/resourses/' + 'noisy-by-red.png'))

    assert {'gazes': [(49, 19)], 'minerals': [(29, 36), (29, 38), (31, 36), (31, 38), (32, 24), (32, 28), (33, 36), (33, 38), (34, 23), (36, 21), (43, 19)]} == map_info.minimap
    map_info.alarm()
