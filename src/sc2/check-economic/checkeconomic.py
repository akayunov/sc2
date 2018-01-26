import sys
import os.path
import pytest
from PIL import Image

sys.path = [os.path.abspath(os.path.dirname(__file__) + '../../../')] + sys.path
import os
from sc2.utils import Watcher


class CheckEconomic(Watcher):
    NAME = 'minimapwatcher'
    # TODO improve for diff screen resolution
    LEFT = 980
    RIGHT = 60 + LEFT
    UP = 310
    BOTTOM = UP + 15

    def __init__(self):
        # TODO move to base class
        self.red_pixels = [None] * (self.RIGHT - self.LEFT)
        for p in range(self.RIGHT - self.LEFT):
            self.red_pixels[p] = [0] * (self.BOTTOM - self.UP)

    def name(self):
        return self.NAME

    # TODO move to base class
    def _get_pixels(self, image):
        im = image

        region = im.crop((self.LEFT, self.UP, self.RIGHT, self.BOTTOM))
        # region.show('xxx', 'eog')
        region.save('sb.png')

        rgb_im = region.convert('RGB')

        for j in range(self.RIGHT - self.LEFT):
            for k in range(self.BOTTOM - self.UP):
                r, g, b = rgb_im.getpixel((j, k))
                if r >= 191 and g == 0 and b == 0:
                    self.red_pixels[j][k] = 1
                else:
                    self.red_pixels[j][k] = 0

    def parse_regions(self, image):
        self._get_pixels(image)


    def alarm(self):
        pass



image = Image.open(os.path.dirname(__file__) + '/resourses/' + 'cc-on-center.png')
ce = CheckEconomic()
ce.parse_regions(image)

from sc2.utils import print_debug
from sc2.sasayblock import SasayBlock
SasayBlock.LEFT = 0
SasayBlock.UP = 0
SasayBlock.RIGHT = 500
SasayBlock.BOTTOM = 500
sb = SasayBlock()
print_debug(sb._get_pixels(image))