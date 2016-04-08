'''
Defines functions that return connector sentences based on tension level.
'''
from discourse_locations import rand


DISCOURSE_CONNECTORS = ['but', 'and', 'so', 'yet']

CLIMAX_CONNECTORS = [
                ' However, ',
                ' Nonewithstanding, ',
                ' Nevertheless, ',
                ' Finally, ',
                ' Crucially, ',
                ' Still, ',
                ]
CLIMAX_FINALISERS = [
                ' Horrible. ',
                ' Definitely not cool. ',
                ' Good story. '
                ]
RANDOM_CONNECTORS = [
                " Anyway, ",
                " Now without further beating around the bush, ",
                " Now let us resume our story. ",
                " No intention of wandering off, so ",
                " Would you believe it if I told you that "
                ]


def get_connector(textContent):
    if len(textContent) == 3:
        text, tension, has_descr = textContent
    else:
        text, tension = textContent
    # add connector according to available description
    if tension == '5.0':
        # prepend the connector
        text = rand(CLIMAX_CONNECTORS) + text + rand(CLIMAX_FINALISERS)
    elif not any(text.endswith(c) for c in DISCOURSE_CONNECTORS):
        # append the connector
        text = text + rand(RANDOM_CONNECTORS)
    return (text, tension)
