"""xrange function implementation"""


def xrange(*args):
    start, stop, step = 0, 0, 0
    if len(args) == 1:
        start = 0
        step = 1
        stop = args[0]
    elif len(args) == 2:
        start = args[0]
        stop = args[1]
        step = 1
    elif len(args) == 3:
        start = args[0]
        stop = args[1]
        step = args[2]
    else:
        raise TypeError
    state = start
    if step > 0:
        while state < stop:
            yield state
            state += step
    elif step < 0:
        while state > stop:
            yield state
            state += step
    else:
        return


if __name__ == '__main__':
    print(list(xrange(1, 10, 2)))
    print(list(xrange(1, 5)))
    print(list(xrange(10, -5, -1)))
    print(list(xrange(1, 0)))
    print(list(xrange(1, 2, -3)))
    for i in xrange(1, 10, 2):
        print(i)
