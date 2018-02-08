from PIL import Image
import sys

try:
    from PIL import ImageGrab
except ImportError:
    class ImageGrab:
        @staticmethod
        def grab():
            return Image.new('RGB', (100, 100), (255, 255, 255))


def print_debug(pixels_):
    for ii in range(len(pixels_[0])):
        for kk in range(len(pixels_)):
            sys.stdout.write(str(pixels_[kk][ii]))
        sys.stdout.write('\n')


def get_screenshot():
    return ImageGrab.grab()


def convert_by_diag(high, a):
    r = []
    for i in range(len(a[0])):
        r.append([int(a[k][i]) for k in range(high)])
    return r


def check_and_convert_templates(cls):
    for template in cls.TEMPLATES:
        if len(cls.TEMPLATES[template]['tmpl']) != cls.HIGH:
            raise Exception('High template is wrong: ' + str(template) + ' ' + str(len(cls.TEMPLATES[template]['tmpl'])))
        if len(cls.TEMPLATES[template]['tmpl']) * len(cls.TEMPLATES[template]['tmpl'][0]) != cls.TEMPLATES[template]['square']:
            raise Exception('Square template is wrong: ' + str(template) + ' ' + str(len(cls.TEMPLATES[template]['tmpl']) * len(cls.TEMPLATES[template]['tmpl'][0])))
        cls.TEMPLATES[template]['tmpl'] = convert_by_diag(cls.HIGH, cls.TEMPLATES[template]['tmpl'])
