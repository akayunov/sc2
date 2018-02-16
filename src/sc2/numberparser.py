from copy import deepcopy

from sc2.watcher import Watcher


class NumberParser(Watcher):
    NAME = 'number watcher '

    LEFT = 0
    RIGHT = 0
    UP = 0
    BOTTOM = 0

    WEIGHT_ZERO_MATCH = 1
    WEIGHT_ONE_MATCH = 1.3

    HIGH = UP - BOTTOM
    COLOR_LIMITS = {
        'r': (0, 0),
        'g': (0, 0),
        'b': (0, 0),
    }
    TEMPLATES = {}

    def __init__(self):
        pass

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
                                        self.COLOR_LIMITS['r'][0] >= r >= self.COLOR_LIMITS['r'][1] and
                                        self.COLOR_LIMITS['g'][0] >= g >= self.COLOR_LIMITS['g'][1] and
                                        self.COLOR_LIMITS['b'][0] >= b >= self.COLOR_LIMITS['b'][1]
                ):
                    pixels[i][k] = 1
                else:
                    pixels[i][k] = 0
        return pixels

    def _count_similarity(self, got_number_array, templ):
        similarity = 0
        for i in range(min(len(got_number_array), len(templ))):
            for k in range(min(len(got_number_array[0]), len(templ[0]))):
                if got_number_array[i][k] == templ[i][k]:
                    similarity += self.WEIGHT_ZERO_MATCH if got_number_array[i][k] == 0 else self.WEIGHT_ONE_MATCH  # add weight for 1

        # check with shift if sizes is not equal
        n_templ = deepcopy(templ)
        while len(got_number_array) != len(n_templ):
            similarity_intermediate = 0
            if len(got_number_array) < len(n_templ):
                got_number_array = [[0] * self.HIGH] + got_number_array
            else:
                n_templ = [[0] * self.HIGH] + n_templ
            for i in range(min(len(got_number_array), len(n_templ))):
                for k in range(min(len(got_number_array[0]), len(n_templ[0]))):
                    if got_number_array[i][k] == n_templ[i][k]:
                        similarity_intermediate += self.WEIGHT_ZERO_MATCH if got_number_array[i][k] == 0 else self.WEIGHT_ONE_MATCH  # add weight for 1
            if similarity_intermediate > similarity:
                similarity = similarity_intermediate

        # devide on maximum pictures to avoid confusing with small templ like 1 with many zeros when zeros hit become bigger then 1 hit
        return float(similarity) / (self.HIGH * max([len(got_number_array), len(n_templ)]))

    def _parse_numbers(self, n_arr):
        result = [0, 0]
        for num_templ in self.TEMPLATES:
            similarity = self._count_similarity(n_arr, self.TEMPLATES[num_templ]['tmpl'])
            if similarity > result[0]:
                result = [similarity, num_templ]
        return result[1]

    def parse_regions(self, image):
        raise NotImplementedError()  # pragma: no cover

    def alarm(self):
        raise NotImplementedError()  # pragma: no cover
