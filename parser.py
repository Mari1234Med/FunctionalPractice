"""Parsing Log Files"""
import re
import collections


def read_find(file_name, find_func):
    """
    Opens logfile and runs find_func for read data
    :param file_name: name of logfile
           find_func: regular expression search function
    :return:  list

    """
    try:
        with open(file_name, 'r') as f:
            data = f.read()
            return find_func(data)

    except FileNotFoundError:
        print("No such file or directory:", file_name)
        return []


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
    pass


if __name__ == '__main__':
    print(read_find('access_log.log', find_most_requests))
