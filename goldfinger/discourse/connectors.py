'''
Defines functions that return connector sentences based on tension level.
'''
from helpers import rand


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
                " No intention of wandering off, so let's proceed. ",
                " Would you believe it if I told you the following: "
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
    elif '.' not in text:
        text = text + '. '
    return (text, tension)
