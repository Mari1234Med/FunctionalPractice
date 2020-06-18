def swap(dictionary):
    """a function that takes a dictionary as input and returns
    a dictionary in which keys with values are swapped
    """
    try:
        if len(dictionary.values()) > len(set(dictionary.values())):
            print('Поменять местами ключи и значения нельзя,'
                  'т.к. произойдет потеря данных')
            return {}
        return {v: k for k, v in dictionary.items()}
    except TypeError:
        print('Невозможно поменять местами ключи и значения')
        return {}


if __name__ == '__main__':
    dict_a = {1: 'a', 2: 'b', 3: 'c', 4: [1, 2, 3, 4]}
    print(dict_a)
    print(swap(dict_a))
    dict_b = {1: 'a', 2: 'b', 3: 'c', 4: 'a'}
    print(dict_b)
    print(swap(dict_b))
    dict_c = {1: 'a', 2: 'b', 3: 'c', 4: 'd'}
    print(dict_c)
    print(swap(dict_c))
