import os.path
import pytest
from PIL import Image

from sc2.grouphealth import GroupHealth


@pytest.mark.parametrize("test_input, expected_subgroup_count, units", [
    ('3-line-full.png', {0: (651, 902.0), 1: (651, 932.0)},
     {
         'red': [(746.5, 972.5), (803.5, 972.5)],
         'orange': [(860.5, 972.5), (917.5, 972.5), (974.5, 972.5), (1031.5, 972.5), (1088.5, 972.5), (689.5, 1029.5)],
         'yellow': [],
         'green': [(689.5, 915.5), (746.5, 915.5), (803.5, 915.5), (860.5, 915.5), (917.5, 915.5), (974.5, 915.5), (1031.5, 915.5), (1088.5, 915.5),
                   (689.5, 972.5), (746.5, 1029.5), (803.5, 1029.5), (860.5, 1029.5), (917.5, 1029.5), (974.5, 1029.5), (1031.5, 1029.5), (1088.5, 1029.5)],
     }),
    ('factory-order.png', {0: (651, 902.0)},
     {
         'green': [(689.5, 915.5), (746.5, 915.5)],
         'orange': [(803.5, 915.5)],
         'red': [],
         'yellow': []
     }
     ),
])
def test_group_health(test_input, expected_subgroup_count, units):
    gh = GroupHealth()
    image = Image.open(os.path.join(os.path.dirname(__file__), 'resourses', test_input))
    gh.parse_regions(image)
    assert expected_subgroup_count == gh.get_subgroup_count(image)
    assert gh.units == units
    gh.alarm()
