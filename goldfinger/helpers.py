from random import randint, choice


def rand(lst):
    '''Get random element from a list'''
    return lst[randint(0, len(lst)-1)]


def die(i):
    '''Returns random int'''
    return randint(0, i)


def dice(commastring):
    '''Randomly get an element from comma-separated list'''
    commalist = commastring.split(", ")
    return rand(commalist)


def choice_from_rest(lst, used_lst):
    ''' Randomly chooses an element from lst that was
    not yet previously choosen.
    Returns choosen element and updated list of chosen
    elements
    '''

    rest_lst = list(set(lst) - set(used_lst))
    elem = choice(rest_lst)
    used_lst.append(elem)
    return elem, used_lst
