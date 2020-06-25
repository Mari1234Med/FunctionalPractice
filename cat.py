""" cat -- concatenate files and print on the standard output.
Concatenate FILE(s), or standard input, to standard output.
Usage: %s [OPTION]... [FILE]..
  -A, --show-all           equivalent to -ET
  -b, --number-nonblank    number nonempty output lines
  -E   -e, --show-ends          display $ at end of each line
  -n, --number             number all output lines
  -s, --squeeze-blank      suppress repeated empty output lines
  -T, -t, --show-tabs          display TAB characters as ^I
"""
import sys
import argparse

counter_nonempty = 0


def create_parser():
    """
    creating a parser
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--number-nonblank', action='store_const',
                        const=True, help=' number nonempty output lines')
    parser.add_argument('-A', '--show-all', action='store_const', const=True,
                        help='equivalent to -vET')
    parser.add_argument('-E', '-e', '--show-ends', action='store_const',
                        const=True, help='display $ at end of each line')
    parser.add_argument('-n', '--number', action='store_const', const=True,
                        help='number all output lines')
    parser.add_argument('-T', '-t', '--show-tabs', action='store_const',
                        const=True, help='display TAB characters as ^I')
    parser.add_argument('files', type=str, nargs='+',
                        help='list of files')
    return parser.parse_args()


def new_cat():
    """

    :return:
    """

    args = create_parser()
    for name_file in args.files:
        try:
            with open(name_file, 'r') as file:
                global counter_nonempty
                counter_nonempty = 0
                lines = file.readlines()
                for i, line in enumerate(lines):
                    lines[i] = line_change(i, line, args)
                    print(lines[i])

        except FileNotFoundError:
            print("No such file or directory:", name_file)


def line_change(i, string, args):
    """
    Change the line according to the flags raised
    :param i: string number
    :param string: current string
    :param args: flags
    :return:
    """
    if args.show_all:
        args.show_ends = True
        args.show_tabs = True
    if args.show_ends:
        index = string.find('\n')
        if index >= 0:
            string = string[:index] + '$'
    if args.number:
        string = str(i + 1) + ' ' + string
    if args.number_nonblank:
        if string.strip():
            global counter_nonempty
            counter_nonempty += 1
            string = str(counter_nonempty) + ' ' + string
    if args.show_tabs:
        while string.find('\t') >= 0:
            index = string.find('\t')
            string = string[:index] + '^I' + string[index + 1:]
    return string


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
    print("The first version of the utility cat:")
    cat(*sys.argv[1:])
    print("The second version of the utility cat:")
    new_cat()
