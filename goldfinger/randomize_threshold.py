'''
Randomly compute new treshold based on a current threshold.
sim() simulates the output for a current_max amount of layers.
'''
import random

MAX_THRESHOLD = 5
CHANCE_ON_DEVIATE = 3
DEVIATION_LIMIT = (-1, 2)


def next_threshold(current_threshold):
    '''
    Compute a new tension threshold based on the previous.
    Define a DEVIATION_LIMIT as upper and lower limit of the
    deviations.

    Input: integer current threshold
    Output: integer new threshold within bounds of deviation limit

    '''
    # check whether current threshold isn't the max
    if current_threshold == MAX_THRESHOLD:
        return current_threshold - 1

    # get new threshold
    if random.randint(0, CHANCE_ON_DEVIATE) == 0:
        # get random within range of deviation limit
        d = random.randrange(DEVIATION_LIMIT[0], DEVIATION_LIMIT[1])
        new_threshold = current_threshold + d
    else:
        new_threshold = current_threshold - 1

    # check whether new threshold did not exceed limits
    if new_threshold < 0 or new_threshold > MAX_THRESHOLD:
        return current_threshold
    else:
        return new_threshold


def sim(current_max):
    '''
    Simulate requests for new thresholds.
    For TESTING only.
    '''
    print current_max
    if current_max <= 0:
        return
    else:
        current_max = next_threshold(current_max)
        sim(current_max)


if __name__ == '__main__':
    sim(5)
