from random import randint

from data import NOC, ACTION_PAIRS
from data import Person, Row, find_by_attribute


def pick_random_char():
    people_count = len(NOC)

    # choose random charcter
    person_number = randint(0, people_count-1)
    actor = Person(NOC[person_number])
    return actor


char = pick_random_char()
print "A random char:"
print "Name: {}, weapon: {}".format(char.character, char.weapon_of_choice)
print

conflicts = find_by_attribute(ACTION_PAIRS, "Link", "but")
some_conflict = Row(conflicts[0])
print "First conflict:"
print "before action: ", some_conflict.before, "after: ", some_conflict.after
