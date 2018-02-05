import keyboard
import mouse
import threading
import thread
import os
from playsound import playsound

from sc2.productionqueue import ProductionQueue
from sc2.sasayblock import SasayBlock
from sc2.watcher import WatcherProperties
from sc2.utils import get_screenshot
from sc2.const import RESOLUTION


class KeyEventCommand:
    def __init__(self, map_info):
        self.map_info = map_info
        self.while_flag = False
        self.hotkey_occupy_expand = 'z+x'
        self.hotkey_send_command_to_units_by_one = '`'
        self.threads_flags = {self.hotkey_send_command_to_units_by_one: []}
        self.expand_flag = False
        keyboard.on_release(self.turn_off_threads_flags)

        # too noisy
        self.production_queue = ProductionQueue()
        production_queue_watcher_properties = WatcherProperties(self.production_queue, 0)
        #self.add_hotkey('3', production_queue_watcher_properties.run_watcher, in_own_thread=False)
        #self.add_hotkey('4', production_queue_watcher_properties.run_watcher, in_own_thread=False)
        #self.add_hotkey('5', production_queue_watcher_properties.run_watcher, in_own_thread=False)
        #self.add_hotkey('6', production_queue_watcher_properties.run_watcher, in_own_thread=False)
        # new expand
        self.add_hotkey(self.hotkey_occupy_expand, target=self.occupy_expand, args=(), timeout=1)
        self.add_hotkey('z+c', target=self.build_scv, args=(), timeout=1)
        # move commads
        self.add_hotkey(self.hotkey_send_command_to_units_by_one, target=self.send_command_to_units_by_one, args=(self.move_unit_command,), timeout=1)
        self.add_hotkey('w', target=self.send_command_to_units_by_one, args=(self.re_seige_tanks,), timeout=1)

    def add_hotkey(self, hotkey, target, args=(), timeout=0):
        keyboard.add_hotkey(
            hotkey, threading.Thread(target=target, args=([hotkey] + list(args))).start, suppress=False, timeout=timeout, trigger_on_release=False
        )

    def turn_off_threads_flags(self, event):
        if (event.name == 'x' and keyboard.is_pressed('z')) or (event.name == 'z' and keyboard.is_pressed('x')):
            self.threads_flags['z+x'] = []
        if (event.name == 'c' and keyboard.is_pressed('z')) or (event.name == 'z' and keyboard.is_pressed('c')):
            self.threads_flags['z+c'] = []
        if event.name == '`':
            self.threads_flags['`'] = []
        if event.name == 'esc':
            print('while flag turned off')
            self.while_flag = False
        if event.name == 'q':
            print('expad flag turned off')
            #q because esc is reserved for cansel build cc and I stil able to build only gazes
            self.expand_flag = False

    def occupy_expand(self, hotkey):
        keyboard.remove_hotkey('z+x')
        self.expand_flag = True
        import time
        mouse_position_x, mouse_position_y = mouse.get_position()
        resourses_group = self.map_info.get_nearest_exp_resourses_group(mouse_position_x, mouse_position_y)
        new_mouse_position_x, new_mouse_position_y = self.map_info.calculate_main_building_position(resourses_group)
        mouse.move(new_mouse_position_x, new_mouse_position_y)
        #time.sleep(1)
        mouse.click(button='left')  # move by minimap
        # we are in center of screen on new expand
        keyboard.send('0')  # choose worker
        # click on first unit
        #mouse.move(700, 900)
        # some exerimental things
        time.sleep(0.1)
        #time.sleep(1)
        #mouse.click()
        mouse.move(RESOLUTION.x / 2, RESOLUTION.y / 2)
        #time.sleep(1)
        keyboard.send('b')
        keyboard.send('c')
        if not self.expand_flag:
            self.add_hotkey('z+x', target=self.occupy_expand, args=(), timeout=1)
            return
        mouse.wait()  # build cc
        if not self.expand_flag:
            self.add_hotkey('z+x', target=self.occupy_expand, args=(), timeout=1)
            return
        # TODO move worker to minerals
        print('GAZES', resourses_group['gazes'])
        for i, gaz in enumerate(resourses_group['gazes']):
            new_mouse_position_x, new_mouse_position_y = self.map_info.get_item_coordinate_on_whole_screen(gaz)
            print('GAZ position', new_mouse_position_x, new_mouse_position_y)
            time.sleep(0.1)
            mouse.move(new_mouse_position_x, new_mouse_position_y)  # move by minimap
            time.sleep(0.1)
            mouse.click()
            #time.sleep(1)
        #    # we are in center of screen on new gaz
            keyboard.send('0')  # choose worker
            # click on first unit
            #print(700 + (i+1) * 50, 900)
            time.sleep(0.1)
            #mouse.move(700 + (i+1) * 50, 900)
            # some exerimental things        
            #time.sleep(0.1)
            #mouse.click()
            mouse.move(RESOLUTION.x / 2, RESOLUTION.y / 2)
            #time.sleep(1)
            keyboard.send('b')
            keyboard.send('r')
            if not self.expand_flag:
                self.add_hotkey('z+x', target=self.occupy_expand, args=(), timeout=1)
                return
            mouse.wait()  # build gazs6
            if not self.expand_flag:
                self.add_hotkey('z+x', target=self.occupy_expand, args=(), timeout=1)
                return
        self.add_hotkey('z+x', target=self.occupy_expand, args=(), timeout=1)

    def build_scv(self, hotkey):
        import time;
        keyboard.remove_hotkey(hotkey)
        sasayblock = SasayBlock()
        worker_counter = 22
        #worker_counter = 1
        # TODO check resourses before order to ensure that order will be done
        while 1:
            #playsound('C:\\sc2\\src\\sc2\\productionqueue\\resourses\\queue_is_overflowing.mp3')
            #i don't need screenshot to check building quue just now how many cc on map by parsing 
            # 6 group key and that all and d oorder after 12 sec
            # as close as posible to send "s" but before get screenshot, do I realy need scren shot I just need to know how many cc is exits
            # 
            image = get_screenshot()
            try:
                sasayblock.parse_regions(image)
            except Exception:
                pass
            # hot to disable right click in this time?
            #self.production_queue.parse_regions(get_screenshot())
            #aleady_building = 0
            #for cc in self.production_queue.production_queues:
            #    aleady_building += len(list(filter(lambda x: x == 254, cc)))
            #print(aleady_building, len(self.production_queue.production_queues))
            #worker_needed = len(self.production_queue.production_queues) * 2 - aleady_building
            # assume that we have 2 cc so we can order 2 worker
            worker_needed = 2
            worker_can_be_order_by_this_mineral_count = int(sasayblock.minerals/50)
            #break
            #time.sleep(0.1)
            keyboard.send('ctrl+0') # add curent selected to 0, for returning back
            keyboard.send('6')  
            for i in range(min(worker_can_be_order_by_this_mineral_count, worker_needed)):
                worker_counter -= 1
                keyboard.send('s')
                print('order done', worker_counter)
                if worker_counter <= 0:
                    break
            if worker_counter <= 0:
                break
            keyboard.send('0,0')
            time.sleep(12)
        keyboard.send('0,0')
        self.add_hotkey(hotkey, target=self.build_scv, args=(), timeout=1)

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
        # thread.get_ident() can be recycled by new thread but is doesn't matter because we always reinitialize it
        self.threads_flags[hotkey].append(thread.get_ident())
        keyboard.remove_hotkey(hotkey)
        keyboard.add_hotkey(hotkey, threading.Thread(target=self.send_command_to_units_by_one, args=(hotkey, command)).start)

        # move units to group 9
        keyboard.send('ctrl+9')
        while thread.get_ident() in self.threads_flags[hotkey]:
            mouse.wait(button='left', target_types=('up',))
            if not thread.get_ident() in self.threads_flags[hotkey]:
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
