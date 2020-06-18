"""short functions that take one argument - a list of numbers"""


def squared(numberlist):
    """Returns - list of squared numbers"""
    return [x ** 2 for x in numberlist]


def second_elem(numlist):
    """Returns - every second list item"""
    return (numlist[i] for i in range(len(numlist)) if i % 2 == 0)


def even_in_odd(numlist):
    """Squares of even elements in odd positions"""
    return (numlist[i] ** 2 for i in range(len(numlist))
            if numlist[i] % 2 == 0 and i % 2 != 0)


if __name__ == '__main__':
    list_a = [1, 3, 5, 7, 9, 11, 13, 15]
    list_b = list(range(1, 20))
    print(squared(list_a))
    print(list(second_elem(list_a)))
    print(list(even_in_odd(list_a)))
    print(squared(list_b))
    print(list(second_elem(list_b)))
    print(list(even_in_odd(list_b)))
