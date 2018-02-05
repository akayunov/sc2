import os
from playsound import playsound

from sc2.watcher import Watcher


class ProductionQueue(Watcher):
    NAME = 'production queue'
    LEFT = 370
    RIGHT = 1360
    UP = 880
    BOTTOM = 1060

    check_points = []

    def __init__(self):
        self.production_queues = []

    def name(self):
        return self.NAME

    def image_is_needed(self):
        return True

    def parse_regions(self, image):
        im = image

        region = im.crop((self.LEFT, self.UP, self.RIGHT, self.BOTTOM))
        # region.show('xxx', 'eog')
        # region.save('sb.png')

        # colors
        # 64 64 64 - empty slot
        # 254 254 254 - occupied slot
        # start position (297, 57)
        x_start_position = 295
        y_start_position = 57
        line_high = 57

        some_structure = []
        marker_count = 0
        previous_marker = 0

        for l in range(3):  # 3 line it's rare case then thera will be more then 27 factory
            for p in range(x_start_position, self.RIGHT - self.LEFT):
                r, g, b = region.getpixel((p, y_start_position + line_high * l))
                if r == g == b == 254:
                    current_marker = 254
                elif r == g == b == 64:
                    current_marker = 64
                else:
                    current_marker = 0

                if previous_marker == current_marker:
                    marker_count += 1
                else:
                    some_structure.append((previous_marker, marker_count))
                    marker_count = 1
                previous_marker = current_marker
        some_structure.append((previous_marker, marker_count))
        factory_result = []
        for el in some_structure:
            if el[0] != 0:
                factory_result.append(el[0])
            if el[0] == 0 and el[1] > 2:
                self.production_queues.append(factory_result)
                factory_result = []

    def alarm(self):
        for factory in self.production_queues:
            # TODO say which queue is overloaded exactly
            if len(list(filter(lambda x: x == 254, factory))) > 2 and len(factory) == 5:
                playsound(os.path.join(os.path.dirname(__file__), 'resourses', 'queue_is_overflowing.mp3'))
            if len(list(filter(lambda x: x == 254, factory))) > 4 and len(factory) == 8:
                playsound(os.path.join(os.path.dirname(__file__), 'resourses', 'queue_is_overflowing.mp3'))
