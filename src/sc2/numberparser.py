import os.path
from copy import deepcopy
from playsound import playsound

from sc2.watcher import Watcher


class NumberParser(Watcher):
    NAME = 'sasayblock'
    GAP_SIZE_BETWEEN_NUMBER_GROUP = 20

    LEFT = 1520
    RIGHT = 1870
    UP = 23
    BOTTOM = 33
    HIGH = BOTTOM - UP

    COLOR_LIMITS = {
        'r': (0, 0),
        'g': (0, 0),
        'b': (0, 0),
    }
    TEMPLATES = {}

    def __init__(self):
        self.minerals = 0
        self.gas = 0
        self.supply = [0, 0]

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
                if ( self.COLOR_LIMITS['r'][0] >= r >= self.COLOR_LIMITS['r'][1] and self.COLOR_LIMITS['g'][0] >= g >= self.COLOR_LIMITS['g'][1]
                     and self.COLOR_LIMITS['b'][0] >= b >= self.COLOR_LIMITS['b'][1]):
                    pixels[i][k] = 1
                else:
                    pixels[i][k] = 0
        return pixels

    def _count_similarity(self, n_arr, num_templ):
        count = 0
        for i in range(min(len(n_arr), len(num_templ))):
            for k in range(min(len(n_arr[0]), len(num_templ[0]))):
                if n_arr[i][k] == num_templ[i][k]:
                    count += 1 if n_arr[i][k] == 0 else 1.3  # add weight for 1
        # check with shift if sizes is not equal
        n_templ = deepcopy(num_templ)
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
        for num_templ in self.TEMPLATES:
            # import pdb;pdb.set_trace()
            sim, symbol = self._count_similarity(n_arr, self.TEMPLATES[num_templ]['tmpl'])
            if sim > result[0]:
                result = [sim, num_templ]
        return result[1]

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
