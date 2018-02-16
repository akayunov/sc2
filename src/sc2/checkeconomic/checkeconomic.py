import os.path
from playsound import playsound

from sc2.utils import check_and_convert_templates
from sc2.numberparser import NumberParser


class CheckEconomic(NumberParser):
    NAME = 'check economic'

    HIGH = 10

    CC_LEFT = 983
    CC_RIGHT = 70 + CC_LEFT
    CC_UP = 313
    CC_BOTTOM = CC_UP + HIGH

    GAZ_LEFT = 993
    GAZ_RIGHT = GAZ_LEFT + 40
    GAZ_UP = 318
    GAZ_BOTTOM = GAZ_UP + HIGH

    TEMPLATES = {
        0: {'tmpl': [
            '01111111100',
            '11000000010',
            '10000000011',
            '10000000001',
            '10000000001',
            '10000000001',
            '10000000001',
            '10000000001',
            '11000000010',
            '01111111100'
        ], 'square': 110},
        1: {'tmpl': [
            '00011',
            '00111',
            '01001',
            '10001',
            '00001',
            '00001',
            '00001',
            '00001',
            '00001',
            '00001'
        ], 'square': 50},
        2: {'tmpl': [
            '00001111000',
            '01110000110',
            '01000000011',
            '00000000011',
            '00000000010',
            '00111111110',
            '01100000000',
            '01000000000',
            '11000000000',
            '11111111111'
        ], 'square': 110},
        3: {'tmpl': [
            '0011111110',
            '1100000001',
            '1000000001',
            '0000000001',
            '0000111111',
            '0000000001',
            '0000000001',
            '1000000001',
            '1100000001',
            '0111111110'
        ], 'square': 100},
        4: {'tmpl': [
            '00000001100',
            '00000011100',
            '00000100100',
            '00001000100',
            '00110000100',
            '01100000100',
            '11000000100',
            '11111111111',
            '00000000100',
            '00000000100'
        ], 'square': 110},

        5: {'tmpl': [
            '11111111110',
            '11000000000',
            '10000000000',
            '11111111100',
            '11000000010',
            '00000000011',
            '00000000001',
            '10000000011',
            '11000000010',
            '01111111100'
        ], 'square': 110},
        6: {'tmpl': [
            '0011111110',
            '0100000001',
            '1100000001',
            '1000000000',
            '1011111110',
            '1100000001',
            '1000000001',
            '1000000001',
            '0100000001',
            '0011111110'
        ], 'square': 100},
        7: {'tmpl': [
            '1111111111',
            '0000000001',
            '0000000010',
            '0000000110',
            '0000000100',
            '0000001000',
            '0000010000',
            '0000100000',
            '0001000000',
            '0011000000'],
            'square': 100},
        8: {'tmpl': [
            '0111111110',
            '1100000001',
            '1000000001',
            '1100000001',
            '0111111111',
            '1100000001',
            '1000000001',
            '1000000001',
            '1100000001',
            '0111111110'
        ], 'square': 100},
        9: {'tmpl': [
            '0011111110',
            '0100000001',
            '1000000001',
            '1000000001',
            '1100000001',
            '0111111101',
            '0000000001',
            '1000000001',
            '0100000001',
            '0011111110'
        ], 'square': 100},
        '/': {'tmpl': [
            '00000001',
            '00000001',
            '00000010',
            '00000100',
            '00001000',
            '00010000',
            '00100000',
            '01000000',
            '01000000',
            '10000000'
        ], 'square': 80
             }
    }

    def __init__(self, build_type):
        super(CheckEconomic, self).__init__()
        self.worker_count = []
        if build_type == 'cc':
            self.LEFT = CheckEconomic.CC_LEFT
            self.RIGHT = CheckEconomic.CC_RIGHT
            self.UP = CheckEconomic.CC_UP
            self.BOTTOM = CheckEconomic.CC_BOTTOM
        elif build_type == 'gaz':
            self.LEFT = CheckEconomic.GAZ_LEFT
            self.RIGHT = CheckEconomic.GAZ_RIGHT
            self.UP = CheckEconomic.GAZ_UP
            self.BOTTOM = CheckEconomic.GAZ_BOTTOM
        else:
            raise Exception('Wrong build  type')

    def _get_pixels(self, image):
        region = image.crop((self.LEFT, self.UP, self.RIGHT, self.BOTTOM))
        # region.show('xxx', 'eog')
        # region.save('sb.png')

        pixels = [None] * (self.RIGHT - self.LEFT)
        for i in range(self.RIGHT - self.LEFT):
            pixels[i] = [0] * (self.BOTTOM - self.UP)
        for i in range(self.RIGHT - self.LEFT):
            for k in range(self.BOTTOM - self.UP):
                r, g, b = region.getpixel((i, k))
                if (
                        # white
                        (200 >= r >= 160 and 200 >= g >= 160 and 200 >= b >= 160) or
                        # red
                        (195 >= r >= 190 and 40 >= g >= 30 and 40 >= b >= 30)
                ):
                    pixels[i][k] = 1
                else:
                    pixels[i][k] = 0
        return pixels

    def parse_regions(self, image):
        pixels = self._get_pixels(image)
        n = []
        for i, _ in enumerate(pixels):
            if not [k for k in pixels[i] if bool(k)]:
                if n:
                    self.worker_count.append(self._parse_numbers(n))
                n = []
            else:
                n.append(pixels[i])

    def get_missed_worker(self):
        worked, needed = map(int, ''.join(map(str, self.worker_count)).split('/'))
        return needed - worked

    def alarm(self):
        playsound(os.path.join(os.path.dirname(__file__), 'resourses', 'change_control_in_5_sec.mp3'))

# some check and convertation for tempates
check_and_convert_templates(CheckEconomic)
