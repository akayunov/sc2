import os.path
import pytest
from PIL import Image

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
    ),
    (
            'vertical_mineral.png',
            {'gazes': [(7, 22), (24, 5)],
             'minerals': [(15, 22), (17, 24), (22, 22), (24, 21), (25, 12), (25, 15), (25, 19), (27, 14)]},
            [
                {'gazes': [(7, 22), (24, 5)], 'minerals': [(27, 14), (25, 12), (25, 15), (25, 19), (22, 22), (24, 21), (17, 24), (15, 22)]}

            ],
            (15, 11),
            {'gazes': [(7, 22), (24, 5)], 'minerals': [(27, 14), (25, 12), (25, 15), (25, 19), (22, 22), (24, 21), (17, 24), (15, 22)]},
            (17, 15)
    )

])
def test_map_info(test_input, expected, expected_group, input_coordinates, expected_nearest_resourses_group, main_building_position, monkeypatch):
    # some hacks for more explicit test pictures
    monkeypatch.setattr(MapInfo, 'LEFT', 0)
    monkeypatch.setattr(MapInfo, 'RIGHT', 100)
    monkeypatch.setattr(MapInfo, 'UP', 0)
    monkeypatch.setattr(MapInfo, 'BOTTOM', 100)

    map_info = MapInfo()
    map_info.parse_regions(Image.open(os.path.join(os.path.dirname(__file__), 'resourses', test_input)))

    assert expected == map_info.minimap
    assert expected_group == map_info.expand_groups
    assert expected_nearest_resourses_group == map_info.get_nearest_exp_resourses_group(*input_coordinates)
    assert main_building_position == map_info.calculate_main_building_position(expected_nearest_resourses_group)
    map_info.alarm()
    assert map_info.name() == 'map info'

# TODO implement it
# def test_map_info_full_map():
#     map_info2 = MapInfo()
#     map_info2.parse_regions(Image.open(os.path.dirname(__file__) + '/resourses/' + 'full_map.png'))
#
#     print(map_info2.expand_groups)
#     map_info.alarm()


@pytest.mark.xfail
def test_map_info_noisy_by_green(monkeypatch):
    # some hacks for more explicit test pictures
    monkeypatch.setattr(MapInfo, 'LEFT', 0)
    monkeypatch.setattr(MapInfo, 'RIGHT', 100)
    monkeypatch.setattr(MapInfo, 'UP', 0)
    monkeypatch.setattr(MapInfo, 'BOTTOM', 100)

    map_info = MapInfo()
    map_info.parse_regions(Image.open(os.path.join(os.path.dirname(__file__), 'resourses', 'noisy-by-green.png')))

    map_info.alarm()
    assert {'gazes': [], 'minerals': []} == map_info.minimap


@pytest.mark.xfail
def test_map_info_noisy_by_red(monkeypatch):
    # some hacks for more explicit test pictures
    monkeypatch.setattr(MapInfo, 'LEFT', 0)
    monkeypatch.setattr(MapInfo, 'RIGHT', 100)
    monkeypatch.setattr(MapInfo, 'UP', 0)
    monkeypatch.setattr(MapInfo, 'BOTTOM', 100)

    map_info = MapInfo()
    map_info.parse_regions(Image.open(os.path.join(os.path.dirname(__file__), 'resourses', 'noisy-by-red.png')))

    map_info.alarm()
    assert {'gazes': [(49, 19)], 'minerals': [(29, 36), (29, 38), (31, 36), (31, 38), (32, 24), (32, 28), (33, 36), (33, 38), (34, 23), (36, 21), (43, 19)]} == map_info.minimap
