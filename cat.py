""" The cat utility
"""
import sys


def cat(*args):
    """
    reads files sequentially and writes them to standard output
    :param args:
    :return:
    """
    for name_file in args:
        try:
            with open(name_file, 'r') as file:
                print(file.read())
        except FileNotFoundError:
            print("No such file or directory:", name_file)


if __name__ == '__main__':
    cat(*sys.argv[1:])
