import sys
import os.path
import pytest
from PIL import Image

sys.path = [os.path.abspath(os.path.dirname(__file__) + '../../../src/')] + sys.path
from sc2.minimapwatcher import MiniMapWatcher


@pytest.mark.parametrize("test_input, expected", [
    ('empty-mini-map.png', [0, 0, 0, 0, 0, 0, 0, 0, 0]),
    ('enemy-in-smog.png', [94, 0, 0, 0, 0, 0, 0, 0, 4]),
    ('visible-enimy.png', [17, 0, 0, 0, 0, 0, 0, 0, 0]),
    ('visible-units-by-units.png', [19, 0, 0, 0, 0, 0, 0, 0, 0])
])
def test_minimap_watcher(test_input, expected):
    minimap_watcher = MiniMapWatcher()
    minimap_watcher.parse_regions(Image.open(os.path.dirname(__file__) + '/resourses/' + test_input))
    assert expected == minimap_watcher.current_values
    # minimap_watcher.alarm()
