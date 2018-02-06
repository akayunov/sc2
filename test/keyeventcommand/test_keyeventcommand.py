import re
import os
import pytest
from PIL import Image

from sc2.keyeventcommand import KeyEventCommand
from sc2.mapinfo import MapInfo


def test_key_event_command_initialization(keyboard_mock):
    map_info = MapInfo()
    kec = KeyEventCommand(map_info)
    assert kec.threads_flags == {
        kec.hotkey_send_command_to_units_by_one: [],
        kec.hotkey_occupy_expand: [],
        kec.hotkey_send_command_to_units_by_one_for_resiege_tanks: [],
        kec.hotkey_build_svc: []
    }
    assert keyboard_mock.hotkeys == set(['`', 'w', 'z+c', 'z+x'])


def test_key_event_command_move(mouse_mock, keyboard_mock, keyevent_mock):
    mouse_mock.wait_buttons = ['left', 'left']
    mouse_mock.get_positions = [(0, 0), (1, 1)]

    map_info = MapInfo()
    kec = KeyEventCommand(map_info)

    with pytest.raises(IndexError):
        kec.send_command_to_units_by_one(kec.hotkey_send_command_to_units_by_one, kec.move_unit_command)
    assert mouse_mock.click_buttons == ['left', 'right', 'left', 'right']
    assert mouse_mock.move_coordinates == [(700, 900), (0, 0), (700, 900), (1, 1)]
    assert keyboard_mock.send_buttons == ['ctrl+9', 'alt+8', '9', 'alt+8', '9']

    assert keyboard_mock.hotkeys == set(['`', 'w', 'z+c', 'z+x'])

    assert len(kec.threads_flags[kec.hotkey_send_command_to_units_by_one]) == 1 and re.match(r'\d+', str(kec.threads_flags[kec.hotkey_send_command_to_units_by_one][0]))
    assert kec.threads_flags[kec.hotkey_occupy_expand] == []
    assert kec.threads_flags[kec.hotkey_send_command_to_units_by_one_for_resiege_tanks] == []
    assert kec.threads_flags[kec.hotkey_build_svc] == []

    keyevent_mock.name = kec.hotkey_send_command_to_units_by_one
    kec.turn_off_threads_flags(keyevent_mock)
    assert kec.threads_flags[kec.hotkey_send_command_to_units_by_one] == []


def test_key_event_command_siege_tank(mouse_mock, keyboard_mock, keyevent_mock):
    mouse_mock.wait_buttons = ['left', 'left']
    mouse_mock.get_positions = [(0, 0), (1, 1)]

    map_info = MapInfo()
    kec = KeyEventCommand(map_info)

    with pytest.raises(IndexError):
        kec.send_command_to_units_by_one(kec.hotkey_send_command_to_units_by_one_for_resiege_tanks, kec.re_seige_tanks)

    assert mouse_mock.click_buttons == ['left', 'right', 'left', 'right']
    assert mouse_mock.move_coordinates == [(700, 900), (0, 0), (700, 900), (1, 1)]
    assert keyboard_mock.send_buttons == ['ctrl+9', 'alt+8', 'shift', 'e', 'shift', '9', 'alt+8', 'shift', 'e', 'shift', '9']
    assert keyboard_mock.hotkeys == set(['`', 'w', 'z+c', 'z+x'])

    assert (
        len(kec.threads_flags[kec.hotkey_send_command_to_units_by_one_for_resiege_tanks]) == 1 and
        re.match(r'\d+', str(kec.threads_flags[kec.hotkey_send_command_to_units_by_one_for_resiege_tanks][0]))
    )
    assert kec.threads_flags[kec.hotkey_occupy_expand] == []
    assert kec.threads_flags[kec.hotkey_send_command_to_units_by_one] == []
    assert kec.threads_flags[kec.hotkey_build_svc] == []

    keyevent_mock.name = kec.hotkey_send_command_to_units_by_one_for_resiege_tanks
    kec.turn_off_threads_flags(keyevent_mock)
    assert kec.threads_flags[kec.hotkey_send_command_to_units_by_one] == []


def test_key_event_command_scv(keyboard_mock, keyevent_mock):
    map_info = MapInfo()
    kec = KeyEventCommand(map_info)
    kec.scv_building_time = 0  # fake for speed

    kec.build_scv(kec.hotkey_build_svc)
    assert keyboard_mock.send_buttons == [
        'ctrl+9', '6', 's', 's', '9,9',
        'ctrl+9', '6', 's', 's', '9,9',
        'ctrl+9', '6', 's', 's', '9,9',
        'ctrl+9', '6', 's', 's', '9,9',
        'ctrl+9', '6', 's', 's', '9,9',
        'ctrl+9', '6', 's', 's', '9,9',
        'ctrl+9', '6', 's', 's', '9,9',
        'ctrl+9', '6', 's', 's', '9,9',
        'ctrl+9', '6', 's', 's', '9,9',
        'ctrl+9', '6', 's', 's', '9,9',
        'ctrl+9', '6', 's', 's', '9,9'
    ]

    assert len(kec.threads_flags[kec.hotkey_build_svc]) == 1 and re.match(r'\d+', str(kec.threads_flags[kec.hotkey_build_svc][0]))
    assert kec.threads_flags[kec.hotkey_occupy_expand] == []
    assert kec.threads_flags[kec.hotkey_send_command_to_units_by_one] == []
    assert kec.threads_flags[kec.hotkey_send_command_to_units_by_one_for_resiege_tanks] == []

    keyevent_mock.name = 'z'
    kec.turn_off_threads_flags(keyevent_mock)
    assert kec.threads_flags[kec.hotkey_build_svc] == []

    assert keyboard_mock.hotkeys == set(['`', 'w', 'z+c', 'z+x'])


def test_key_event_command_expand(mouse_mock, keyboard_mock, keyevent_mock):
    mouse_mock.wait_buttons = ['left', 'left', 'left']
    mouse_mock.get_positions = [(160, 1000)]

    map_info = MapInfo()
    map_info.parse_regions(Image.open(os.path.dirname(__file__) + '/resourses/' + 'full_map.png'))

    kec = KeyEventCommand(map_info)
    kec.occupy_expand(kec.hotkey_occupy_expand)

    assert keyboard_mock.send_buttons == ['0', 'b,c', '0', 'b,r', '0', 'b,r']
    assert mouse_mock.move_coordinates == [(162, 1016), (960, 540), (169, 1010), (960, 540), (169, 1003), (960, 540)]
    assert mouse_mock.click_buttons == ['left', 'left', 'left']

    assert len(kec.threads_flags[kec.hotkey_occupy_expand]) == 1 and re.match(r'\d+', str(kec.threads_flags[kec.hotkey_occupy_expand][0]))
    assert kec.threads_flags[kec.hotkey_build_svc] == []
    assert kec.threads_flags[kec.hotkey_send_command_to_units_by_one] == []
    assert kec.threads_flags[kec.hotkey_send_command_to_units_by_one_for_resiege_tanks] == []

    keyevent_mock.name = 'z'
    kec.turn_off_threads_flags(keyevent_mock)
    assert kec.threads_flags[kec.hotkey_occupy_expand] == []

    assert keyboard_mock.hotkeys == set(['`', 'w', 'z+c', 'z+x'])
