"""zip function implementation"""


def my_zip(*args):
    """
    function takes iterables (can be zero or more), aggregates them in a tuple,
     and return it
    :param args:
    :return:  ierator of typle
    """
    if args == ():
        return
    list_iter = sorted(args, key=len)
    for i in range(len(list_iter[0])):
        zip_list = []
        for cur_list in args:
            zip_list.append(cur_list[i])
        yield tuple(zip_list)


if __name__ == '__main__':
    list_a = [1, 2, 3, 4, 5]
    list_b = ['a', 'b', 'c']
    print(list(my_zip(list_a, list_b)))
    print(list(list(my_zip())))
    print(list(list(my_zip(list_a))))
    zipped = my_zip()
    print(zipped)
