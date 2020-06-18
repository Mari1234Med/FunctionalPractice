"""Eternal generator"""


def eternal_gen():
    """
    Eternal generator
    :return:  1
    """
    while True:
        yield 1


if __name__ == '__main__':
    gen = eternal_gen()
    print(gen)
    print(next(gen))
