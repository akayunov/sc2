import os
import pytest
import playsound
import keyboard
import mouse


# TODO move to monkepatch
def mock_play_sound(path):
    os.path.isfile(path)


playsound.playsound = mock_play_sound


class MockException(Exception):
    pass


class KeyBoardMock:
    def __init__(self):
        self.combination = ''
        self.send_buttons = []
        self.hotkeys = set()

    def send(self, combination, do_press=True, do_release=True):
        self.send_buttons.append(combination)

    def remove_hotkey(self, combination):
        self.hotkeys.remove(combination)

    def add_hotkey(self, hotkey, callback, args=(), suppress=False, timeout=1, trigger_on_release=False):
        self.hotkeys.update([hotkey])

    def is_pressed(self, combination):
        return True

    def on_release(self, callback):
        pass

    def release(self, button):
        self.send_buttons.append(button)

    def press(self, button):
        self.send_buttons.append(button)


class MouseMock:
    def __init__(self):
        self.wait_buttons = []
        self.move_coordinates = []
        self.click_buttons = []
        self.get_positions = []

    def wait(self, button='left', target_types=('up', 'down', 'double')):
        return self.wait_buttons.pop(0)

    def move(self, x, y):
        self.move_coordinates.append((x, y))

    def click(self, button='left'):
        self.click_buttons.append(button)

    def get_position(self):
        return self.get_positions.pop(0)


class KeyBoardEvent:
    def __init__(self, name):
        self.name = name


@pytest.fixture(scope='function')
def keyevent_mock():
    return KeyBoardEvent('tratata')


@pytest.fixture(scope='function')
def mouse_mock():
    mm = MouseMock()
    mouse.wait = mm.wait
    mouse.move = mm.move
    mouse.click = mm.click
    mouse.get_position = mm.get_position
    return mm


@pytest.fixture(scope='function')
def keyboard_mock():
    km = KeyBoardMock()
    keyboard.send = km.send
    keyboard.add_hotkey = km.add_hotkey
    keyboard.remove_hotkey = km.remove_hotkey
    keyboard.is_pressed = km.is_pressed
    keyboard.on_release = km.on_release
    keyboard.release = km.release
    keyboard.press = km.press
    return km
