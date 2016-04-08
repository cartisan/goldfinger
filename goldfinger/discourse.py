from create_fabula import generate_story
from random import randint
import re

# 1. Search an element in the Scalextric CSV-converted data with the corresponding columnheader and rowheader

def csv_search(filename, columnheader, rowheader):
	with open(filename, 'rt') as f:
		data = f.read()
	datalines = data.split("\n")
	
	# columnheaders
	columnheaders = datalines[0].split(";")
	columnindex = columnheaders.index(columnheader)

	# rowheaders
	rowheaders = []
	for line in datalines:
		row = line.split(";")
		rowheaders.append(row[0])
	rowindex = rowheaders.index(rowheader)
	for i, line in enumerate(datalines):
		if i == rowindex:
			return line.split(";")[columnindex]


# 2. Search an element in the NOC-data with the corresponding columnheader and rowheader

def tsv_search(filename, columnheader, rowheader):
	with open(filename, 'rt') as f:
		data = f.read()
	datalines = data.split("\n")
	
	# columnheaders
	columnheaders = datalines[0].split("\t")
	columnindex = columnheaders.index(columnheader)

	# rowheaders
	rowheaders = []
	for line in datalines:
		row = line.split("\t")
		rowheaders.append(row[0])
	rowindex = rowheaders.index(rowheader)
	for i, line in enumerate(datalines):
		if i == rowindex:
			return line.split("\t")[columnindex]

# 3. Choose a random instance from a series of possible utterances

def dice(idiomstring):
	idiomlist = idiomstring.split(", ")
	number = len(idiomlist) - 1
	index = randint(0, number)
	return idiomlist[index]
	# clean up redundant quotation marks in the data?


# 4. Replace adjective with superlative

def superlative(adjective):
	with open('cc_pattern/superlatives.txt', 'rt') as f:
		data = f.read()
	datalines = data.split("\n")
	for line in datalines:
		row = line.split("\t")
		if row[0] == adjective:
			return row[1]

print(superlative("grand"))

story = generate_story()
print(story)


# 5. Insert conjunctions between two verbs

def conjunction(tuplestory):
	verb1 = tuplestory[0]
	verb2 = tuplestory[2]
	with open("cc_pattern/Veale's action pairs.txt", 'rt') as f:
		data = f.read()
	datalines = data.split("\n")
	for line in datalines:
		row = line.split(";")
		if  row[1] == verb1 and row[3] == verb2 :
			conj = row[2]
	return conj

print(conjunction(('are_rewarded_with', '2.0', 'take_advantage_of')))


# 6. Replace A and B by characters:

#def make_characters():





# TUPLES GENERATION: PHASE 1

def generate_partial_story(tuplestory, isLast=False):
	verb1 = tuplestory[0]
	verb2 = tuplestory[2]
	intensity = tuplestory[1]
	conj = conjunction(tuplestory)
	idiom1 = dice( csv_search("cc_pattern/Veale's idiomatic actions.txt", "Idiomatic Forms", verb1) )
	idiom2 = dice( csv_search("cc_pattern/Veale's idiomatic actions.txt", "Idiomatic Forms", verb2) )

	if islast:
		if conj == "and":
			return (str(idiom1) + " " + conj  + " " + str(idiom2), intensity)
		else: 
			return (str(idiom1) + ", " + conj  + " " + str(idiom2), intensity)
	else:
		"""
		conj = conjunction(tuplestory)
		dice = randint(0, 2)
		if dice == 1:
			if conj == "and":
				return tuple(str(idiom) + " " + conj  , intensity)
			else: 
				return tuple(str(idiom) + ", " + conj  , intensity)
		else:
			return tuple(idiom, intensity)
		"""
		return (idiom1, intensity)


def introduction(firsttuple):

	verb1 = firsttuple[0]
	intensity = firsttuple[1]
	intro = dice( csv_search("cc_pattern/Veale's initial bookend actions.txt", "Establishing Action", verb1) )
	return ((str(intro + ". ")),(intensity) )

print(introduction(('are_worshipped_by', '2.0', 'condescend_to')))


def ending(lasttuple):
	verb = lasttuple[2]
	intensity = lasttuple[1]
	ending = dice( csv_search("cc_pattern/Veale's closing bookend actions.txt", "Closing Action", verb) )
	ending = ending.replace('\"', "")
	ending[0].upper()
	return ((str(ending + ". "), (intensity) ))

print(ending(('trust', '3.0', 'are_abducted_by')))




# TRYOUT






"""
for sentence in story:
	print(generate_partial_story(sentence))
"""





"""
chosen_idiom = dice(idiom)
print(chosen_idiom)

idiomlist = ['spy_on', 'are_discovered_by', 'beg_forgiveness_from', 'are_killed_by', 'haunt', 'are_exorcized_by']

story = []

for idiom in idiomlist: 
	story.append(csv_search("Veale's idiomatic actions.txt", "Idiomatic Forms", idiom))


print(". ".join(story))

"""




