from random import randint

from data import NOC, ACTION_PAIRS, LOCATIONS
from data import Person, Row, find_by_attribute


def pick_random_char():
    people_count = len(NOC)

    # choose random charcter
    person_number = randint(0, people_count-1)
    actor = Person(NOC[person_number])
    return actor


def find_conflict_locations():
    """ Find locations with at least one interaction that is
    in action pairs list and has the link: "but"

    Returns
        list of form: (location-row, action-name)
    """
    buts = find_by_attribute(ACTION_PAIRS, "Link", "but")
    but_actions = [x["Before"] for x in buts]  # get just the names

    print "num. of but-actions: ", len(but_actions)
    print "Like e.g. ", but_actions[:5]
    print

    conflict_locations = []  # contains tuples of (location, avail. but-action)
    for loc in LOCATIONS:
        # action-pairs use underscore in their actions, locations use spaces
        actions = [act.replace(" ", "_") for act in loc["Interactions"]]

        # find interactions that are but-actions
        for action in actions:
            if action in but_actions:
                conflict_locations.append((loc, action))

    print "number of conflict locations:", len(conflict_locations)

    # each element is tuple of (location,action), so to see location
    # get first element of list, and first entry in this tuple
    loc_name = conflict_locations[0][0]["Location"]
    print "first suitable location: ", loc_name, ", action: ", conflict_locations[0][1]

    return conflict_locations

char = pick_random_char()
print "A random char:"
print "Name: {}, weapon: {}".format(char.character, char.weapon_of_choice)
print

conflicts = find_by_attribute(ACTION_PAIRS, "Link", "but")
some_conflict = Row(conflicts[0])
print "First conflict:"
print "before action: ", some_conflict.before, "after: ", some_conflict.after
print

print "Try to find some nice conflict locations..."
find_conflict_locations()
