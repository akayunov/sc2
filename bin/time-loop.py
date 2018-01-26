import traceback
import time
import os
import sys
import pyautogui as pag

sys.path = [os.path.abspath(os.path.dirname(__file__) + '/../src/')] + sys.path

from sc2.sasayblock import SasayBlock
from sc2.minimapwatcher import MiniMapWatcher
from sc2.productionqueue import ProductionQueue


def start_background():
    # check sasai block and resourses
    sasay_block = SasayBlock()
    sasay_block_alarm_period = 5  # seconds

    # check minimap
    minimap_watcher = MiniMapWatcher()
    minimap_watcher_alarm_period = 5  # seconds

    # check production queue if can
    production_queue = ProductionQueue()
    production_queue_alarm_period = 5

    watchers = [[sasay_block, sasay_block_alarm_period], [minimap_watcher, minimap_watcher_alarm_period],
                [production_queue, production_queue_alarm_period]]
    while 1:
        time.sleep(0.5)
        im = pag.screenshot()
        for watcher in watchers:
            try:
                print('=' * 8, watcher[0].NAME, '=' * 8)
                watcher[0].parse_regions(im)
                if watcher[1] <= 0:
                    watcher[0].alarm()
                    watcher[1] = 5
                watcher[1] -= 1
            except Exception:
                print(traceback.format_exc())


if __name__ == '__main__':
    try:
        start_background()
    except KeyboardInterrupt:
        exit(0)
    except Exception:
        print(traceback.format_exc())
        exit(1)
    exit(0)
