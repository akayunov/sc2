import keyboard
import mouse
import threading

from sc2.productionqueue import ProductionQueue
from sc2.watcher import WatcherProperties
from sc2.const import RESOLUTION


class KeyEventCommand:
    def __init__(self, map_info):
        self.map_info = map_info
        self.while_flag = False
        self.hotkeys = set()
        keyboard.on_release(self.turn_off_while_flag)

        production_queue_watcher = WatcherProperties(ProductionQueue(), 0)
        self.add_hotkey('3', production_queue_watcher.run_watcher, in_own_thread=False)
        self.add_hotkey('4', production_queue_watcher.run_watcher, in_own_thread=False)
        self.add_hotkey('5', production_queue_watcher.run_watcher, in_own_thread=False)
        self.add_hotkey('6', production_queue_watcher.run_watcher, in_own_thread=False)
        # new expand
        self.add_hotkey('z+x', target=self.occupy_expand, args=(), timeout=1, in_own_thread=False)
        # move commads
        self.add_hotkey('`', target=self.send_command_to_units_by_one, args=(self.move_unit_command,), timeout=1)
        self.add_hotkey('q', target=self.send_command_to_units_by_one, args=(self.re_seige_tanks,), timeout=1)

    def add_hotkey(self, hotkey, target, args=(), in_own_thread=True, timeout=0):
        self.hotkeys.update(hotkey)
        if in_own_thread:
            # you should recreate this thread(remove and add this hotkey again) in hotkey handler because of threads can only be started once
            keyboard.add_hotkey(hotkey, threading.Thread(target=target, args=([hotkey] + list(args))).start,
                                suppress=False, timeout=timeout, trigger_on_release=False)
        else:
            keyboard.add_hotkey(hotkey, target, args=args, suppress=False, timeout=timeout, trigger_on_release=False)

    def turn_off_while_flag(self, event):
        if event.name in self.hotkeys or event.name == 'esc':
            self.while_flag = False

    def occupy_expand(self):
        mouse_position_x, mouse_position_y = mouse.get_position()
        resourses_group = self.map_info.get_nearest_exp_resourses_group(mouse_position_x, mouse_position_y)
        new_mouse_position_x, new_mouse_position_y = self.map_info.calculate_main_building_position(resourses_group)
        mouse.move(new_mouse_position_x, new_mouse_position_y)
        mouse.click(button='left')  # move by minimap
        mouse.move(RESOLUTION.x / 2, RESOLUTION.y / 2)
        # we are in center of screen on new expand
        keyboard.send('0')  # choose worker
        keyboard.send('b')
        keyboard.send('c')
        mouse.wait()  # build cc
        # TODO move worker to minerals
        for gaz in resourses_group['gazes']:
            new_mouse_position_x, new_mouse_position_y = self.map_info.get_item_coordinate_on_whole_screen(gaz)
            mouse.move(new_mouse_position_x, new_mouse_position_y)  # move by minimap

            mouse.click()
            mouse.move(RESOLUTION.x / 2, RESOLUTION.y / 2)
            #mouse.wait()
        #    # we are in center of screen on new gaz
            keyboard.send('0')  # choose worker
            keyboard.send('b')
            keyboard.send('r')
            mouse.wait()  # build gazs

    @staticmethod
    def move_unit_command():
        mouse.click(button='right')

    @staticmethod
    def re_seige_tanks():
        keyboard.press('shift')
        mouse.click(button='right')
        keyboard.send('e')
        keyboard.release('shift')

    def send_command_to_units_by_one(self, hotkey, command):
        self.while_flag = True
        keyboard.remove_hotkey(hotkey)
        # move units to group 9
        keyboard.send('ctrl+9')
        # while we wait it we don't want triger this hotkey again
        mouse.wait(button='left', target_types=('up',))
        is_waited = False
        while self.while_flag:
            if is_waited:
                mouse.wait(button='left', target_types=('up',))
                if not self.while_flag:
                    break
            mouse_position_x, mouse_position_y = mouse.get_position()
            # click on first unit
            mouse.move(700, 900)
            mouse.click()
            # remove unit from group
            keyboard.send('alt+8')
            mouse.move(mouse_position_x, mouse_position_y)
            # mouse.click(button='left')
            # move units
            command()
            # choose left units
            keyboard.send('9')
            is_waited = True
        keyboard.add_hotkey(hotkey, threading.Thread(target=self.send_command_to_units_by_one, args=(hotkey, command)).start, suppress=False, timeout=1, trigger_on_release=False)
