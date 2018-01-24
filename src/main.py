import traceback
import time

import pyscreenshot as ps
from .sasaiblock import sasaiblock
from .minimapwatcher import MiniMapWatcher

minimap_watcher_alarm_period = 5  # seconds

while 1:
    time.sleep(1)
    im = ps.grab(childprocess=False)
    # check sasai block and resourses
    try:
        pass
        # pixels = sasaiblock.get_pixels(im)
        # print(sasaiblock.get_numbers(pixels))
    except Exception as e:
        print(traceback.format_exc())

    # check minimap
    try:
        minimap_watcher = MiniMapWatcher()
        minimap_watcher.parse_regions(im)
        if minimap_watcher_alarm_period <= 0:
            minimap_watcher.alarm()
            minimap_watcher_alarm_period = 5
        minimap_watcher_alarm_period -= 1
    except Exception as e:
        print(traceback.format_exc())
