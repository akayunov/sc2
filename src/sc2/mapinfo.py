from copy import deepcopy
from functools import partial
from sc2.utils import Watcher


class MapInfo(Watcher):
    NAME = 'map info'
    # TODO improve for diff screen resolution
    LEFT = 20
    RIGHT = 275 + LEFT
    UP = 805
    BOTTOM = UP + 275

    def __init__(self):
        self.minimap = {'gazes': [], 'minerals': []}
        self.expand_groups = []
        # TODO move to base class
        self.blue_pixels = [None] * (self.RIGHT - self.LEFT)
        for p in range(self.RIGHT - self.LEFT):
            self.blue_pixels[p] = [0] * (self.BOTTOM - self.UP)

    def name(self):
        return self.NAME

    def alarm(self):
        pass

    # TODO move to base class
    def _get_pixels(self, image):
        im = image

        region = im.crop((self.LEFT, self.UP, self.RIGHT, self.BOTTOM))
        # region.show('xxx', 'eog')
        # region.save('sb.png')

        for j in range(self.RIGHT - self.LEFT):
            for k in range(self.BOTTOM - self.UP):
                r, g, b = region.getpixel((j, k))
                if r == 126 and g == 191 and b == 241:
                    self.blue_pixels[j][k] = 1
                else:
                    self.blue_pixels[j][k] = 0

    def check_blue_region(self, x, y, size):
        # YOU NEED TO CHECK GAZ FIRST BECAUSE IT HAVE A BIGGER SQUARE
        # b b
        # b b
        # we are in left - up b so to check minerals we need to check x + 1, y; y+1,x; y+1,x+1 but size = 2, so we need to decrease size by 1
        # it suitable for gas with size 6 too
        square = size * size  # wish object square
        size = size - 1
        counter_square = 0  # counted object square

        # let's think what x + size + 1 and y + size + 1 is always exists
        for xi in range(x, x + size + 1):  # +1 because we start from 1 not 0
            for yi in range(y, y + size + 1):  # +1 because we start from 1 not 0
                counter_square += self.blue_pixels[xi][yi]
        if counter_square == square:
            # remove this blue pixels for don't check it again in next iteration
            # only for gasez because mineral can have a common border see test two-expand.png
            if size == 5:
                for xi in range(x, x + size + 1):
                    for yi in range(y, y + size + 1):
                        self.blue_pixels[xi][yi] = 0

            return True
        return False

    def parse_regions(self, image):
        self._get_pixels(image)
        for j in range(self.RIGHT - self.LEFT):
            for k in range(self.BOTTOM - self.UP):
                if self.blue_pixels[j][k] == 1:
                    if self.check_blue_region(j, k, 6):
                        # gaz is found, save "up - left" corner as it coordinates
                        self.minimap['gazes'].append((self.LEFT + j, self.UP + k))
                    elif self.check_blue_region(j, k, 2):
                        # mineral is found, save "up - left" corner as it coordinates
                        self.minimap['minerals'].append((j, k))

        self.group_resources_by_expand()
        self.calculate_main_build_position()

    def group_resources_by_expand(self):
        # if distance between object smaller then 4 all of them in one expand group
        minerals = deepcopy(self.minimap['minerals'])
        while minerals:
            group = []
            mineral_base = minerals.pop()
            group.append(mineral_base)
            item_was_added = 1
            while item_was_added:
                item_was_added = 0
                for mineral_comparision in minerals:
                    if min(map(partial(self.distance, 'mineral_to_mineral', mineral_comparision), group)) < 5:
                        item_was_added = 1
                        group.append(mineral_comparision)
                minerals = filter(lambda x: x not in group, minerals)
            self.expand_groups.append({'minerals': group, 'gazes': []})

        gazes = deepcopy(self.minimap['gazes'])
        for group in self.expand_groups:
            item_was_added = 1
            while item_was_added:
                item_was_added = 0
                for gaze_base in gazes:
                    if min(map(partial(self.distance, 'mineral_to_gaz', gaze_base), group['minerals'])) < 4:
                        group['gazes'].append(gaze_base)
                        item_was_added = 1
                        break
                    if group['gazes'] and min(map(partial(self.distance, 'gaz_to_gaz', gaze_base), group['gazes'])) < 4:
                        group['gazes'].append(gaze_base)
                        item_was_added = 1
                        break
                gazes = filter(lambda x: x not in group['gazes'], gazes)

    @staticmethod
    def distance(item_type, item_1_gaz, item_2_mineral):
        if item_type == 'mineral_to_mineral':
            # return max from x or y distance, 2 = mineral size
            return max([abs(item_1_gaz[0] - item_2_mineral[0]) - 2, abs(item_1_gaz[1] - item_2_mineral[1]) - 2])
        elif item_type == 'mineral_to_gaz':
            x_distance = (item_1_gaz[0] - item_2_mineral[0] - 2) if (item_1_gaz[0] - item_2_mineral[0]) > 0 else (item_2_mineral[0] - item_1_gaz[0] - 6)
            y_distance = (item_1_gaz[1] - item_2_mineral[1] - 6) if (item_1_gaz[1] - item_2_mineral[1]) > 0 else (item_2_mineral[1] - item_1_gaz[1] - 2)
            return max([x_distance, y_distance])
        elif item_type == 'gaz_to_gaz':
            return max([abs(item_1_gaz[0] - item_2_mineral[0]) - 6, abs(item_1_gaz[1] - item_2_mineral[1]) - 6])
        else:
            raise Exception('Unknown resourses type')

    def get_nearest_exp_position(self, x, y):
        # just return coordinates by main build position
        pass

    def calculate_main_build_position(self):
        pass
