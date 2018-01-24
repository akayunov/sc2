import sys
def print_debug(pixels_):
    for ii in range(len(pixels_[0])):
        for kk in range(len(pixels_)):
            sys.stdout.write(str(pixels_[kk][ii]))
        sys.stdout.write('\n')

