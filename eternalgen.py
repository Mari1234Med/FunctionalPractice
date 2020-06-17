"""Eternal generator returns  - 1"""


def eternal_gen():
    while True:
        yield 1


if __name__ == '__main__':
    gen = eternal_gen()
    print(gen)
    print(next(gen))
