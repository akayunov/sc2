import sys
import os.path
import pytest
from PIL import Image

sys.path = [os.path.abspath(os.path.dirname(__file__) + '../../../src/')] + sys.path
from productionqueue import ProductionQueue


@pytest.mark.parametrize("test_input, expected", [
    ('factory-order.png', [
        [254, 254, 64, 64, 64, 64, 64, 64],
        [254, 64, 64, 64, 64, 64, 64, 64]
    ]),
    ('factory-order-queue.png', [
        [254, 254, 64, 64, 64, 64, 64, 64],
        [254, 64, 64, 64, 64, 64, 64, 64],
        [254, 254, 64, 64, 64]
    ]),
    ('factory-without-reactor.png', [
        [254, 254, 64, 64, 64, 64, 64, 64]
    ]),
    ('laboratory-building.png', [
        [254, 254, 64, 64, 64, 64, 64, 64],
        [254, 64, 64, 64, 64, 64, 64, 64]
    ])
])
def test_production_queue(test_input, expected):
    production_queue = ProductionQueue()
    production_queue.parse_regions(Image.open(os.path.dirname(__file__) + '/resourses/' + test_input))
    assert expected == production_queue.production_queues
    # for sound alarm do
    production_queue.alarm()
