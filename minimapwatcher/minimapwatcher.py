#!/usr/bin/env python
import sys
from copy import deepcopy
from pprint import pprint
from PIL import Image
from operator import getitem

SIZE = 300
LEFT = 0  # TODO more space for bigger number for late game ~1300
RIGHT = SIZE + LEFT
UP = 800
BOTTOM = UP + SIZE


def print_debug(pixels_):
    for ii in range(len(pixels_[0])):
        for kk in range(len(pixels_)):
            sys.stdout.write(str(pixels_[kk][ii]))
        sys.stdout.write('\n')


def get_pixels(image):
    im = image

    region = im.crop((LEFT, UP, RIGHT, BOTTOM))
    # region.show('xxx', 'eog')
    # region.save('sb.png')

    rgb_im = region.convert('RGB')
    # rgb_im.show('xxx', 'eog')

    pixels_ = [None] * (RIGHT - LEFT)
    for i in range(RIGHT - LEFT):
        pixels_[i] = [0] * (BOTTOM - UP)
    for i in range(RIGHT - LEFT):
        for k in range(BOTTOM - UP):
            r, g, b = rgb_im.getpixel((i, k))
            # print((i, k), '-', (r, g, b))
            if r >= 245 and g <= 20 and b <= 20:
                pixels_[i][k] = 1
            else:
                pixels_[i][k] = 0
    return pixels_


def parse_region(red_pixels_):
    result = []
    one_third_part = int(len(red_pixels_)/3)
    two_third_part = int(len(red_pixels_)/3) * 2

    for start_col in [0, one_third_part, two_third_part]:
        for start_el in [0, one_third_part, two_third_part]:
            qudrant_count = 0
            for i in range(start_col, start_col + one_third_part):
                for k in range(start_el, start_el + one_third_part):
                    qudrant_count += red_pixels_[i][k]
            result.append(qudrant_count)
    return result

if __name__ == '__main__':
    init_value = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    red_pixels = get_pixels(Image.open('resourses/sc.png'))
    changed_regions = parse_region(red_pixels)
