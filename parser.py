"""Parsing Log Files"""
import re
import collections

FILE_NAME = 'access_log.log'


def find_most_requests(data):
    """
    Returns list of 10 clients of this server requesting the largest
     number of pages
    :param data:
    :return: list
    """
    reg = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    list_ip = re.findall(reg, data)
    counter_ip = collections.Counter(list_ip)
    return counter_ip.most_common(10)


def find_popular_platforms(data):
    """
    Returns 5 most popular platforms (OS) for launching web browsers
    :param data:
    :return: list
    """
    reg = r'((Linux|Windows|Macintosh|Unix|iPhone OS).*?)(?=\))'
    list_group = re.findall(reg, data)
    list_os = [item[0] for item in list_group]
    counter_ip = collections.Counter(list_os)
    return counter_ip.most_common(5)


def main():
    """
    Opens logfile, runs and print find_most_requests() and
    find_popular_platforms()
     :return:

    """
    try:
        with open(FILE_NAME, 'r') as f:
            data = f.read()
            print(find_most_requests(data))
            print(find_popular_platforms(data))
    except FileNotFoundError:
        print("No such file or directory:", FILE_NAME)


if __name__ == '__main__':
    main()
