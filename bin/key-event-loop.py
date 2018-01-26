import traceback
import os
import sys
import pyautogui as pag
import keyboard

sys.path = [os.path.abspath(os.path.dirname(__file__) + '/../src/')] + sys.path

from sc2.productionqueue import ProductionQueue

# check production queue if can
production_queue = ProductionQueue()


def run_watcher(watcher):
    im = pag.screenshot()
    try:
        print('=' * 8, watcher.NAME, '=' * 8)
        watcher.parse_regions(im)
        if watcher <= 0:
            watcher.alarm()
            watcher = 5
        watcher -= 1
    except Exception:
        print(traceback.format_exc())


if __name__ == '__main__':
    try:
        keyboard.add_hotkey('3', run_watcher, args=(production_queue,), suppress=False, timeout=0.5, trigger_on_release=False)
        keyboard.add_hotkey('4', run_watcher, args=(production_queue,), suppress=False, timeout=0.5, trigger_on_release=False)
        keyboard.add_hotkey('5', run_watcher, args=(production_queue,), suppress=False, timeout=0.5, trigger_on_release=False)
        keyboard.add_hotkey('6', run_watcher, args=(production_queue,), suppress=False, timeout=0.5, trigger_on_release=False)
        keyboard.wait()
    except KeyboardInterrupt:
        exit(0)
    except Exception:
        print(traceback.format_exc())
        exit(1)
    exit(0)
