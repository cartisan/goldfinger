from cc_pattern.drivel import drivel
from pattern.en import parse


def embellish(sentence):
    s = parse(sentence).split()[0]
    for i in s:
        if 'NN' in i:
            word = i[0]
            return sentence.replace(word, drivel(word)[2:])

print embellish("He that becomes a god.")
