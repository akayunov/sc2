import traceback
import time
import os
import sys

sys.path = [os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))] + sys.path

from sc2.utils import get_screenshot
from sc2.mapinfo import MapInfo
from sc2.sasayblock import SasayBlock
from sc2.enemyonminimap import EnemyOnMinimap
from sc2.idleworker import IdleWorker
from sc2.watcher import WatcherProperties


if __name__ == '__main__':
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
        exit(0)
    except Exception:
        print(traceback.format_exc())
        exit(1)
    exit(0)
