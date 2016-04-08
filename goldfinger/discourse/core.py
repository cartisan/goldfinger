from data import csv_search, find_by_attribute, ACTION_PAIRS
from discourse.embellish import embellish
from helpers import dice, die


NUTSNESS = 6


def sanitise(text):
    # text = text.replace('\"', '') # this also replaces dialogue quotes!
    return text


def edit(text):
    '''Perform changes on the text'''
    if die(10-NUTSNESS) != 0:
        text = embellish(text)
    return sanitise(str(text))


# --------------------------------- story components ------------------------#

# do we want a "cleaning" function that cleans up the text before it sends it
# back as a tuple?

def generate_partial_story(actionPair, isLast=False):
    '''
    Compose key sentences from the fabula framework action pairs.

    Input: triple of action pairs (String, int, String)
    Output: tuple of actions/tension (String, int)
    '''
    verb, tension, verb2 = actionPair
    idiom = dice(csv_search("cc_pattern/Veale's idiomatic actions.txt", "Idiomatic Forms", verb))
    if not isLast:
        return (edit(idiom), tension)
    else:
        # compose conjunction for last action pair
        conj = conjunction(actionPair)
        idiom2 = dice(csv_search("cc_pattern/Veale's idiomatic actions.txt", "Idiomatic Forms", verb2))
        if conj == "and":
            sentence = '{0} {1} {2}'.format(idiom, conj, idiom2)
            return (edit(sentence), tension)
        else:
            sentence = '{0}, {1} {2}'.format(idiom, conj, idiom2)
            return (edit(sentence), tension)


def introduction(actionPair):
    verb, tension, verb2 = actionPair
    intro = dice(csv_search("cc_pattern/Veale's initial bookend actions.txt", "Establishing Action", verb))
    intro = intro[0].upper() + intro[1:]
    return (edit(intro) + ". ", tension)


def ending(actionPair):
    verb, tension, verb2 = actionPair
    ending = dice(csv_search("cc_pattern/Veale's closing bookend actions.txt", "Closing Action", verb))
    ending = ending[0].upper() + ending[1:] if ending else ending
    return (edit(ending) + ". ", tension)


# ------------------------------ discourse components ------------------------#

# we would possibly want a Sentence class that can care for e.g. full stops for
# every sentence etc.
# But what then with partial sentences?

def superlative(adjective):
    with open('cc_pattern/superlatives.txt', 'rt') as f:
        data = f.read()
    datalines = data.split("\n")
    for line in datalines:
        row = line.split("\t")
        if row[0] == adjective:
            return row[1]


def conjunction(actionPair):
    '''Find the conjunction of the action pair'''
    verb1, tension, verb2 = actionPair
    pair = find_by_attribute(ACTION_PAIRS, "Action Pair", verb1 + ':' + verb2)
    return pair[0]['Link']
