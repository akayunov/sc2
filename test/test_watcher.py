from sc2.idleworker import IdleWorker
from sc2.watcher import WatcherProperties


def test_watcher_properties():
    wp = WatcherProperties(IdleWorker(), 5)
    assert wp.initial_alarm_period == 5
    wp.run_watcher()
    wp.run_watcher()
    assert wp.curent_alarm_period == 3
    wp.run_watcher()
    wp.run_watcher()
    wp.run_watcher()
    assert wp.curent_alarm_period == 0
    wp.run_watcher()
    assert wp.curent_alarm_period == 4
