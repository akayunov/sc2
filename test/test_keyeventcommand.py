import pytest
from sc2.keyeventcommand2 import KeyEventCommand
from sc2.mapinfo import MapInfo


def test_key_event_command_move(mouse_mock, keyboard_mock):
    mouse_mock.wait_buttons = ['left', 'left']
    mouse_mock.get_positions = [(0, 0), (1, 1)]

    map_info = MapInfo()
    kec = KeyEventCommand(map_info)
    assert keyboard_mock.hotkeys == set(['`', 'w', 'z+c', 'z+x'])
    with pytest.raises(IndexError):
        kec.send_command_to_units_by_one(kec.hotkey_send_command_to_units_by_one, kec.move_unit_command)
    assert mouse_mock.click_buttons == ['left', 'right', 'left', 'right']
    assert mouse_mock.move_coordinates == [(700, 900), (0, 0), (700, 900), (1, 1)]
    assert keyboard_mock.send_buttons == ['ctrl+9', 'alt+8', '9', 'alt+8', '9']
    assert keyboard_mock.hotkeys == set(['`', 'w', 'z+c', 'z+x'])


def test_key_event_command_siege_tank(mouse_mock, keyboard_mock):
    mouse_mock.wait_buttons = ['left', 'left']
    mouse_mock.get_positions = [(0, 0), (1, 1)]

    map_info = MapInfo()
    kec = KeyEventCommand(map_info)
    assert keyboard_mock.hotkeys == set(['`', 'w', 'z+c', 'z+x'])
    with pytest.raises(IndexError):
        kec.send_command_to_units_by_one(kec.hotkey_send_command_to_units_by_one, kec.re_seige_tanks)
    assert mouse_mock.click_buttons == ['left', 'right', 'left', 'right']
    assert mouse_mock.move_coordinates == [(700, 900), (0, 0), (700, 900), (1, 1)]
    assert keyboard_mock.send_buttons == ['ctrl+9', 'alt+8', 'shift', 'e', 'shift', '9', 'alt+8', 'shift', 'e', 'shift', '9']
    assert keyboard_mock.hotkeys == set(['`', 'w', 'z+c', 'z+x'])