import os.path
from copy import deepcopy
from playsound import playsound
from functools import partial

from sc2.watcher import Watcher


ONE = [
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
]
TWO = [
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
]
THREE = [
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

]
FOUR = [
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

]

FIVE = [
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

]
SIX = [
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

]
SEVEN = [
    '111111',
    '000001',
    '000001',
    '000010',
    '000010',
    '000100',
    '000100',
    '001000',
    '011000',
    '010000'
]
EIGHT = [
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

]
NINE = [
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
]


def _convert_by_diag(high, a):
    r = []
    for i in range(len(a[0])):
        r.append([int(a[k][i]) for k in range(high)])
    return r


class IdleWorker(Watcher):
    NAME = 'idle worker'
    # TODO improve for diff screen resolution
    HIGH = 10

    LEFT = 50
    RIGHT = 300 - 220 - 52 + LEFT
    UP = 750
    BOTTOM = UP + HIGH + 3 - 3

    ALL_NUMBERS = [ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE]

    NUMBERS_TEMPLATE = dict(
        zip(
            ['ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX', 'SEVEN', 'EIGHT', 'NINE'],
            zip(
                map(partial(_convert_by_diag, HIGH), ALL_NUMBERS),
                [1, 2, 3, 4, 5, 6, 7, 8, 9],
                [len(tp[0]) * HIGH for tp in ALL_NUMBERS]
            )
        )
    )

    def __init__(self):
        self.worker_count = []
        # check HIGH of all templ
        if filter(lambda x: len(x) != self.HIGH, self.ALL_NUMBERS):
            raise Exception()

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
                if r >= 160 and g >= 160 and b >= 160:
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

    def alarm(self):
        if int(''.join(self.worker_count)) >= 2:
            playsound(os.path.join(os.path.dirname(__file__), 'resourses', 'too_many_idle_workers.mp3'))
