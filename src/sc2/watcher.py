import abc
import traceback

from sc2.utils import get_screenshot


class Watcher(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def name(self):
        raise NotImplementedError()  # pragma: no cover

    @abc.abstractmethod
    def parse_regions(self, image):
        raise NotImplementedError()  # pragma: no cover

    @abc.abstractmethod
    def image_is_needed(self):
        raise NotImplementedError()  # pragma: no cover

    @abc.abstractmethod
    def alarm(self):
        raise NotImplementedError()  # pragma: no cover


class WatcherProperties(object):
    def __init__(self, watcher, initial_alarm_period=0):
        self.watcher = watcher
        self.initial_alarm_period = initial_alarm_period
        self.curent_alarm_period = initial_alarm_period

    def run_watcher(self, image=None):
        if image is None and self.watcher.image_is_needed():
            image = get_screenshot()
        try:
            print('=' * 8, self.watcher.NAME, '=' * 8)
            self.watcher.parse_regions(image)
            if self.curent_alarm_period <= 0:
                self.watcher.alarm()
                self.curent_alarm_period = self.initial_alarm_period
            self.curent_alarm_period -= 1
        except Exception:  # pragma: no cover
            print(traceback.format_exc())  # pragma: no cover
