class GroupHealth:
    NAME = 'group health'
    SUB_GROUP_PIXELS = 11
    LEFT = 650  # 11 pixels for subgroup counting
    RIGHT = 1122
    UP = 887
    BOTTOM = 1059
    UNIT_X_SIZE = int((RIGHT - LEFT - SUB_GROUP_PIXELS) / 8)
    UNIT_Y_SIZE = int((BOTTOM - UP) / 3)
    UNIT_COLOR = {
        0: 'green',
        1: 'yellow',
        2: 'orange',
        3: 'red'
    }
    SUBGROUP_BUTTON_HIGH = 30

    def __init__(self):
        self.units = {
            'red': [],
            'orange': [],
            'yellow': [],
            'green': [],
        }

    def name(self):
        return self.NAME

    def image_is_needed(self):
        return True

    def get_subgroup_count(self, image):
        im = image
        region = im.crop((self.LEFT, self.UP, self.RIGHT, self.BOTTOM))
        # got from up to bottom and find last nont black pixel
        # then devide this coordinate on hight of subgroup key
        max_y_coordinate = 0
        for i in range(self.BOTTOM - self.UP):
            r, g, b = region.getpixel((1, i))
            if r >= 20 and g >= 20 and b >= 20:
                max_y_coordinate = i
        subgroup_count = int(max_y_coordinate / self.SUBGROUP_BUTTON_HIGH) + 1
        return {i: (1 + self.LEFT, self.UP + self.SUBGROUP_BUTTON_HIGH/2 + i * self.SUBGROUP_BUTTON_HIGH) for i in range(subgroup_count)}

    def parse_regions(self, image):
        im = image
        region = im.crop((self.LEFT, self.UP, self.RIGHT, self.BOTTOM))
        # region.show('xxx', 'eog')
        # region.save('sb.png')
        self.units = {
            'red': [],
            'orange': [],
            'yellow': [],
            'green': [],
        }
        for line_number in range(3):
            for unit_number in range(8):
                start_x = self.UNIT_X_SIZE * unit_number + self.SUB_GROUP_PIXELS
                start_y = self.UNIT_Y_SIZE * line_number
                # go by diag and find out color most near to red
                # r = 0 - green
                # g = 0 - red
                # r>200 and g > 200 - yellow
                # r>200 and g > 100 - orange
                unit_color = None
                for i in range(min([self.UNIT_X_SIZE, self.UNIT_Y_SIZE])):
                    r, g, b = region.getpixel((start_x + i, start_y + i))
                    if r == 0 and g >= 200 and b == 0 and unit_color in (None,):  # green
                        unit_color = 'green'
                    elif r >= 200 and g >= 200 and b == 0 and unit_color in ('green', None):  # yellow
                        unit_color = 'yellow'
                    elif r >= 200 and g >= 100 and b == 0 and unit_color in ('green', 'yellow', None):  # orange
                        unit_color = 'orange'
                    elif g == 0 and r >= 200 and b == 0:  # red
                        unit_color = 'red'
                        break
                if unit_color:
                    self.units[unit_color].append((start_x + self.UNIT_X_SIZE/2 + self.LEFT, start_y + self.UNIT_Y_SIZE/2 + self.UP))

    def alarm(self):
        pass
