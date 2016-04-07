from pprint import pprint
from random import randint
import sys

from data import ACTION_PAIRS, MIDPOINTS
from data import find_by_attribute


NUM_OF_CLIMAXES = len(find_by_attribute(ACTION_PAIRS, "Tension", "5.0"))

# datatypes:
# action -> triple: (Before, tension, After)
# story_part -> triple (Before Midpoint, Midpoint, After midpoint)
# story_graph -> [action, action, ...]


def pick_climax():
    """ Returns a climax action: (Before, 5, After) and its rating"""

    climaxes = find_by_attribute(ACTION_PAIRS, "Tension", "5.0")
    random_num = randint(0, len(climaxes)-1)
    climax = climaxes[random_num]
    action = (climax["Before"], climax["Tension"], climax["After"])
    return action, 5


def find_previous_steps(action):
    """ Returns a list of midpoint rows that each represents
    possible previous steps:

        [  {'After Midpoint': ['beg_forgiveness_from'], <-- possible step 1
            'Before Midpoint': ['spy_on'],
            'Midpoint': ['are_discovered_by']},

           {...}                                         <-- possible step 2
        ]
    """

    after_midpoint = action[0]
    try:
        steps = find_by_attribute(MIDPOINTS, "After Midpoint", after_midpoint)
    except KeyError:
        raise KeyError("Midpoints have no 'After Midpoint' for: {}"
                       .format(after_midpoint))
    return steps


def choose_step(steps, current_rating, prev=True):
    # turn midpoint row into 2 actions:
    # (BeforeM, M, AfterM) --> (BeforeM, rating, M), (M, rating, AfterM)
    all_midpoint_steps = []
    for step in steps:
        # TODO: if midpoint has more than one element, try with others
        try:
            ap_str = "{}:{}".format(step["Before Midpoint"][0], step["Midpoint"][0])
            ap_row = find_by_attribute(ACTION_PAIRS, "Action Pair", ap_str)[0]
            action_pair = (ap_row["Before"], ap_row["Tension"], ap_row["After"])

            ap2_str = "{}:{}".format(step["Midpoint"][0],step["After Midpoint"][0])
            ap2_row = find_by_attribute(ACTION_PAIRS, "Action Pair", ap2_str)[0]
            action_pair2 = (ap2_row["Before"], ap2_row["Tension"], ap2_row["After"])
            all_midpoint_steps.append((action_pair, action_pair2))
        except:
            # the action-pair table doesn't contain an entry for such a midpoint
            continue

    print "All Midpoint rows ending on Befor-action of conflict:"
    pprint(all_midpoint_steps)
    print

    # filter out all action-pair tuples that were not tension scored:
    filtered_midpoint_steps = []
    for (ap1, ap2) in all_midpoint_steps:
        if ap1[1] and ap2[1]:
            filtered_midpoint_steps.append((ap1, ap2))

    print "All Midpoint rows that have tension ratings for both pairs:"
    pprint(filtered_midpoint_steps)
    print

    if len(filtered_midpoint_steps) == 0:
        raise Exception("Not enough rated action-pairs")

    # select action-pair tuple fitting to our curve
    fitting_midpoint_steps = []
    for (ap1, ap2) in filtered_midpoint_steps:
        if prev:
            if float(ap2[1]) <= current_rating and float(ap1[1]) <= float(ap2[1]):
                fitting_midpoint_steps.append((ap1, ap2))
        else:
            if float(ap1[1]) <= current_rating and float(ap2[1]) <= float(ap1[1]):
                fitting_midpoint_steps.append((ap1, ap2))

    print "All Midpoint rows that fit tension curve:"
    pprint(fitting_midpoint_steps)
    print

    if len(fitting_midpoint_steps) == 0:
        raise Exception("No midpoints that fit tension curve")

    random_midpoint = randint(0, len(fitting_midpoint_steps)-1)

    print fitting_midpoint_steps[random_midpoint]
    print

    return fitting_midpoint_steps[random_midpoint]


def generate_previous_step(action, current_rating):
    try:
        steps = find_previous_steps(action)
    except KeyError as e:
        # no midpoint data for this climax
        print e
        return []

    # try to find a previous step, if not enugh data
    # return empty list
    try:
        prev_step = choose_step(steps, current_rating)
    except:
        return []

    prev_step = list(prev_step)
    print "Previous step:"
    print prev_step
    return prev_step


# ================ next steps generation ===============
# TODO: refactor to use same code as previous with parameter

def find_next_steps(action):
    """ Returns a list of midpoint rows that each represents
    possible next steps:

        [  {'After Midpoint': ['beg_forgiveness_from'], <-- possible step 1
            'Before Midpoint': ['spy_on'],
            'Midpoint': ['are_discovered_by']},

           {...}                                         <-- possible step 2
        ]
    """

    before_midpoint = action[2]
    try:
        steps = find_by_attribute(MIDPOINTS, "Before Midpoint", before_midpoint)
    except KeyError:
        raise KeyError("Midpoints have no 'Before Midpoint' for: {}"
                       .format(before_midpoint))
    return steps


def generate_next_step(action, current_rating):
    try:
        steps = find_next_steps(action)
    except KeyError as e:
        # no midpoint data for this climax
        print e
        return []

    # try to find a previous step, if not enugh data
    # return empty list
    try:
        prev_step = choose_step(steps, current_rating, prev=False)
    except:
        return []

    prev_step = list(prev_step)
    print "Previous step:"
    print prev_step
    return prev_step


def generate_story():
    prev_step, next_step = [], []
    count = 0
    tried_climaxes = []
    while not prev_step or not next_step:
        # pick untried climax
        if count >= NUM_OF_CLIMAXES - 1:
            print "Searched for to long! Tried climaxes:"
            pprint(sorted(tried_climaxes))
            print
            sys.exit()

        action, current_rating = pick_climax()
        unique_id = action[0] + ":" + action[2]

        if unique_id in tried_climaxes:
            # had that one already
            continue

        tried_climaxes.append(unique_id)
        count += 1
        print "===================================="
        print "Trying climax number:", count
        print action
        print

        prev_step = generate_previous_step(action, current_rating)
        next_step = generate_next_step(action, current_rating)

    story = prev_step + [action] + next_step
    print "\nFinal Story:"
    print story
    return story

story = generate_story()
