""" The cat utility reads files sequentially and writes them to
 standard output.
"""
import sys


def cat(*args):
    for name_file in args:
        try:
            with open(name_file, 'r') as f:
                print(f.read())
        except FileNotFoundError:
            print("No such file or directory:", name_file)


if __name__ == '__main__':
    cat(*sys.argv[1:])
