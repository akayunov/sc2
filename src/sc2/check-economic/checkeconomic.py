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
    UP = 313
    BOTTOM = UP + 10

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
                if 200 >= r >= 160 and 200 >= g >= 160 and 200 >= b >= 160:
                    self.red_pixels[j][k] = 1
                else:
                    self.red_pixels[j][k] = 0

    def parse_regions(self, image):
        self._get_pixels(image)


    def alarm(self):
        pass


from sc2.sasayblock import SasayBlock
from sc2.utils import print_debug
SasayBlock.LEFT = 980
SasayBlock.RIGHT = 60 + 980
SasayBlock.UP = 313
SasayBlock.BOTTOM = 313 + 10

image = Image.open(os.path.dirname(__file__) + '/resourses/' + 'cc-on-center.png')
ce = CheckEconomic()
ce._get_pixels(image)
print_debug(ce.red_pixels)
# ce.parse_regions(image)

sb = SasayBlock()
sb.parse_regions(image)




