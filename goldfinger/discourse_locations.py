'''
Defines methods to add location discourse to existing text.

Usage:
>> NUTSNESS = 10
>> add_location_discourse(
    "He was killed",
    "abandoned building",
    add_props=True,
    add_extra=True
    )
"He was killed in a changing room. It is a claustrophobica rose-mauve
roomette in which things are stored."

'''
from random import randint

from cc_pattern.drivel import drivel
from cc_pattern.noc import index
from pattern.en import pluralize, sentiment, referenced
import math

from data import find_by_attribute, LOCATIONS

NUTSNESS = 10


# -------------------------------- getters -----------------------------------#

def rand(lst):
    '''Get random element from a list'''
    return lst[randint(0, len(lst)-1)]


def get_location_by_name(name):
    '''
    Get location dict by name

    Input: String name
    Output: dict location
    '''
    location = find_by_attribute(LOCATIONS, "Location", name)
    return location[0]


def get_location_by_tension(tension):
    '''
    Get location dict by exact tension level

    Input: integer tension
    Output: list location(s)
    '''
    print index(LOCATIONS, "Tension", unique=False)
    locations_on_tension = find_by_attribute(LOCATIONS, "Tension", tension)
    return rand(locations_on_tension)


def get_location_at_random():
    location = rand(find_by_attribute(LOCATIONS, "Preposition", "in"))
    return location


# ---------------------------- tension estimation ----------------------------#

def estimate_location_tension():
    '''
    Compute the most tense locations with sentiment analysis.
    Shouldn't be used more than once!

    Output: file with sorted locations based on sentiments
    '''
    locations = LOCATIONS
    f = open('location_tensions2.txt', 'w')
    tensions = []
    for location in locations:
        ambience = location['Ambience']
        s = [0, 0]
        for amb in ambience:
            n, p = sentiment(amb)
            s[0] += n
            s[1] += p
        s[0] /= len(ambience)
        s[1] /= len(ambience)
        total_tension = s[0]+s[1]
        tensions.append(total_tension)
        # tensions.append(str(s[0]+s[1]) + "; " + str(s[0]) + ', ' + str(s[1]) + ' ' + repr(location['Location']) + '\n')
    maxt = max(tensions)
    mint = min(tensions)
    for t in tensions:
        normalized = math.ceil(5*(t-mint)/(maxt-mint))
        f.write(str(5-normalized) + '\n')


# ------------------------------- discourse ----------------------------------#

def add_sentence(noun, adjective, nutsness=10):
    '''
    Create a new sentence. Nutsness will define the chance on generating
    strange additions with pattern's drivel(). This is awesome.

    Input: String noun, String adjective, integer nutsness
    Output: String sentence
    '''
    nuts = 10-nutsness
    n = noun.split()

    if randint(0, nuts) == 0:
        # return a ridiculous sentence
        sentence = ' It is {}.'.format(
                                    referenced(
                                        adjective + drivel(n[-1])
                                        )
                                    )
    else:
        # return a boring sentence
        sentence = ' This is a {} place.'.format(referenced(adjective))

    return sentence


def add_location_props(loc):
    '''
    Returns partial sentence of location props.

    Input: dict or String location
    Output: String " amongst the X" with X a random prop
    '''
    if type(loc) == str:
        loc = get_location_by_name(loc)
    props = loc['Props']
    if props == ['']:
        return '.'
    else:
        prop = rand(props)
        return ' amongst the {}.'.format(pluralize(prop))


def add_location_description(loc):
    '''
    Adds a short sentence after location identifier which describes
    the location.
    Let's hope this gives a more realistic feel to the text!

    Input: dict or String location
    Output: String sentence
    '''
    if type(loc) == str:
        loc = get_location_by_name(loc)
    ambience = loc['Ambience']
    amb = rand(ambience)
    tension = [float(t) for t in loc['Sentiment']]
    # attempt to get an appropriate ambience for the location
    while True:
        amb = rand(ambience)
        if (abs(sum(tension)-sum(sentiment(amb))) < 1):
            return add_sentence(loc['Location'], amb, nutsness=NUTSNESS)


def add_location_discourse(text, location, add_props=False, add_descr=False):
    '''
    Appends a location with preposition and determiner to an input text

    Input: String text, String location identifier
    Output: String text added with location discourse
    '''
    if type(location) == str:
        location = get_location_by_name(location)
    # get parts of the text
    name = location['Location']
    preposition = location['Preposition']
    determiner = location['Determiner']
    props = add_location_props(location) if add_props else '.'
    extra_simple_sentence = add_location_description(location) if add_descr else ''
    # return compiled text
    return "{0} {1} {2} {3}{4}{5}".format(
                                text,
                                preposition,
                                determiner,
                                name,
                                props,
                                extra_simple_sentence
                                )


# ------------------------------- generation ---------------------------------#

def generate_location_story(storyPart):
    '''
    Search for a location and add it to a sentence of a story.

    Input: tuple (storySentence, tensionLevel)
    Output: tuple (storySentence+location, tensionLevel, bool has_descr)
    '''
    sentence, tension = storyPart
    # location = get_location_by_tension(tension)
    location = get_location_at_random()
    props = True
    descr = bool(randint(0, NUTSNESS) != 0)
    story_with_location = add_location_discourse(
        sentence,
        location,
        add_props=props,
        add_descr=descr
        )
    return (story_with_location, tension, descr)


if __name__ == "__main__":
    # for testing
    print add_location_discourse(
        "He was killed",
        "changing room",
        add_props=True,
        add_descr=True
        )

    print generate_location_story(("The little pony was enflowered", "5.0"))
