"""zip function implementation"""


def my_zip(*args):
    if args == ():
        return
    list_iter = sorted(args, key=len)
    for i in range(len(list_iter[0])):
        zip_list = []
        for j in range(len(args)):
            zip_list.append(args[j][i])
        yield tuple(zip_list)


if __name__ == '__main__':
    list_a = [1, 2, 3, 4, 5]
    list_b = ['a', 'b', 'c']
    print(list(my_zip(list_a, list_b)))
    print(list(list(my_zip())))
    print(list(list(my_zip(list_a))))
    zipped = my_zip()
    print(zipped)
