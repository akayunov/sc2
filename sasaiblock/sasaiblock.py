#!/usr/bin/env python
import sys
from copy import deepcopy
from pprint import pprint
from PIL import Image
from operator import getitem

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
    '01001',
    '10001',
    '00001',
    '00001',
    '00001',
    '00001',
    '00001',
    '00001'
]
TWO = [  # TODO
    '11111111111',
    '11111111111',
    '11111111111',
    '11111111111',
    '11111111111',
    '11111111111',
    '11111111111',
    '11111111111',
    '11111111111',
    '11111111111'
]
THREE = [  # TODO
    '11111111111',
    '11111111111',
    '11111111111',
    '11111111111',
    '11111111111',
    '11111111111',
    '11111111111',
    '11111111111',
    '11111111111',
    '11111111111'
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
    '1111111110',
    '1000000000',
    '1000000000',
    '1000000000',
    '1111111110',
    '0000000011',
    '0000000011',
    '1000000011',
    '1100000110',
    '0001110000'
]
SIX = [  # TODO
    '11111111111',
    '11111111111',
    '11111111111',
    '11111111111',
    '11111111111',
    '11111111111',
    '11111111111',
    '11111111111',
    '11111111111',
    '11111111111'
]
SEVEN = [
    '11111111111',
    '11111111111',
    '00000000110',
    '00000000100',
    '00000001000',
    '00000011000',
    '00000110000',
    '00001100000',
    '00011000000',
    '00110000000']
EIGHT = [  # TODO
    '11111111111',
    '11111111111',
    '11111111111',
    '11111111111',
    '11111111111',
    '11111111111',
    '11111111111',
    '11111111111',
    '11111111111',
    '11111111111'
]
NINE = [  # TODO
    '11111111111',
    '11111111111',
    '11111111111',
    '11111111111',
    '11111111111',
    '11111111111',
    '11111111111',
    '11111111111',
    '11111111111',
    '11111111111'
]
SLASH = [
    '00000001',
    '00000001',
    '00000010',
    '00000100',
    '00001000',
    '00010000',
    '00010000',
    '00100000',
    '01000000',
    '10000000'
]

GAP_SIZE_BETWEEN_NUMBER_GROUP = 20

LEFT = 1520  # TODO more space for bigger number for late game ~1300
RIGHT = 1830
UP = 23
BOTTOM = 33
HIGH = BOTTOM - UP

ALL_NUMBERS = [ZERO, ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, SLASH]

# check HIGH of all templ
if filter(lambda x: len(x) != HIGH, ALL_NUMBERS):
    raise Exception()


def convert_by_diag(a):
    r = []
    for i in range(len(a[0])):
        r.append([int(a[k][i]) for k in range(HIGH)])
    return r


NUMBERS_TEMPLATE = dict(
    zip(
        ['ZERO', 'ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX', 'SEVEN', 'EIGHT', 'NINE', 'SLASH'],
        zip(
            map(convert_by_diag, ALL_NUMBERS),
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, '/'],
            [len(tp[0]) * HIGH for tp in ALL_NUMBERS]
        )
    )
)


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
            # white 255 255 255
            if r >= 245 and g >= 245 and b >= 245:
                pixels_[i][k] = 1
            else:
                pixels_[i][k] = 0
    return pixels_


def count_similarity(n_arr, num_templ):
    count = 0
    for i in range(min(len(n_arr), len(num_templ[0]))):
        for k in range(min(len(n_arr[0]), len(num_templ[0][0]))):
            if n_arr[i][k] == num_templ[0][i][k]:
                count += 1 if n_arr[i][k] == 0 else 1.5  # add weight for 1
    # check with shift if sizes is not equal
    n_templ = deepcopy(num_templ[0])
    while len(n_arr) != len(n_templ):
        count_intermediate = 0
        if len(n_arr) < len(n_templ):
            n_arr = [[0] * HIGH] + n_arr
        else:
            n_templ = [[0] * HIGH] + n_templ
        for i in range(min(len(n_arr), len(n_templ))):
            for k in range(min(len(n_arr[0]), len(n_templ[0]))):
                if n_arr[i][k] == n_templ[i][k]:
                    count_intermediate += 1 if n_arr[i][k] == 0 else 1.5  # add weight for 1
        if count_intermediate > count:
            count = count_intermediate

    # devide on maximum pictures to avoid confusing with small templ like 1 with many zeros when zeros hit become bigger then 1 hit
    return float(count) / (HIGH * max([len(n_arr), len(n_templ)])), num_templ[1]


def parse_numbers(n_arr):
    result = [0, 0]
    for num_templ in NUMBERS_TEMPLATE:
        sim, symbol = count_similarity(n_arr, NUMBERS_TEMPLATE[num_templ])
        if sim > result[0]:
            result = [sim, symbol]
    return result[1]


def get_numbers(pixels_):
    numbers = []
    groups = []
    n = []
    gap_size = 0
    for i, col in enumerate(pixels_):
        if not filter(None, pixels_[i]):
            # find empty gap
            gap_size += 1
            if n:
                numbers.append(parse_numbers(n))
            n = []
        else:
            n.append(pixels_[i])
            gap_size = 0
        if gap_size > 10 and numbers:
            groups.append(numbers)
            numbers = []
    groups.append(numbers)
    return groups

if __name__ == '__main__':
    pixels = get_pixels(Image.open('resourses/sc.png'))
    print(get_numbers(pixels))
