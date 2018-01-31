import sys
import os.path
import pytest
from PIL import Image

sys.path = [os.path.abspath(os.path.dirname(__file__) + '../../../src/')] + sys.path
from sc2.idleworker import IdleWorker


@pytest.mark.parametrize("test_input, expected", [
    ('cc-3-worker.png', [9]),
    ('cc-4-worker.png', [8]),
    ('cc-5-worker.png', [7]),
    ('cc-6-worker.png', [6]),
    ('cc-7-worker.png', [5]),
    ('cc-8-worker.png', [4]),
    ('cc-9-worker.png', [3]),
    ('cc-10-worker.png', [2]),
    ('cc-12-worker.png', [1]),
    ('cc-16-worker.png', []),
])
def test_idle_worker(test_input, expected):
    iw = IdleWorker()
    iw.parse_regions(Image.open(os.path.dirname(__file__) + '/resourses/' + test_input))
    assert expected == iw.worker_count
    # iw.alarm()
