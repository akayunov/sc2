import traceback
import time
import os.path

import sys
sys.path = [os.path.abspath(os.path.dirname(__file__) + '../../../src/')] + sys.path

import pyscreenshot as ps
from sasayblock import SasayBlock
from minimapwatcher import MiniMapWatcher

# check sasai block and resourses
sasay_block = SasayBlock()
sasay_block_alarm_period = 5  # seconds

# check minimap
minimap_watcher = MiniMapWatcher()
minimap_watcher_alarm_period = 5  # seconds

watchers = [[sasay_block, sasay_block_alarm_period], [minimap_watcher, minimap_watcher_alarm_period]]

while 1:
    time.sleep(1)
    im = ps.grab(childprocess=False)
    for watcher in watchers:
        try:
            print('=' * 8, watcher[0].NAME, '=' * 8)
            watcher[0].parse_regions(im)
            if watcher[1] <= 0:
                watcher[0].alarm()
                watcher[1] = 5
            watcher[1] -= 1
        except Exception as e:
            print(traceback.format_exc())
