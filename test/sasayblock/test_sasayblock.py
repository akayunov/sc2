import sys
import os.path
import pytest
from PIL import Image

sys.path = [os.path.abspath(os.path.dirname(__file__) + '../../../src/')] + sys.path
from minimapwatcher import MiniMapWatcher


@pytest.mark.parametrize("test_input, expected", [
    ('sc.png', [574, 0, 0, 15]),
])
def test_sasay_block(test_input, expected):
    pass
    # minimap_watcher = MiniMapWatcher()
    # minimap_watcher.parse_regions(Image.open(os.path.dirname(__file__) + '/resourses/' + test_input))
    # assert expected == minimap_watcher.current_values
    # for sound alarm do
    # minimap_watcher.alarm()
