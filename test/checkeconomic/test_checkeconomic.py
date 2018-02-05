import os.path
import pytest
from PIL import Image

from sc2.checkeconomic import CheckEconomic


@pytest.mark.parametrize("test_input, expected, missed_worker", [
    ('cc-0-worker.png', [0, '/', 1, 6], 16),
    ('cc-3-worker.png', [3, '/', 1, 6], 13),
    ('cc-4-worker.png', [4, '/', 1, 6], 12),
    ('cc-8-worker.png', [8, '/', 1, 6], 8),
    ('cc-9-worker.png', [9, '/', 1, 6], 7),
    ('cc-12-worker.png', [1, 2, '/', 1, 6], 4),
    ('cc-17-worker.png', [1, 7, '/', 1, 6], -1),
])
def test_check_economic_cc(test_input, expected, missed_worker):
    ce = CheckEconomic('cc')
    ce.parse_regions(Image.open(os.path.join(os.path.dirname(__file__), 'resourses', test_input)))
    assert expected == ce.worker_count
    assert missed_worker == ce.get_missed_worker()
    ce.alarm()


# TODO add gaz 4 worker
@pytest.mark.parametrize("test_input, expected, missed_worker", [
    ('gaz-2-worker.png', [2, '/', 3], 1),
    ('gaz-1-worker.png', [1, '/', 3], 2)
])
def test_check_economic_gaz(test_input, expected, missed_worker):
    ce = CheckEconomic('gaz')
    ce.parse_regions(Image.open(os.path.join(os.path.dirname(__file__), 'resourses', test_input)))
    assert expected == ce.worker_count
    assert missed_worker == ce.get_missed_worker()
    ce.alarm()


def test_check_economic_exc():
    with pytest.raises(Exception, match=r'Wrong build  type'):
        CheckEconomic('tratata')
