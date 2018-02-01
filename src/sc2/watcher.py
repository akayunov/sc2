import abc
import pyautogui
import traceback


class Watcher(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def name(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def parse_regions(self, image):
        raise NotImplementedError()

    @abc.abstractmethod
    def image_is_needed(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def alarm(self):
        raise NotImplementedError()


class WatcherProperties(object):
    def __init__(self, watcher, initial_alarm_period):
        self.watcher = watcher
        self.initial_alarm_period = initial_alarm_period
        self.curent_alarm_period = initial_alarm_period

    def run_watcher(self, image=None):
        if image is None and self.watcher.image_is_needed():
            image = pyautogui.screenshot()

        try:
            print('=' * 8, self.watcher.NAME, '=' * 8)
            self.watcher.parse_regions(image)
            if self.curent_alarm_period <= 0:
                self.watcher.alarm()
                self.watcher.curent_alarm_period = self.watcher.initial_alarm_period
                self.watcher.curent_alarm_period -= 1
        except Exception:
            print(traceback.format_exc())