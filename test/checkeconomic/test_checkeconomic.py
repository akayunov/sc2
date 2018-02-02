import os.path
import pytest
from PIL import Image

from sc2.checkeconomic import CheckEconomic


@pytest.mark.parametrize("test_input, expected", [
    ('cc-0-worker.png', [0, '/', 1, 6]),
    ('cc-3-worker.png', [3, '/', 1, 6]),
    ('cc-4-worker.png', [4, '/', 1, 6]),
    ('cc-8-worker.png', [8, '/', 1, 6]),
    ('cc-9-worker.png', [9, '/', 1, 6]),
    ('cc-12-worker.png', [1, 2, '/', 1, 6]),
    ('cc-17-worker.png', [1, 7, '/', 1, 6]),
])
def test_check_economic_cc(test_input, expected):
    ce = CheckEconomic('cc')
    ce.parse_regions(Image.open(os.path.dirname(__file__) + '/resourses/' + test_input))
    assert expected == ce.worker_count
    # ce.alarm()


# TODO add gaz 4 worker
@pytest.mark.parametrize("test_input, expected", [
    ('gaz-2-worker.png', [2, '/', 3]),
    ('gaz-1-worker.png', [1, '/', 3])
])
def test_check_economic_gaz(test_input, expected):
    ce = CheckEconomic('gaz')
    ce.parse_regions(Image.open(os.path.dirname(__file__) + '/resourses/' + test_input))
    assert expected == ce.worker_count
    # ce.alarm()