import keyboard
import mouse
import threading
import time
from sc2.sasayblock import SasayBlock
from sc2.utils import get_screenshot
from sc2.const import RESOLUTION


class KeyEventCommand:
    def __init__(self, map_info):
        self.map_info = map_info

        self.hotkey_occupy_expand = 'z+x'
        self.hotkey_build_svc = 'z+m'
        # TODO don't need two hot key for unit and for tanks
        self.hotkey_send_command_to_units_by_one = '`'
        self.hotkey_send_command_to_units_by_one_for_resiege_tanks = 'w'


        self.scv_building_time = 12
        self.threads_flags = {
            self.hotkey_send_command_to_units_by_one: [],
            self.hotkey_send_command_to_units_by_one_for_resiege_tanks: [],
        }
        keyboard.on_release(self.turn_off_threads_flags)

        # new expand
        self.add_hotkey(self.hotkey_occupy_expand, target=self.occupy_expand, args=(), timeout=1)
        self.add_hotkey(self.hotkey_build_svc, target=self.build_scv, args=(), timeout=1)
        # move commads
        self.add_hotkey(self.hotkey_send_command_to_units_by_one, target=self.send_command_to_units_by_one, args=(self.move_unit_command,), timeout=1)
        self.add_hotkey(self.hotkey_send_command_to_units_by_one_for_resiege_tanks, target=self.send_command_to_units_by_one, args=(self.re_seige_tanks,), timeout=1)

    @staticmethod
    def add_hotkey(hotkey, target, args=(), timeout=0):
        keyboard.add_hotkey(
            hotkey, threading.Thread(target=target, args=([hotkey] + list(args))).start, suppress=False, timeout=timeout, trigger_on_release=False
        )

    def turn_off_threads_flags(self, event):
        if event.name == self.hotkey_send_command_to_units_by_one:
            self.threads_flags[self.hotkey_send_command_to_units_by_one] = []
        if event.name == self.hotkey_send_command_to_units_by_one_for_resiege_tanks:
            self.threads_flags[self.hotkey_send_command_to_units_by_one_for_resiege_tanks] = []

    def occupy_expand(self, hotkey):
        try:
            keyboard.remove_hotkey(hotkey)
            mouse_position_x, mouse_position_y = mouse.get_position()
            resourses_group = self.map_info.get_nearest_exp_resourses_group(mouse_position_x, mouse_position_y)
            new_mouse_position_x, new_mouse_position_y = self.map_info.calculate_main_building_position(resourses_group)
            mouse.move(new_mouse_position_x, new_mouse_position_y)
            mouse.click(button='left')  # move by minimap to center of screen on new expand
            keyboard.send('0')  # choose worker
            time.sleep(0.1)  # some exerimental things
            mouse.move(RESOLUTION.x / 2, RESOLUTION.y / 2)
            keyboard.send('b,c')
            mouse.wait()  # build cc
            keyboard.send('esc')

            # TODO move worker which build cc to minerals
            for i, gaz in enumerate(resourses_group['gazes']):
                new_mouse_position_x, new_mouse_position_y = self.map_info.get_item_coordinate_on_whole_screen(gaz)
                time.sleep(0.1)
                mouse.move(new_mouse_position_x, new_mouse_position_y)  # move by minimap
                time.sleep(0.1)
                mouse.click()
                keyboard.send('0')  # choose worker
                time.sleep(0.1)
                mouse.move(RESOLUTION.x / 2, RESOLUTION.y / 2)
                keyboard.send('b,r')
                mouse.wait()  # build gaz
                keyboard.send('esc')
        finally:
            # recreate thread for next run
            keyboard.add_hotkey(hotkey, threading.Thread(target=self.occupy_expand, args=(hotkey,)).start)

    def build_scv(self, hotkey):
        try:
            keyboard.remove_hotkey(hotkey)
            worker_counter = 22

            while 1:
                # TODO I don't need screenshot to check building quue just now how many cc on map by parsing
                # 6 group key and that all and d oorder after 12 sec
                # as close as posible to send "s" but before get screenshot, do I realy need scren shot I just need to know how many cc is exits
                image = get_screenshot()
                try:
                    #  check resourses before order to ensure that order will be done
                    sasayblock = SasayBlock()
                    sasayblock.parse_regions(image)
                    worker_can_be_order_by_this_mineral_count = int(sasayblock.minerals / 50)
                except Exception:
                    worker_can_be_order_by_this_mineral_count = 4

                # TODO how to disable right click in this time?
                worker_needed = 2  # TODO get this number from parsing cc count

                keyboard.send('ctrl+9')  # add curent selected to 0, for returning back
                keyboard.send('6')
                for i in range(min(worker_can_be_order_by_this_mineral_count, worker_needed)):
                    worker_counter -= 1
                    keyboard.send('s')
                    if worker_counter <= 0:
                        break
                if worker_counter <= 0:
                    break
                keyboard.send('9')
                time.sleep(self.scv_building_time)
            keyboard.send('9')
        finally:
            # recreate thread for next run
            keyboard.add_hotkey(hotkey, threading.Thread(target=self.build_scv, args=(hotkey,)).start)

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
        # recreate thread for next run
        # threading.get_ident() can be recycled by new thread but is doesn't matter because we always reinitialize it
        try:
            self.threads_flags[hotkey].append(threading.get_ident())
            keyboard.remove_hotkey(hotkey)

            # move units to group 9
            keyboard.send('ctrl+9')
            while threading.get_ident() in self.threads_flags[hotkey]:
                mouse.wait(button='left', target_types=('up',))
                if not threading.get_ident() in self.threads_flags[hotkey]:
                    break
                mouse_position_x, mouse_position_y = mouse.get_position()

                # click on first unit
                mouse.move(700, 900)
                mouse.click()

                # remove unit from group
                keyboard.send('alt+8')

                mouse.move(mouse_position_x, mouse_position_y)
                command()
                # choose remaining units
                keyboard.send('9')
        finally:
            # TODO move it to decorator
            keyboard.add_hotkey(hotkey, threading.Thread(target=self.send_command_to_units_by_one, args=(hotkey, command)).start)
