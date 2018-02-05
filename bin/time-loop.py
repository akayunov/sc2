import traceback
import time
import os
import sys
import mouse
import keyboard

sys.path = [os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))] + sys.path

from sc2.utils import get_screenshot
from sc2.mapinfo import MapInfo
from sc2.sasayblock import SasayBlock
from sc2.minimapwatcher import MiniMapWatcher
from sc2.idleworker import IdleWorker
from sc2.checkeconomic import CheckEconomic
from sc2.watcher import WatcherProperties


if __name__ == '__main__':
    try:
        map_info = MapInfo()
        watchers = [
            WatcherProperties(SasayBlock, 5), WatcherProperties(MiniMapWatcher, 1), WatcherProperties(IdleWorker, 5)
        ]
        # economic_checkers = [
        #     WatcherProperties(CheckEconomic('cc'), 30),
        #     WatcherProperties(CheckEconomic('gaz'), 30)
        # ]

        while 1:
            time.sleep(1)
            im = get_screenshot()
            for watcher in watchers:
                watcher.run_watcher(image=im)

                # for watcher in economic_checkers:
                #     try:
                #         print('=' * 8, watcher.watcher.NAME, '=' * 8)
                #         if watcher.curent_alarm_period <= 0:
                #             watcher.watcher.alarm()
                #             # TODO implement
                #             # for position in map_info.get_positions():
                #             #     # move by minimap
                #             #     mouse.move(*position)
                #             #     # move to screen center
                #             #     mouse.move(RESOLUTION.x/2, RESOLUTION.y/2)
                #             #     mouse.click()
                #             #     # center by building
                #             #     keyboard.send('ctrl+f')
                #             #     watcher.watcher.parse_regions(im)
                #             #     watcher.watcher.get_missed_worker()
                #             #     put workers from minerals to gaz
                #             #     order new worker
                #             watcher.curent_alarm_period = watcher.initial_alarm_period
                #         watcher.curent_alarm_period -= 1
                #     except Exception:
                #         print(traceback.format_exc())
    except KeyboardInterrupt:
        exit(0)
    except Exception:
        print(traceback.format_exc())
        exit(1)
    exit(0)
