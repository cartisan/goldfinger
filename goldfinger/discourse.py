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

idiom = csv_search("cc_pattern/Veale's idiomatic actions.txt", "Idiomatic Forms", "disappoint")


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


#superlative = tsv_search()


"""
chosen_idiom = dice(idiom)
print(chosen_idiom)

idiomlist = ['spy_on', 'are_discovered_by', 'beg_forgiveness_from', 'are_killed_by', 'haunt', 'are_exorcized_by']

story = []

for idiom in idiomlist: 
	story.append(csv_search("Veale's idiomatic actions.txt", "Idiomatic Forms", idiom))


print(". ".join(story))

"""




