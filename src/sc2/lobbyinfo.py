from sc2.utils import Watcher


class LobbyInfo(Watcher):
    NAME = 'lobby info'
    # TODO improve for diff screen resolution
    LEFT = 20
    RIGHT = 275 + LEFT
    UP = 805
    BOTTOM = UP + 275

    def __init__(self):
        self.minimap = {'gazes': [], 'minerals': []}
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

        rgb_im = region.convert('RGB')

        for j in range(self.RIGHT - self.LEFT):
            for k in range(self.BOTTOM - self.UP):
                r, g, b = rgb_im.getpixel((j, k))
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

        # let's think what x + size - 1 and y + size - 1 is always exists
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
                        # gaz is found
                        self.minimap['gazes'].append((self.LEFT + j + 2, self.UP + k + 2))
                    elif self.check_blue_region(j, k, 2):
                        # mineral is found
                        self.minimap['minerals'].append((j, k))
        self.calculate_main_build_position()

    def get_nearest_exp_position(self, x, y):
        # just return coordinates by main build position
        pass

    def calculate_main_build_position(self):
        pass
