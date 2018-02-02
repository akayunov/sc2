import os.path
import pytest
from PIL import Image

from sc2.sasayblock import SasayBlock


@pytest.mark.parametrize("test_input, expected", [
    ('1.png', [574, 0, [0, 15]]),
    ('3.png', [41, 0, [13, 15]]),
    ('4.png', [747, 2263, [108, 134]]),
    ('5.png', [931, 2320, [108, 134]]),
    ('many-starports.png', [3984, 81, [129, 200]]),
    ('cc-17-worker.png', [963, 0, [17, 23]])
])
def test_sasay_block(test_input, expected):
    sasay_block = SasayBlock()
    sasay_block.parse_regions(Image.open(os.path.dirname(__file__) + '/resourses/' + test_input))
    assert expected == [sasay_block.minerals, sasay_block.gas, sasay_block.supply]
    # for sound alarm do
    # sasay_block.alarm()
