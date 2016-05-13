import collections
from pprint import pprint
import logging
from random import choice

from data import ACTION_PAIRS, MIDPOINTS
from data import find_by_attribute
from helpers import choice_from_rest

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def Tree():
    # t = Tree()
    # t[1] = "value"
    # t[2][2] = "another value"
    # number of nodes at level 0
    # len(t) - 1
    return collections.defaultdict(Tree)

    def get_node(self, key):
        return self[key]


def midpoint_to_actionpairs(mp):
    # transform (BefM, M, AftM) to [((BefM, rating, M)), (M, rating, AftM)]
    try:
        ap_str = "{}:{}".format(mp["Before Midpoint"][0], mp["Midpoint"][0])
        ap_row = find_by_attribute(ACTION_PAIRS, "Action Pair", ap_str)[0]
        action_pair = (ap_row["Before"], ap_row["Tension"], ap_row["After"])

        ap2_str = "{}:{}".format(mp["Midpoint"][0], mp["After Midpoint"][0])
        ap2_row = find_by_attribute(ACTION_PAIRS, "Action Pair", ap2_str)[0]
        action_pair2 = (ap2_row["Before"], ap2_row["Tension"], ap2_row["After"])
    except:
        return None

    # filter action pairs without tension rating
    if not action_pair[1] or not action_pair2[1]:
        if not action_pair[1]:
            logger.warning("No tension for action pair: {}, {}".
                           format(action_pair[0],
                                  action_pair[2]))
        if not action_pair2[1]:
            logger.warning("No tension for action pair: {}, {}".
                           format(action_pair2[0],
                                  action_pair2[2]))

        return None

    return (action_pair, action_pair2)


def find_previous_steps(action, tension):
    """ Returns a list of tuples of actionpairs, that each represents
    possible previous steps:

    action: ('beg_forgiveness_from', '5.0', 'are_indoctrinated_by')
    returns:
    [(('spy_on', '3.0', 'are_discovered_by'),
      ('are_discovered_by', '3.0', 'beg_forgiveness_from')),
     (('disfigure', '3.0', 'are_disgusted_by'),
      ('are_disgusted_by', '2.0', 'beg_forgiveness_from')),
    ]
    """

    logging.debug("Finding previous midpoint for " + str(action))
    after_midpoint = action[0]
    try:
        midpoints = find_by_attribute(MIDPOINTS,
                                      "After Midpoint",
                                      after_midpoint)
    except:
        # no midpoints for this action
        logging.warning("No After Midpoint: " + after_midpoint)
        return []

    # transform (BefM, M, AftM) to [((BefM, rating, M)), (M, rating, AftM)]
    ap_tuples = []
    for mp in midpoints:
        ap_tuple = midpoint_to_actionpairs(mp)
        if ap_tuple:
            ap_tuples.append(ap_tuple)
    return ap_tuples


def create_story_graph_back(tension_curve):
    logger.info(
        "Backwards generating story graph from tension " + tension_curve[2]
    )
    story_graph = Tree()

    climaxes = find_by_attribute(ACTION_PAIRS, "Tension", tension_curve[2])
    logger.debug(str(len(climaxes)) + " climaxes found")

    for climax in climaxes:
        action_pair = (climax["Before"], climax["Tension"], climax["After"])
        story_graph[tension_curve[2]][action_pair]

    # TODO: remove restriction of used climax
    # for action_pair in story_graph[tension_curve[2]].keys()[3:4]:
    for action_pair in story_graph[tension_curve[2]].keys()[2:3]:
        previous_steps = find_previous_steps(action_pair, tension_curve[1])
        for (BefMM, MAftM) in previous_steps:
            #                  current state           rating   prev ap
            story_graph[tension_curve[2]][action_pair][MAftM[1]][MAftM]
            #                                    prev action            rating   first ap
            story_graph[tension_curve[2]][action_pair][MAftM[1]][MAftM][BefMM[1]][BefMM]

    return story_graph


# def create_story_graph_front(tension_curve):
#     story_graph = Tree()

#     climaxes = find_by_attribute(ACTION_PAIRS, "Tension", tension_curve[2])
#     for climax in climaxes:
#         action_pair = (climax["Before"], climax["Tension"], climax["After"])
#         story_graph[tension_curve[2]][action_pair]

#     for action_pair in story_graph[tension_curve[2]].keys()[2:3]:
#         print
#         print "conflict:", action_pair
#         previous_steps = find_previous_steps(action_pair, "4.0")
#         pprint(previous_steps)
#         for (BefMM, MAftM) in previous_steps:
#             #        current state           rating   prev ap
#             story_graph["5.0"][action_pair][MAftM[1]][MAftM]
#             #                         prev action            rating   first ap        
#             story_graph["5.0"][action_pair][MAftM[1]][MAftM][BefMM[1]][BefMM]

#     return story_graph


def find_story(story_graph, tension_curve):
    logger.info("Starting story generation: {}".format(tension_curve))
    tension1, tension2, tension3 = tension_curve[2], tension_curve[1], tension_curve[0]

    # ================================================================
    ap1 = None
    used_ap1 = []
    prev_events_ratings = None
    possible_prev_ratings = set([])
    while True:
        try:
            ap1, used_ap1 = choice_from_rest(story_graph[tension1].keys(),
                                             used_ap1)
        except IndexError:
            # tried all possible ap1
            message = "No further story could be found with 2nd tension: {}, available: {}"\
                .format(tension2, possible_prev_ratings)
            logging.warning(message)
            break

        ap1_node = story_graph[tension1][ap1]
        prev_events_ratings = ap1_node.keys()

        if tension2 not in prev_events_ratings:
            possible_prev_ratings |= set(prev_events_ratings)
            prev_events_ratings = []
            continue

        logger.debug("Chosen final ap: {}".format(ap1))
        logger.debug("Ratings available for back planing: {}".
                     format(prev_events_ratings))

        # ================================================================
        ap2 = None
        used_ap2 = []
        prev_events_ratings2 = None
        possible_prev_ratings2 = set([])
        while True:
            try:
                ap2, used_ap2 = choice_from_rest(ap1_node[tension2].keys(),
                                                 used_ap2)
            except IndexError:
                # chosen ap1 doesn't lead to ap2 that have tension3 available
                # break out and jump to continue, that leads to next ap1 choice
                message = "  No ap2 could be found from final ap {} leading to "\
                          .format(ap1) +\
                          "3rd tension: {}, but ap2s were found leading to 3rd "\
                          .format(tension3) +\
                          "tensions: {}".format(possible_prev_ratings2)
                logging.warning(message)
                break

            ap2_node = ap1_node[tension2][ap2]
            prev_events_ratings2 = ap2_node.keys()

            if tension3 not in prev_events_ratings2:
                possible_prev_ratings2 |= set(prev_events_ratings2)
                prev_events_ratings2 = []
                continue

            logger.debug("Chosen penultimate ap: {}".format(ap2))
            logger.debug("Ratings available for back planing: {}".
                         format(prev_events_ratings2))

            # ================================================================
            ap3 = choice(ap2_node[tension3].keys())
            logger.debug("Chosen ante-penultimate ap: {}".format(ap3))

            return [ap3, ap2, ap1]
        # ================================================================
        prev_events_ratings = []
        continue
    # ================================================================
    return []

tension_curve = ["4.0", "5.0", "5.0"]
sg = create_story_graph_back(tension_curve)
story = find_story(sg, tension_curve)
print story
