import collections
from pprint import pprint
import pdb
import logging
from random import choice

from data import ACTION_PAIRS, MIDPOINTS
from data import find_by_attribute
from helpers import choice_from_rest

logging.basicConfig(level=logging.INFO)
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
            logger.debug("No tension for action pair: {}, {}".
                           format(action_pair[0],
                                  action_pair[2]))
        if not action_pair2[1]:
            logger.debug("No tension for action pair: {}, {}".
                           format(action_pair2[0],
                                  action_pair2[2]))

        return None

    return (action_pair, action_pair2)


def find_next_steps(action, backw=True):
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

    if backw:
        known_midpoint = action[0]
        column = "After Midpoint"
        logging.debug("Finding previous midpoint for " + known_midpoint)
    else:
        known_midpoint = action[2]
        column = "Before Midpoint"
        logging.debug("Finding next midpoint for " + known_midpoint)

    try:
        midpoints = find_by_attribute(MIDPOINTS,
                                      column,
                                      known_midpoint)
    except:
        # no midpoints for this action
        logging.debug("No Midpoint: " + known_midpoint)
        return []

    # transform (BefM, M, AftM) to [((BefM, rating, M)), (M, rating, AftM)]
    ap_tuples = []
    for mp in midpoints:
        ap_tuple = midpoint_to_actionpairs(mp)
        if ap_tuple:
            ap_tuples.append(ap_tuple)
    return ap_tuples


def create_story_graph_backw(climax_tension):
    logger.info(
        "Backwards generating story graph from tension " + climax_tension
    )
    story_graph = Tree()

    climaxes = find_by_attribute(ACTION_PAIRS, "Tension", climax_tension)
    logger.debug(str(len(climaxes)) + " climaxes found")

    # create initial set of nodes to expand
    expand_nodes = []
    for climax in climaxes:
        action_pair = (climax["Before"], climax["Tension"], climax["After"])
        # put node in Graph
        story_graph[climax_tension][action_pair]
        ap_node = story_graph[climax_tension][action_pair]
        expand_nodes.append((ap_node, action_pair))

    # expand nodes
    for current_ap_node, action_pair in expand_nodes:
        previous_steps = find_next_steps(action_pair, backw=True)

        for (BefMM, MAftM) in previous_steps:
            #               rating   prev ap
            current_ap_node[MAftM[1]][MAftM]
            penultimate_ap_node = current_ap_node[MAftM[1]][MAftM]
            #                   rating   first ap
            penultimate_ap_node[BefMM[1]][BefMM]

    return story_graph


def create_story_graph_forw(climax_tension):
    logger.info(
        "Forward generating story graph from tension " + climax_tension
    )
    story_graph = Tree()

    climaxes = find_by_attribute(ACTION_PAIRS, "Tension", climax_tension)
    logger.debug(str(len(climaxes)) + " climaxes found")

    # create initial set of nodes to expand
    expand_nodes = []
    for climax in climaxes:
        action_pair = (climax["Before"], climax["Tension"], climax["After"])
        # put node in Graph
        story_graph[climax_tension][action_pair]
        ap_node = story_graph[climax_tension][action_pair]
        expand_nodes.append((ap_node, action_pair))

    # expand nodes
    for current_ap_node, action_pair in expand_nodes:
        next_steps = find_next_steps(action_pair, backw=False)

        for (BefMM, MAftM) in next_steps:
            #               rating   next ap
            current_ap_node[BefMM[1]][BefMM]
            next_ap_node = current_ap_node[BefMM[1]][BefMM]
            #            rating   last ap
            next_ap_node[MAftM[1]][MAftM]

    return story_graph


def find_storystep(story_graph, tension_curve, backw):
    """Takes a story graph of type Tree and a 3-element tension curve,
    and back generates a story consisting of three action pairs that is
    consistent with the curve."""

    if backw:
        tension1, tension2, tension3 = tension_curve[::-1]
    else:
        tension1, tension2, tension3 = tension_curve
    logger.info("Starting story generation: {}".format([tension1,
                                                        tension2,
                                                        tension3]))

    # ================================================================
    used_ap1 = []
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
        used_ap2 = []
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
                continue

            logger.debug("Chosen penultimate ap: {}".format(ap2))
            logger.debug("Ratings available for back planing: {}".
                         format(prev_events_ratings2))

            # ================================================================
            ap3 = choice(ap2_node[tension3].keys())
            logger.debug("Chosen ante-penultimate ap: {}".format(ap3))

            if backw:
                return [ap3, ap2, ap1]
            return [ap1, ap2, ap3]
        # ================================================================
        prev_events_ratings = []
        continue
    # ================================================================
    return []


