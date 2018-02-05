import os
import playsound


def mock_play_sound(path):
    os.path.isfile(path)

playsound.playsound = mock_play_sound
