import os.path
from playsound import playsound

from sc2.utils import check_and_convert_templates
from sc2.numberparser import NumberParser


class IdleWorker(NumberParser):
    NAME = 'idle worker'

    HIGH = 10
    LEFT = 50
    RIGHT = 300 - 220 - 52 + LEFT
    UP = 750
    BOTTOM = UP + HIGH + 3 - 3

    COLOR_LIMITS = {
        'r': (255, 160),
        'g': (255, 160),
        'b': (255, 160),
    }

    TEMPLATES = {
        1: {'tmpl': [
            '0011',
            '0111',
            '1011',
            '0011',
            '0011',
            '0011',
            '0011',
            '0011',
            '0011',
            '0011'
        ], 'square': 40},
        2: {'tmpl': [
            '011110',
            '100001',
            '100001',
            '100001',
            '000001',
            '001111',
            '110000',
            '100000',
            '100000',
            '111111'
        ], 'square': 60},
        3: {'tmpl': [
            '0111110',
            '1000010',
            '1000010',
            '0000010',
            '0011110',
            '0000010',
            '0000001',
            '1000001',
            '1000010',
            '0111110'
        ], 'square': 70},
        4: {'tmpl': [
            '00000110',
            '00001110',
            '00010010',
            '00010010',
            '00100010',
            '01000010',
            '11000110',
            '11111111',
            '00000010',
            '00000010'
        ], 'square': 80},

        5: {'tmpl': [
            '1111110',
            '1000000',
            '1000000',
            '1111110',
            '1000010',
            '0000001',
            '0000001',
            '1000001',
            '1000010',
            '0111110'
        ], 'square': 70},
        6: {'tmpl': [
            '0111100',
            '1000010',
            '1000010',
            '1000000',
            '1111110',
            '1000010',
            '1000001',
            '1000001',
            '1000010',
            '0111110'
        ], 'square': 70},
        7: {'tmpl': [
            '111111',
            '000001',
            '000001',
            '000010',
            '000010',
            '000100',
            '000100',
            '001000',
            '011000',
            '010000'],
            'square': 60},
        8: {'tmpl': [
            '0111110',
            '1000010',
            '1000001',
            '1000010',
            '1111110',
            '1000010',
            '1000001',
            '1000001',
            '1000010',
            '0111110'
        ], 'square': 70},
        9: {'tmpl': [
            '0111110',
            '1000010',
            '1000001',
            '1000001',
            '1000011',
            '1111111',
            '0000001',
            '1000001',
            '1000010',
            '0111110'
        ], 'square': 70},
    }

    def __init__(self):
        super(IdleWorker, self).__init__()
        self.worker_count = []

    def parse_regions(self, image):
        pixels = self._get_pixels(image)
        self.worker_count = []
        n = []
        for i, col in enumerate(pixels):
            if not filter(None, pixels[i]):
                if n:
                    self.worker_count.append(self._parse_numbers(n))
                n = []
            else:
                n.append(pixels[i])

    def alarm(self):
        print('XAXAXA', self.worker_count)
        if self.worker_count and int(''.join(map(str, self.worker_count))) >= 2:
            playsound(os.path.join(os.path.dirname(__file__), 'resourses', 'too_many_idle_workers.mp3'))

# some check and convertation for tempates
check_and_convert_templates(IdleWorker)
