import traceback
import os
import sys
import pyautogui as pag
import keyboard
import mouse
import threading

sys.path = [os.path.abspath(os.path.dirname(__file__) + '/../src/')] + sys.path

from sc2.productionqueue import ProductionQueue
from sc2.mapinfo import MapInfo

GLOBAL_WHILE_FLAG = False

# check production queue if can
production_queue = ProductionQueue()


def run_watcher(watcher):
    im = pag.screenshot()
    try:
        print('=' * 8, watcher.NAME, '=' * 8)
        watcher.parse_regions(im)
        watcher.alarm()
    except Exception:
        print(traceback.format_exc())


def occupy_expand(map_inf):
    mouse_position_x, mouse_position_y = mouse.get_position()
    resourses_group = map_inf.get_nearest_exp_resourses_group(mouse_position_x, mouse_position_y )
    new_mouse_position_x, new_mouse_position_y = map_inf.calculate_main_building_position(resourses_group)
    mouse.move(new_mouse_position_x, new_mouse_position_y)
    mouse.click(button='left')  # move by minimap
    # TODO improve for different resolution
    mouse.move(1920 / 2, 1080 / 2)
    # we are in center of screen on new expand
    keyboard.send('0')  # choose worker
    keyboard.send('b')
    keyboard.send('c')
    #mouse.wait()  # build cc
    # TODO move worker to minerals
    #for gaz in resourses_group['gazes']:
    #    new_mouse_position_x, new_mouse_position_y = map_inf.get_item_coordinate_on_whole_screen(gaz)
    #    mouse.move(new_mouse_position_x, new_mouse_position_y)  # move by minimap
    #    mouse.click()
    #    mouse.move(1920 / 2, 1080 / 2)
    #    # we are in center of screen on new gaz
    #    keyboard.send('0')  # choose worker
    #    keyboard.send('b')
    #    keyboard.send('r')
    #    mouse.click()  # build gazs


def set_global_while_flag_to_value(event):
    global GLOBAL_WHILE_FLAG
    if event.name == '`':
        GLOBAL_WHILE_FLAG = False


def move_units_by_one():
    global GLOBAL_WHILE_FLAG
    GLOBAL_WHILE_FLAG = True
    keyboard.remove_hotkey('`')
    # move units to group 9
    keyboard.send('ctrl+9')
    # while wwe wait it we don't have any '`' hotkey
    mouse.wait(button='right', target_types=('up',))
    is_waited = False
    while GLOBAL_WHILE_FLAG:
        if is_waited:
            mouse.wait(button='right', target_types=('up',))
            if not GLOBAL_WHILE_FLAG:
                break
        mouse_position_x, mouse_position_y = mouse.get_position()
        # click on first unit
        mouse.move(700, 900)
        mouse.click()
        # remove unit from group
        keyboard.send('alt+8')
        mouse.move(mouse_position_x, mouse_position_y)
        mouse.click(button='right')
        # choose left units
        keyboard.send('9')
        is_waited = True
    keyboard.add_hotkey('`', threading.Thread(target=move_units_by_one).start, suppress=False, timeout=1, trigger_on_release=False)


if __name__ == '__main__':
    keyboard.wait('s')
    map_info = MapInfo()
    im = pag.screenshot()
    map_info.parse_regions(im)
    try:
        keyboard.add_hotkey('3', run_watcher, args=(production_queue,), suppress=False, timeout=0, trigger_on_release=False)
        keyboard.add_hotkey('4', run_watcher, args=(production_queue,), suppress=False, timeout=0, trigger_on_release=False)
        keyboard.add_hotkey('5', run_watcher, args=(production_queue,), suppress=False, timeout=0, trigger_on_release=False)
        keyboard.add_hotkey('6', run_watcher, args=(production_queue,), suppress=False, timeout=0, trigger_on_release=False)
        # new expand
        keyboard.add_hotkey('z+x', occupy_expand, args=(map_info,), suppress=False, timeout=1, trigger_on_release=False)
        # move unit by one

        keyboard.on_release(set_global_while_flag_to_value)
        keyboard.add_hotkey('`', threading.Thread(target=move_units_by_one).start, suppress=False, timeout=1, trigger_on_release=False)

        keyboard.wait()
    except KeyboardInterrupt:
        exit(0)
    except Exception:
        print(traceback.format_exc())
        exit(1)
    exit(0)
