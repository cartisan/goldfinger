from random import randint


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
