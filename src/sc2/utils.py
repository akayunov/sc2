import abc
import sys


def print_debug(pixels_):
    for ii in range(len(pixels_[0])):
        for kk in range(len(pixels_)):
            sys.stdout.write(str(pixels_[kk][ii]))
        sys.stdout.write('\n')


class Watcher(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def name(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def parse_regions(self, image):
        raise NotImplementedError()

    @abc.abstractmethod
    def alarm(self):
        raise NotImplementedError()


class WatcherProperties(object):
    def __init__(self, watcher, initial_alarm_period):
        self.watcher = watcher
        self.initial_alarm_period = initial_alarm_period
        self.curent_alarm_period = initial_alarm_period
