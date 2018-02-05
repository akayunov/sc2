import math
from copy import deepcopy
from functools import partial


class MapInfo(object):
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
                    for yi in range(y, y + size + 1 ):
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
                        self.minimap['gazes'].append((j, k))
                    elif self.check_blue_region(j, k, 2):
                        # mineral is found, save "up - left" corner as it coordinates
                        self.minimap['minerals'].append((j, k))

        self.group_resources_by_expand()

    def get_item_coordinate_on_whole_screen(self, el):
        return el[0] + self.LEFT, el[1] + self.UP

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

        i = 0
        gazes = deepcopy(self.minimap['gazes'])
        for group in self.expand_groups:
            item_was_added = 1
            while item_was_added and i < 10000:
                i += 1
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
            # TODO (item_1_gaz[0] - item_2_mineral[0]) > 0  is equal to item_1_gaz[0] > item_2_mineral[0]
            x_distance = (item_1_gaz[0] - item_2_mineral[0] - 2) if (item_1_gaz[0] - item_2_mineral[0]) > 0 else (item_2_mineral[0] - item_1_gaz[0] - 6)
            y_distance = (item_1_gaz[1] - item_2_mineral[1] - 2) if (item_1_gaz[1] - item_2_mineral[1]) > 0 else (item_2_mineral[1] - item_1_gaz[1] - 6)
            return max([x_distance, y_distance])
        elif item_type == 'gaz_to_gaz':
            return max([abs(item_1_gaz[0] - item_2_mineral[0]) - 6, abs(item_1_gaz[1] - item_2_mineral[1]) - 6])
        else:
            raise Exception('Unknown resourses type')

    def get_nearest_exp_resourses_group(self, x, y):
        x = x - self.LEFT
        y = y - self.UP
        result = (1000000000, self.expand_groups[0])
        for group in self.expand_groups:
            for el in group['gazes'] + group['minerals']:
                distance = math.sqrt((x - el[0]) ** 2 + (y - el[1]) ** 2)
                if result[0] > distance:
                    result = (distance, group)
        return result[1]

    def calculate_main_building_position(self, group):
        gr = group['minerals'] + group['gazes']
        max_x = max(max(el[0] + 2 for el in group['minerals']), max(el[0] + 6 for el in group['gazes']))
        min_x = min((el[0] for el in gr))
        max_y = max(max(el[1] + 2 for el in group['minerals']), max(el[1] + 6 for el in group['gazes']))
        min_y = min((el[1] for el in gr))
        # print('MAX', max_x, max_y, min_x, min_y)
        mineral_field = []
        for i in range(max_x - min_x):
            mineral_field.append([0] * (max_y - min_y))
        # 7  = 6 + 1, 6 - distance between mineral and cc, 1 - line where will be boarder of cc
        for el in group['minerals']:
            normalize_coordinates = (el[0] - min_x, el[1] - min_y)
            for i in range(normalize_coordinates[0] - 7, normalize_coordinates[0] + 7 + 2):  # 2 - size mineral field
                for k in range(normalize_coordinates[1] - 7, normalize_coordinates[1] + 7 + 2):  # 2 - size mineral field
                    # print('COOR', i, k)
                    if 0 < i < max_x - min_x and 0 < k < max_y - min_y:
                        mineral_field[i][k] = 1
        for el in group['gazes']:
            normalize_coordinates = (el[0] - min_x, el[1] - min_y)
            for i in range(normalize_coordinates[0] - 7, normalize_coordinates[0] + 7 + 6):  # 6 - size mineral field
                for k in range(normalize_coordinates[1] - 7, normalize_coordinates[1] + 7 + 6):  # 6 - size mineral field
                    if 0 < i < max_x - min_x and 0 < k < max_y - min_y:
                        mineral_field[i][k] = 1

        for el in group['minerals']:
            normalize_coordinates = (el[0] - min_x, el[1] - min_y)
            for i in range(normalize_coordinates[0] - 6, normalize_coordinates[0] + 6 + 2):  # 2 - size mineral field
                for k in range(normalize_coordinates[1] - 6, normalize_coordinates[1] + 6 + 2):  # 2 - size mineral field
                    if 0 < i < max_x - min_x and 0 < k < max_y - min_y:
                        mineral_field[i][k] = 2
        for el in group['gazes']:
            normalize_coordinates = (el[0] - min_x, el[1] - min_y)
            for i in range(normalize_coordinates[0] - 6, normalize_coordinates[0] + 6 + 6):  # 6 - size gaz field
                for k in range(normalize_coordinates[1] - 6, normalize_coordinates[1] + 6 + 6):  # 6 - size gaz field
                    if 0 < i < max_x - min_x and 0 < k < max_y - min_y:
                        mineral_field[i][k] = 2

        # # for debug
        for el in group['minerals']:
            normalize_coordinates = (el[0] - min_x, el[1] - min_y)
            for i in range(normalize_coordinates[0], normalize_coordinates[0] + 2):  # 2 - size mineral field
                for k in range(normalize_coordinates[1], normalize_coordinates[1] + 2):  # 2 - size mineral field
                    if 0 < i < max_x - min_x and 0 < k < max_y - min_y:
                        mineral_field[i][k] = ' '
        for el in group['gazes']:
            normalize_coordinates = (el[0] - min_x, el[1] - min_y)
            for i in range(normalize_coordinates[0], normalize_coordinates[0] + 6):  # 6 - size gaz field
                for k in range(normalize_coordinates[1], normalize_coordinates[1] + 6):  # 6 - size gaz field
                    if 0 < i < max_x - min_x and 0 < k < max_y - min_y:
                        mineral_field[i][k] = ' '
        # from sc2.utils import print_debug
        # print_debug(mineral_field)
        # now all element with value == 1 is allowed for building
        # and we search point what is nearest to center
        center_coordinates = ((max_x - min_x) / 2, (max_y - min_y) / 2)
        # print('CENTER',center_coordinates)
        result = (1000000, (0, 0))
        for i in range(len(mineral_field)):
            for k in range(len(mineral_field[i])):
                if mineral_field[i][k] == 1:
                    distance = math.sqrt((i - center_coordinates[0]) ** 2 + (k - center_coordinates[1]) ** 2)
                    # print('DISTANEC', distance, i, k)
                    if distance  <= result[0]:
                        result = (distance, (i, k))
        # print('RESULT',result)
        return result[1][0] + min_x + self.LEFT, result[1][0] + min_y + self.UP
