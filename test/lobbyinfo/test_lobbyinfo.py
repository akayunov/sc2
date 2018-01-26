import sys
import os.path
import pytest
from PIL import Image

sys.path = [os.path.abspath(os.path.dirname(__file__) + '../../../src/')] + sys.path
from sc2.lobbyinfo import LobbyInfo


@pytest.mark.parametrize("test_input, expected", [
    ('one-expand.png', {'gazes': [(21, 17), (28, 24)], 'minerals': [(2, 28), (4, 23), (4, 26), (4, 30), (6, 21), (8, 19), (13, 19), (15, 17)]}),
    ('two-expand.png', {'gazes': [(21, 17), (28, 24), (61, 30), (86, 28)],
                        'minerals': [(2, 28), (4, 23), (4, 26), (4, 30), (6, 21), (8, 19), (13, 19), (15, 17), (62, 24), (63, 23), (69, 21), (71, 19), (74, 21), (76, 19), (81, 21),
                                     (83, 23)]})
])
def test_lobby_info(test_input, expected):
    # some hacks for more explicit test pictures
    LobbyInfo.LEFT = 0
    LobbyInfo.RIGHT = 100
    LobbyInfo.UP = 0
    LobbyInfo.BOTTOM = 100

    lobby_info = LobbyInfo()
    lobby_info.parse_regions(Image.open(os.path.dirname(__file__) + '/resourses/' + test_input))

    assert expected == lobby_info.minimap
    lobby_info.alarm()


@pytest.mark.xfail
def test_lobby_info_noisy_by_green():
    # some hacks for more explicit test pictures
    LobbyInfo.LEFT = 0
    LobbyInfo.RIGHT = 100
    LobbyInfo.UP = 0
    LobbyInfo.BOTTOM = 100

    lobby_info = LobbyInfo()
    lobby_info.parse_regions(Image.open(os.path.dirname(__file__) + '/resourses/' + 'noisy-by-green.png'))

    assert {'gazes': [], 'minerals': []} == lobby_info.minimap
    lobby_info.alarm()

@pytest.mark.xfail
def test_lobby_info_noisy_by_red():
    # some hacks for more explicit test pictures
    LobbyInfo.LEFT = 0
    LobbyInfo.RIGHT = 100
    LobbyInfo.UP = 0
    LobbyInfo.BOTTOM = 100

    lobby_info = LobbyInfo()
    lobby_info.parse_regions(Image.open(os.path.dirname(__file__) + '/resourses/' + 'noisy-by-red.png'))

    assert {'gazes': [(49, 19)], 'minerals': [(29, 36), (29, 38), (31, 36), (31, 38), (32, 24), (32, 28), (33, 36), (33, 38), (34, 23), (36, 21), (43, 19)]} == lobby_info.minimap
    lobby_info.alarm()
