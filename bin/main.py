import traceback
import time
import os
import sys
import pyscreenshot as ps

sys.path = [os.path.abspath(os.path.dirname(__file__) + '/../src/')] + sys.path

from wsgiref.simple_server import make_server

from sc2.sasayblock import SasayBlock
from sc2.minimapwatcher import MiniMapWatcher
from sc2.productionqueue import ProductionQueue

# check sasai block and resourses
sasay_block = SasayBlock()
sasay_block_alarm_period = 5  # seconds

# check minimap
minimap_watcher = MiniMapWatcher()
minimap_watcher_alarm_period = 5  # seconds

watchers = [[sasay_block, sasay_block_alarm_period], [minimap_watcher, minimap_watcher_alarm_period]]

pid = os.fork()
if pid:
    # parent
    pass
else:
    # child
    # TODO may true daemonization ?
    production_queue_watcher = ProductionQueue()

    def simple_app(environ, start_response):
        status = '200 OK'
        headers = [('Content-type', 'text/plain')]
        start_response(status, headers)
        im = ps.grab(childprocess=False)
        production_queue_watcher.parse_regions(im)
        production_queue_watcher.alarm()
        return []


    httpd = make_server('', 8000, simple_app)
    print("Serving on port 8000...")
    httpd.serve_forever()


def start():
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
            except Exception:
                print(traceback.format_exc())


if __name__ == '__main__':
    try:
        start()
    except KeyboardInterrupt:
        # send kill don't need await
        os.kill(pid, 15)
        exit(1)
    except Exception:
        print(traceback.format_exc())
        exit(1)
    exit(0)
