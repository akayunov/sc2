import pytest
from sc2.utils import print_debug, check_and_convert_templates


def test_print_debug():
    print_debug([[1, 2], [3, 4]])


def test_convert_templates():
    class Templ1:
        HIGH = 10

        TEMPLATES = {
            0: {'tmpl': [
                '00001110000',
                '01111111110',
                '11000000011',
                '11000000011',
                '11000000011',
                '11000000011',
                '11000000011',
                '11000000011',
                '01111111110',
                '00001110000',
                '00001110000'
            ],
                'square': 110},
        }

    with pytest.raises(Exception, match=r'High template is wrong.*'):
        check_and_convert_templates(Templ1)

    class Templ2:
        HIGH = 10

        TEMPLATES = {
            0: {'tmpl': [
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
            ],
                'square': 0},
        }

    with pytest.raises(Exception, match=r'Square template is wrong.*'):
        check_and_convert_templates(Templ2)
