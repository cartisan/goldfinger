'''
Defines functions that return connector sentences based on tension level.
'''
from discourse_locations import rand


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
                ' Anyway, ',
                " Now without further beating around the bush, ",
                " Now let us resume our story. ",
                " No intention of wandering off, so ",
                " Would you believe it if I told you that "
                ]


def get_connector(textTriple):
    text, tension, has_descr = textTriple
    # add connector according to available description
    if tension == '5.0':
        # prepend the connector
        text = text[0].lower() + text[1:]
        text = rand(CLIMAX_CONNECTORS) + text
    # append the connector
    text = text + rand(RANDOM_CONNECTORS)
    return text
