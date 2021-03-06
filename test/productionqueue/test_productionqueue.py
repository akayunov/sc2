import os.path
import pytest
from PIL import Image

from sc2.productionqueue import ProductionQueue


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
    ]),
    ('3-line-full.png', [
        [254, 64, 64, 64, 64, 64, 64, 64],
        [254, 64, 64, 64, 64, 64, 64, 64],
        [64, 64, 64, 64, 64, 64, 64, 64],
        [64, 64, 64, 64, 64, 64, 64, 64],
        [64, 64, 64, 64, 64, 64, 64, 64],
        [64, 64, 64, 64, 64, 64, 64, 64],
        [64, 64, 64, 64, 64, 64, 64, 64],
        [64, 64, 64, 64, 64, 64, 64, 64],
        # second line
        [64, 64, 64, 64, 64, 64, 64, 64],
        [64, 64, 64, 64, 64],
        [64, 64, 64, 64, 64],
        [64, 64, 64, 64, 64],
        [64, 64, 64, 64, 64],
        [64, 64, 64, 64, 64],
        [64, 64, 64, 64, 64],
        [64, 64, 64, 64, 64],
    ]),
    ('many-baracs.png', [
        [254, 254, 254, 254, 64, 64, 64, 64],
        [254, 254, 254, 254, 64, 64, 64, 64],
        [254, 254, 254, 254, 254, 64, 64, 64],
        [254, 254, 254, 254, 64, 64, 64, 64],
        [254, 254, 254, 254, 64, 64, 64, 64],
        [254, 254, 64, 64, 64],
        [254, 254, 64, 64, 64],
        # second line
        [254, 254, 64, 64, 64],
        [254, 254, 64, 64, 64],
        [254, 254, 64, 64, 64],
        [254, 254, 64, 64, 64],
        [254, 64, 64, 64, 64],
        # third line
        [254, 64, 64, 64, 64],
        [254, 64, 64, 64, 64],
        [254, 64, 64, 64, 64],
        [254, 64, 64, 64, 64],
        [254, 64, 64, 64, 64],
        [254, 64, 64, 64, 64],
        [254, 64, 64, 64, 64]
    ]),
    ('1-barac-build-2-mar.png', [
        []
    ]),
    ('4-cc-csv-build.png', [[254, 254, 64, 64, 64], [254, 64, 64, 64, 64], [254, 64, 64, 64, 64]]),
    ('queue-is-overflowing.png', [[254, 254, 254, 64, 64], [254, 254, 254, 64, 64]]),
    ('many-starports.png', [[254, 64, 64, 64, 64],
                            [254, 64, 64, 64, 64],
                            [254, 64, 64, 64, 64],
                            [254, 64, 64, 64, 64],
                            [254, 64, 64, 64, 64],
                            [254, 64, 64, 64, 64],
                            [254, 64, 64, 64, 64],
                            [254, 64, 64, 64, 64],
                            [254, 64, 64, 64, 64],
                            [254, 64, 64, 64, 64]])

])
def test_production_queue(test_input, expected):
    production_queue = ProductionQueue()
    production_queue.parse_regions(Image.open(os.path.join(os.path.dirname(__file__), 'resourses', test_input)))
    assert expected == production_queue.production_queues
    assert production_queue.name() == 'production queue'
    assert production_queue.image_is_needed() is True
    production_queue.alarm()
