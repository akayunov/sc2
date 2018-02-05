import os.path
from playsound import playsound

from sc2.numberparser import NumberParser
from sc2.utils import check_and_convert_templates


class SasayBlock(NumberParser):
    NAME = 'sasayblock'
    GAP_SIZE_BETWEEN_NUMBER_GROUP = 20

    LEFT = 1520
    RIGHT = 1870
    UP = 23
    BOTTOM = 33
    HIGH = BOTTOM - UP

    COLOR_LIMITS = {
        'r': (255, 235),
        'g': (255, 235),
        'b': (255, 235),
    }

    TEMPLATES = {
        0: {'tmpl': [
            '00001110000',
            '01111111110',
            '11000000011',
            '11000000011',
            '11000000011',
            '11000000011',
            '11000000011',
            '11000000011',
            '01111111110',
            '00001110000'
        ], 'square': 110},
        1: {'tmpl': [
            '00011',
            '00111',
            '11001',
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
            '00011111000',
            '01110000110',
            '01000000010',
            '00000000010',
            '00000111110',
            '00000000110',
            '00000000011',
            '11000000011',
            '01100000110',
            '00011111100'
        ], 'square': 110},
        4: {'tmpl': [
            '00000001100',
            '00000011100',
            '00001100100',
            '00011000100',
            '01100000100',
            '11000000100',
            '11000000110',
            '11111111111',
            '00000000100',
            '00000000100'
        ], 'square': 110},

        5: {'tmpl': [
            '1111111111',
            '1000000000',
            '1000000000',
            '1000000000',
            '1111111110',
            '0000000011',
            '0000000011',
            '1000000011',
            '1110000110',
            '0001111000'
        ], 'square': 100},
        6: {'tmpl': [
            '000111000',
            '111000111',
            '100000001',
            '100000000',
            '100011100',
            '111000011',
            '100000001',
            '100000001',
            '110000111',
            '000111000'
        ], 'square': 90},
        7: {'tmpl': [
            '11111111111',
            '11111111111',
            '00000000110',
            '00000001100',
            '00000001000',
            '00000011000',
            '00000110000',
            '00001100000',
            '00011000000',
            '00110000000'],
            'square': 110},
        8: {'tmpl': [
            '0011110000',
            '1100000110',
            '1000000010',
            '1000000010',
            '1111111110',
            '1100000110',
            '1000000011',
            '1000000011',
            '1100000110',
            '0011111100'
        ], 'square': 100},
        9: {'tmpl': [
            '00011111000',
            '01100001110',
            '01000000010',
            '01000000010',
            '01100000111',
            '00011100011',
            '00000000010',
            '11000000010',
            '01100001110',
            '00011110000'
        ], 'square': 110},
        '/': {'tmpl': [
            '000000001',
            '000000010',
            '000000100',
            '000001000',
            '000010000',
            '000100000',
            '000100000',
            '001000000',
            '010000000',
            '100000000'
        ], 'square': 90
        }
    }

    def __init__(self):
        super(SasayBlock, self).__init__()
        self.minerals = 0
        self.gas = 0
        self.supply = [0, 0]

    def parse_regions(self, image):
        pixels = self._get_pixels(image)
        numbers = []
        groups = []
        n = []
        gap_size = 0
        for i, col in enumerate(pixels):
            if not filter(None, pixels[i]):
                # find empty gap
                gap_size += 1
                if n:
                    numbers.append(self._parse_numbers(n))
                n = []
            else:
                n.append(pixels[i])
                gap_size = 0
            if gap_size > 10 and numbers:
                groups.append(numbers)
                numbers = []

        self.minerals = int(''.join(map(str, (groups[0]))))
        self.gas = int(''.join(map(str, (groups[1]))))
        self.supply = list(map(int, ''.join(map(str, (groups[2]))).split('/')))

    def alarm(self):
        if self.supply[1] < 200:
            if self.minerals > 500:
                playsound(os.path.join(os.path.dirname(__file__), 'resourses', 'too_many_minerals.mp3'))
            if self.gas > 500:
                playsound(os.path.join(os.path.dirname(__file__), 'resourses', 'too_many_vespen_gas.mp3'))
            if float(self.supply[1] - self.supply[0]) / self.supply[1] < 0.15:
                playsound(os.path.join(os.path.dirname(__file__), 'resourses', 'sasai_block.mp3'))


# some check and convertation for tempates
check_and_convert_templates(SasayBlock)
