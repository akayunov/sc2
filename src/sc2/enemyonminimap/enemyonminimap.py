import os
from playsound import playsound
from sc2.watcher import Watcher


class EnemyOnMinimap(Watcher):
    NAME = 'minimap watcher'

    LEFT = 20
    RIGHT = 275 + LEFT
    UP = 805
    BOTTOM = UP + 275

    def __init__(self):
        self.previous_values = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.current_values = [0, 0, 0, 0, 0, 0, 0, 0, 0]

        self.red_pixels = [None] * (self.RIGHT - self.LEFT)
        for p in range(self.RIGHT - self.LEFT):
            self.red_pixels[p] = [0] * (self.BOTTOM - self.UP)

    def name(self):
        return self.NAME

    def image_is_needed(self):
        return True

    def _get_pixels(self, image):
        im = image

        region = im.crop((self.LEFT, self.UP, self.RIGHT, self.BOTTOM))
        # region.show('xxx', 'eog')
        # region.save('sb.png')

        for j in range(self.RIGHT - self.LEFT):
            for k in range(self.BOTTOM - self.UP):
                r, g, b = region.getpixel((j, k))
                if r >= 191 and g == 0 and b == 0:
                    self.red_pixels[j][k] = 1
                else:
                    self.red_pixels[j][k] = 0

    def parse_regions(self, image):
        self._get_pixels(image)
        self.previous_values = self.current_values
        result = []
        one_third_part = int(len(self.red_pixels) / 3)
        two_third_part = int(len(self.red_pixels) / 3) * 2

        for start_col in [0, one_third_part, two_third_part]:
            for start_el in [0, one_third_part, two_third_part]:
                qudrant_count = 0
                for z in range(start_col, start_col + one_third_part):
                    for k in range(start_el, start_el + one_third_part):
                        qudrant_count += self.red_pixels[k][z]
                result.append(qudrant_count)

        self.current_values = result

    def alarm(self):
        for k in range(1, 1 + len(self.current_values)):
            if self.previous_values[k - 1] < self.current_values[k - 1]:
                playsound(os.path.join(os.path.dirname(__file__), 'resourses', 'enemy_in_' + str(k) + '_sector.mp3'))
