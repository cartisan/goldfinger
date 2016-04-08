import re

from data import NOC
from discourse.core import rand


def make_characters(n):
    '''Get n characters'''
    chars = []
    for i in range(n):
        chars.append(rand(NOC)['Character'])
    return chars


def replacefunction(text, firstchar, secondchar):
    '''Replace A and B in text by character names'''
    regex1 = re.compile(r'(\b)A(\b)')
    regex2 = re.compile(r'(\b)B(\b)')
    text = re.sub(regex1, firstchar, text)
    text = re.sub(regex2, secondchar, text)
    return text
