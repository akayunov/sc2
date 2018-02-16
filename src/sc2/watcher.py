import abc
import traceback

from sc2.utils import get_screenshot


class Watcher:
    __metaclass__ = abc.ABCMeta

    NAME = 'watcher'

    def name(self):
        return self.NAME

    @abc.abstractmethod
    def parse_regions(self, image):
        raise NotImplementedError()  # pragma: no cover

    @abc.abstractmethod
    def image_is_needed(self):
        raise NotImplementedError()  # pragma: no cover

    @abc.abstractmethod
    def alarm(self):
        raise NotImplementedError()  # pragma: no cover


class WatcherProperties:
    def __init__(self, watcher, initial_alarm_period=0):
        self.watcher = watcher
        self.initial_alarm_period = initial_alarm_period
        self.curent_alarm_period = initial_alarm_period

    def run_watcher(self, image=None):
        watcher_obj = self.watcher()
        if image is None and watcher_obj.image_is_needed():
            image = get_screenshot()
        try:
            print('=' * 8, watcher_obj.NAME, '=' * 8)
            watcher_obj.parse_regions(image)
            if self.curent_alarm_period <= 0:
                watcher_obj.alarm()
                self.curent_alarm_period = self.initial_alarm_period
            self.curent_alarm_period -= 1
        except Exception:  # pragma: no cover
            print(traceback.format_exc())  # pragma: no cover
