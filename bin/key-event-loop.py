import traceback
import os
import sys
import keyboard
from sc2.utils import get_screenshot

sys.path = [os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))] + sys.path

from sc2.mapinfo import MapInfo
from sc2.keyeventcommand import KeyEventCommand


if __name__ == '__main__':
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
        exit(0)
    except Exception:
        print(traceback.format_exc())
        exit(1)
    exit(0)
