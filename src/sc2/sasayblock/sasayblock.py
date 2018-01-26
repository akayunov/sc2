import os.path
from copy import deepcopy
from playsound import playsound
from sc2.utils import Watcher
from functools import partial

ZERO = [
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
]
ONE = [
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
]
FOUR = [
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
]

FIVE = [
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
]
SIX = [ # TODO
    '110000000',
    '111000111',
    '100000001',
    '100000000',
    '100011100',
    '111000011',
    '100000001',
    '100000001',
    '110000111',
    '000111100'
]
SEVEN = [
    '11111111111',
    '11111111111',
    '00000000110',
    '00000001100',
    '00000001000',
    '00000011000',
    '00000110000',
    '00001100000',
    '00011000000',
    '00110000000']
EIGHT = [
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
]
NINE = [
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
]
SLASH = [
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
]


def _convert_by_diag(high, a):
    r = []
    for i in range(len(a[0])):
        r.append([int(a[k][i]) for k in range(high)])
    return r


class SasayBlock(Watcher):
    NAME = 'sasayblock'
    GAP_SIZE_BETWEEN_NUMBER_GROUP = 20
    # TODO improve for diff screen resolution
    LEFT = 1520
    RIGHT = 1870
    UP = 23
    BOTTOM = 33
    HIGH = BOTTOM - UP

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

    def __init__(self):
        self.minerals = 0
        self.gas = 0
        self.supply = [0, 0]
        # check HIGH of all templ
        if filter(lambda x: len(x) != self.HIGH, self.ALL_NUMBERS):
            raise Exception()

    def name(self):
        return self.NAME

    def _get_pixels(self, image):
        region = image.crop((self.LEFT, self.UP, self.RIGHT, self.BOTTOM))
        # region.show('xxx', 'eog')
        # region.save('sb.png')

        rgb_im = region.convert('RGB')
        pixels = [None] * (self.RIGHT - self.LEFT)
        for i in range(self.RIGHT - self.LEFT):
            pixels[i] = [0] * (self.BOTTOM - self.UP)
        for i in range(self.RIGHT - self.LEFT):
            for k in range(self.BOTTOM - self.UP):
                r, g, b = rgb_im.getpixel((i, k))
                if r >= 235 and g >= 235 and b >= 235:
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
        from sc2.utils import print_debug
        print_debug(pixels)
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
        print(groups)
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