def find_next_storystep(prev_node, tension, next_tension, used_aps):
    possible_next_ratings = set([])
    while True:
        try:
            next_ap, used_aps = choice_from_rest(prev_node[tension].keys(),
                                                 used_aps)
            next_ap_node = prev_node[tension][next_ap]
            next_ratings = next_ap_node.keys()

            if next_tension not in next_ratings:
                possible_next_ratings |= set(next_ratings)
                continue

            logger.debug("Chosen ap: {}".format(next_ap))

            return next_ap, next_ap_node, used_aps

        except IndexError:
            # previous node doesn't lead to any ap that would have the right
            # next tension
            # break out and jump to continue, that leads to next ap1 choice
            message = "No ap could be found leading to tension {} "\
                      .format(next_tension) +\
                      "but aps leading to tensions {} were available"\
                      .format(possible_next_ratings)
            logging.warning(message)
            return None, None, used_aps


def find_story_climax(tension_curve, story_graph_f, story_graph_b):
    tension1, tension2, tension3, tension4, tension5 = tension_curve

    # ================================================================
    used_ap1 = []
    possible_prev_ratings = set([])
    possible_next_ratings = set([])

    while True:
        try:
            # choose one of unused aps
            # only if they offer the requested 2nd and 4th ratings
            # if not, note down which alternative ratings are available
            ap3, used_ap3 = choice_from_rest(story_graph_b[tension3].keys(),
                                             used_ap1)

            ap3_node_b = story_graph_b[tension3][ap3]
            prev_events_ratings = ap3_node_b.keys()
            if tension2 not in prev_events_ratings:
                possible_prev_ratings |= set(prev_events_ratings)
                continue

            ap3_node_f = story_graph_f[tension3][ap3]
            next_events_ratings = ap3_node_f.keys()
            if tension4 not in next_events_ratings:
                possible_next_ratings |= set(next_events_ratings)
                continue

            logger.debug("Chosen climax ap: {}".format(ap3))
        except IndexError:
            # tried all possible climax aps
            message = "No further story could be found with 2nd tension: {} (available: {})" +\
                      "or 4th tension {} (available: {})".\
                      format(tension2, possible_prev_ratings,
                             tension4, possible_next_ratings)
            logging.warning(message)
            break

        # ================================================================
        logger.debug("Finding pre-climax story")
        used_ap2s = []
        ap2, ap2_node, used_ap2s = find_next_storystep(ap3_node_b,
                                                       tension2,
                                                       tension1,
                                                       used_ap2s)
        if not ap2_node:
            # no continuation for previous story, try other climax
            logger.debug("No fitting pre story found, trying other climax")
            continue

        ap1 = choice(ap2_node[tension1].keys())
        logger.debug("Chosen first ap: {}".format(ap1))

        # ================================================================
        logger.debug("Finding post-climax story")
        used_ap4s = []
        ap4, ap4_node, used_ap4s = find_next_storystep(ap3_node_f,
                                                       tension4,
                                                       tension5,
                                                       used_ap4s)
        if not ap4_node:
            # no continuation for next story, try other climax
            logger.debug("No fitting post story found, trying other climax")
            continue

        ap5 = choice(ap4_node[tension5].keys())
        logger.debug("Chosen last ap: {}".format(ap5))

        return [ap1, ap2, ap3, ap4, ap5]

    # ================================================================
    return []

tension_curve = ["3.0", "4.0", "5.0", "4.0", "3.0"]
sg_b = create_story_graph_backw(tension_curve[2])
sg_f = create_story_graph_forw(tension_curve[2])
story = find_story_climax(tension_curve, sg_f, sg_b)
print story

# tension_curve = ["5.0", "4.0", "3.0"]
# sg = create_story_graph_forw(tension_curve[0])
# story = find_storystep(sg, tension_curve, backw=False)
# print story

# tension_curve = ["1.0", "2.0", "4.0", "5.0", "5.0"]
# t1 = tension_curve[-3:]
# sg1 = create_story_graph_back(t1)
# story1 = find_storystep_back(sg1, t1)
# t2 = tension_curve[:3]
# sg2 = create_story_graph_back(t2)
# story2 = find_storystep_back(sg2, t2)
# print story2 + story1
