'''
Let's generate a story, shall we?
'''

from create_fabula import generate_story
from discourse_locations import generate_location_story
from discourse_connectors import get_connector

text = "My little pony was enflowered"
tension = '5.0'

st = generate_location_story((text, tension))

st_plus = get_connector(st)

print st_plus
