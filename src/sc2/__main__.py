import argparse
import traceback
import time
import keyboard

from sc2.utils import get_screenshot
from sc2.mapinfo import MapInfo
from sc2.sasayblock import SasayBlock
from sc2.enemyonminimap import EnemyOnMinimap
from sc2.idleworker import IdleWorker
from sc2.watcher import WatcherProperties
from sc2.keyeventcommand import KeyEventCommand


parser = argparse.ArgumentParser(description='Sc2 game assistant')
parser.add_argument('-t', '--time-watchers', action='store_true', help='Start time event watchers')
parser.add_argument('-k', '--key-event-command', action='store_true', help='Start key events command')
args = parser.parse_args()


if args.key_event_command:
    print('Press "s" to start')
    keyboard.wait('s')
    print('Started')
    map_info = MapInfo()
    image = get_screenshot()
    map_info.parse_regions(image)
    kec = KeyEventCommand(map_info)
    try:
        keyboard.wait()
    except KeyboardInterrupt:
        print('Finished')
        exit(0)
    except Exception:
        print(traceback.format_exc())
        exit(1)
    print('Finished')
    exit(0)
elif args.time_watchers:
    try:
        map_info = MapInfo()
        watchers = [
            WatcherProperties(SasayBlock, 5), WatcherProperties(EnemyOnMinimap, 1), WatcherProperties(IdleWorker, 5)
        ]
        while 1:
            time.sleep(1)
            im = get_screenshot()
            for watcher in watchers:
                watcher.run_watcher(image=im)
    except KeyboardInterrupt:
        print('Finished')
        exit(0)
    except Exception:
        print(traceback.format_exc())
        exit(1)
    print('Finished')
    exit(0)
else:
    print('Finished')
    exit(0)
