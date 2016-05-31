# Meg Drouhard
# 11/20/15
# escience-stats

# Calculates statistics for sets of eScience categories

#!/usr/bin/env python
import sys
import os, os.path
import argparse
import itertools
import networkx as nx
import json
import jsonpickle
from networkx.readwrite import json_graph

class Node:
	def __init__(self, index, name, group, size):
		self.index = index 			# index in graph
		self.name = name 				# label name
		self.group = group 			# group number
		self.size = size				# size of group labeled

class Person:
	def __init__(self, stringID, displayString):
		self.stringID = stringID							# string id
		self.displayString = displayString 		# string name to display
		self.nodes = []												# list of nodes associated with person
		self.links = []												# list of links associated with person

# build set of persons from given file by stripping newlines and adding strings to set
def build_set(fileName):
	newSet = set()
	with open(fileName, "r") as f:
		for line in f:
			newSet.add(line.rstrip('\n'))

	return newSet

# update person dict pDict by adding nodeID to array of nodes for each person in 
def update_person_dict_nodes(pDict, personSet, nodeID):
	for personKey in personSet:
		# if person not in dict, create person
		if not personKey in pDict:
			pDict[personKey] = Person(personKey, personKey)

		# update person's node list
		pDict[personKey].nodes.append(nodeID)


	return	


# TODO updated dict links

# TODO sort node and link lists in dict FINALIZE

###############################################################################

# Parse arguments
parser = argparse.ArgumentParser(description='eScience Map Builder')

parser.add_argument('-i',
                        '--input-path',
                        dest='inputpath',
                        required=True,
                        help='input path name')

parser.add_argument('-o',
                        '--output-path',
                        dest='outputpath',
                        required=False,
                        help='graph output path name')

parser.add_argument('-m',
                        '--map-output-path',
                        dest='mapoutputpath',
                        required=False,
                        help='map output path name')

parser.add_argument('-p',
                        '--personal',
                        dest='personalmap',
                        required=False,
                        help='person id for individual map generation')


args = parser.parse_args()

# setup the path arguments if provided
if args.inputpath:
    path = args.inputpath
else:
    sys.exit('Error: missing input path.')

if args.outputpath:
    outfile = args.outputpath
else:
    outfile = os.path.join(path,'output.json')

if args.mapoutputpath:
    map_outfile = args.mapoutputpath
else:
    map_outfile = os.path.join(path,'map_output.json')

# if non-empty (white space treated as empty) personal id provided
if args.personalmap and not args.personalmap.isspace():
    personID = args.personalmap
else:
    personID = None

# Set up graph variables
G = nx.Graph()				# Graph data structure
group = 0							# group number (category of labels; e.g., department)
index = 0							# node index for graph
nodeDict = dict()			# label -> Node
nodeSetDict = dict()	# label -> Node(label) set

# Set up person map variables
personDict = dict()		# personID -> {displayID, nodeIDsArray, linkIDsArray}

# traverse subdirectories of inputpath
# stupid os.walk doesn't work the way I need it to
subdirs = os.listdir(path)
for subdir in subdirs:
	subdirpath = os.path.join(path,subdir)
	if os.path.isdir(subdirpath):
		group += 1
		files = os.listdir(subdirpath)
		for f in files:
			# exclude hidden files
			if not f.startswith('.'):
				labelName = f[:-4]
				fpath = os.path.join(subdirpath,f)
				
				# save set & properties associated with label
				labelSet = build_set(fpath)
				nodeSetDict[labelName] = labelSet
				nodeDict[labelName] = index
				nodeSize = len(labelSet)

				# update personDict with nodeID for this set
				update_person_dict_nodes(personDict, labelSet, index)

				# create & add node to graph and dictionary
				# full map case
				if not personID:		
					node = Node(index, labelName, group, nodeSize)
					G.add_node(index, name=node.name, group=node.group, size=node.size)
				# personal map case
				elif personID:
					if (personID in labelSet):
						print personID + " is in set " + labelName + " (nodeID=" + str(index) + ")"
						node = Node(index, labelName, group, nodeSize)
						G.add_node(index, name=node.name, group=node.group, size=node.size)

				index += 1

#TODO: bring this back if we do venn diagrams again
# # Determine non-empty intersections of sets and create graph links
# for L in range(1, len(nodeSetDict)+1):
#   for subset in itertools.combinations(nodeSetDict, L):
# 	intersection = nodeSetDict[subset[0]]
# 	for s in subset:
# 		intersection = intersection & nodeSetDict[s]
# 	if len(intersection) > 0:
# 		print len(intersection)

# Determine pairwise intersections and create graph links
for keyA in nodeSetDict:
	for keyB in nodeSetDict:
		if keyA != keyB:
			# if full network case or if person falls into boths
			if (not personID) or (personID in nodeSetDict[keyA]) or (personID in nodeSetDict[keyB]):
				intersection = nodeSetDict[keyA] & nodeSetDict[keyB]
				overlapAmt = len(intersection)
				if overlapAmt > 0:
					# print keyA + " & " + keyB + ": " + str(overlapAmt)
					indexA = nodeDict[keyA]
					indexB = nodeDict[keyB]
					# print str(indexA) + " & " + str(indexB) + ": " + str(overlapAmt)
					G.add_edge(indexA, indexB, value=overlapAmt)


# dump graph data to json
data = json_graph.node_link_data(G)
s = json.dumps(data)
with open(outfile, "w") as f:
	f.write(s)

# dump personDict data to json using jsonpickle
d = jsonpickle.encode(personDict)
with open(map_outfile, "w") as f:
	f.write(d)