import os.path
from playsound import playsound
from copy import deepcopy
from functools import partial

from sc2.watcher import Watcher


ZERO = [
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

]
ONE = [
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
]
TWO = [
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
]
THREE = [
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
]
FOUR = [
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
]

FIVE = [
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
]
SIX = [
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

]
SEVEN = [
    '1111111111',
    '0000000001',
    '0000000010',
    '0000000110',
    '0000000100',
    '0000001000',
    '0000010000',
    '0000100000',
    '0001000000',
    '0011000000'
]
EIGHT = [
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
]
NINE = [
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
]
SLASH = [
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
]


def _convert_by_diag(high, a):
    r = []
    for i in range(len(a[0])):
        r.append([int(a[k][i]) for k in range(high)])
    return r


class CheckEconomic(Watcher):
    NAME = 'check economic'
    # TODO improve for diff screen resolution
    HIGH = 10

    CC_LEFT = 983
    CC_RIGHT = 70 + CC_LEFT
    CC_UP = 313
    CC_BOTTOM = CC_UP + HIGH

    GAZ_LEFT = 993
    GAZ_RIGHT = GAZ_LEFT + 40
    GAZ_UP = 318
    GAZ_BOTTOM = GAZ_UP + HIGH

    ALL_NUMBERS = [ZERO, ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, SLASH]

    NUMBERS_TEMPLATE = dict(
        zip(
            ['ZERO', 'ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX', 'SEVEN', 'EIGHT', 'NINE', 'SLASH'],
            zip(
                map(partial(_convert_by_diag, HIGH), ALL_NUMBERS),
                [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, '/'],
                [len(tp[0]) * HIGH for tp in ALL_NUMBERS]
            )
        )
    )

    def __init__(self, build_type):
        self.worker_count = []
        # check HIGH of all templ
        if filter(lambda x: len(x) != self.HIGH, self.ALL_NUMBERS):
            raise Exception()
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

    def name(self):
        return self.NAME

    def image_is_needed(self):
        return True

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

    def _count_similarity(self, n_arr, num_templ):
        count = 0
        for i in range(min(len(n_arr), len(num_templ[0]))):
            for k in range(min(len(n_arr[0]), len(num_templ[0][0]))):
                if n_arr[i][k] == num_templ[0][i][k]:
                    count += 1 if n_arr[i][k] == 0 else 1.3  # add weight for 1
        # check with shift if sizes is not equal
        n_templ = deepcopy(num_templ[0])
        while len(n_arr) != len(n_templ):
            count_intermediate = 0
            if len(n_arr) < len(n_templ):
                n_arr = [[0] * self.HIGH] + n_arr
            else:
                n_templ = [[0] * self.HIGH] + n_templ
            for i in range(min(len(n_arr), len(n_templ))):
                for k in range(min(len(n_arr[0]), len(n_templ[0]))):
                    if n_arr[i][k] == n_templ[i][k]:
                        count_intermediate += 1 if n_arr[i][k] == 0 else 1.5  # add weight for 1
            if count_intermediate > count:
                count = count_intermediate

        # devide on maximum pictures to avoid confusing with small templ like 1 with many zeros when zeros hit become bigger then 1 hit
        return float(count) / (self.HIGH * max([len(n_arr), len(n_templ)])), num_templ[1]

    def _parse_numbers(self, n_arr):
        result = [0, 0]
        for num_templ in self.NUMBERS_TEMPLATE:
            sim, symbol = self._count_similarity(n_arr, self.NUMBERS_TEMPLATE[num_templ])
            if sim > result[0]:
                result = [sim, symbol]
        return result[1]

    def parse_regions(self, image):
        pixels = self._get_pixels(image)
        n = []
        for i, col in enumerate(pixels):
            if not filter(None, pixels[i]):
                if n:
                    self.worker_count.append(self._parse_numbers(n))
                n = []
            else:
                n.append(pixels[i])

    def get_missed_worker(self):
        # [1, 2, '/', 1, 6]
        return map(int, ''.join(self.worker_count).split('/'))

    def alarm(self):
        playsound(os.path.join(os.path.dirname(__file__), 'resourses', 'change_control_in_5_sec.mp3'))
