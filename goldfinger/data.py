from cc_pattern.noc import parse, index


# ---------------------- data tables ----------------------------
ACTION_PAIRS = parse("Veale's action pairs 2.xlsx")
MIDPOINTS = parse("Veale's script midpoints.xlsx")
LOCATIONS = parse("Veale's location listing.xlsx")
NOC = parse("Veale's The NOC List.xlsx")


# ---------------------- operations on tables ----------------------------
def find_by_attribute(table, attr, value):
    """ Finds all elements of a table where the attribute (=column of table)
    attr is (or contains) the value.
    Like: All entries of NOC with the Category Actor.

    Returns a list of table entries, each entry is a dict.

    Example:
    --------
    actors = find_by_attribute(NOC, "Category", "Actor")
    actors[0]
    >> {'Character': 'Daniel Day-Lewis', 'Weapon':...}

    lewis_roles = find_by_attribute(NOC, "Portrayed By", "Daniel Day-Lewis")
    lewis_roles[0]
    >> {'Character': 'Abraham Lincoln', 'Oppononent':...}
    """

    return index(table, attr, unique=False)[value]


# ---------------------- individual table entries ------------------------
class Row(object):
    """ Encapsulates one row from an xls list in an object-oriented fashion.
    Each property is set as an object attribut, and it's content is set
    using a list (empty, one-, or multi-elemented).
    Attributes are lower-case and space turn to underscores.
        "Weapon of Choice" --> weapon_of_choice

    Lists with specified Row subclasses:
        NOC -> Person-class

    Example: Action-pair list row(11)
    --------------------------
    pair = Row(ACTION_PAIRS[11])
    pair.before
    >> ['kill']

    Example: location list
    --------------------------
    location = Row(LOCATIONS[11])
    pair.ambience
    >> ["forlorn", "musty", "desolate", ...]
    """

    def __init__(self, row):
        for key, value in row.items():
            k2 = key.lower()
            k3 = k2.replace(" ", "_")

            # Input is a mix of strings, list, and lists of
            # empty strings. We want lists of strings or empty lists.
            newvalue = []
            if type(value) == list:
                for v in value:
                    if v:
                        newvalue.append(v.encode('utf-8'))
            elif type(value) == str or type(value) == unicode:
                if value:
                    newvalue.append(value.encode('utf-8'))
            setattr(self, k3, newvalue)

    def missing_attributes(self):
        # find empty attributes:
        missing_properties = set()
        for k, v in self.__dict__.items():
            if not v:
                missing_properties.add(k)

        return missing_properties


class Person(Row):
    def __init__(self, row):
        super(Person, self).__init__(row)

        # we had problems with nameless chars last time
        try:
            self.character[0]
        except:
            print "person.py: No name found for {}".\
                format(self.character)
            self.character = ['']

    def find_mates():
        """ Returns a list of NOC indices indicating chars
        that can be used as mate for this char.
        """
        pass
