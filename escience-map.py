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
from networkx.readwrite import json_graph

class Node:
	def __init__(self, index, name, group, size):
		self.index = index 			# index in graph
		self.name = name 				# label name
		self.group = group 			# group number
		self.size = size				# size of group labeled

def build_set(fileName):
	newSet = set()
	with open(fileName, "r") as f:
		for line in f:
			newSet.add(line.rstrip('\n'))

	return newSet

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
                        help='output path name')


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


G = nx.Graph()				# Graph data structure
group = 0							# group number (category of labels; e.g., department)
index = 0							# node index for graph
nodeDict = dict()			# label -> Node
nodeSetDict = dict()	# label -> Node(label) set


# traverse subdirectories of inputpath
# stupid os.walk doesn't work the way I need it to
subdirs = os.listdir(path)
for subdir in subdirs:
	subdirpath = os.path.join(path,subdir)
	if os.path.isdir(subdirpath):
		group += 1
		files = os.listdir(subdirpath)
		for f in files:
			labelName = f[:-4]
			fpath = os.path.join(subdirpath,f)
			
			# save set associated with label
			labelSet = build_set(fpath)
			nodeSetDict['labelName'] = labelSet
			# create & add node to graph and dictionary
			nodeSize = len(labelSet)
			node = Node(index, labelName, group, nodeSize)
			G.add_node(index, name=node.name, group=node.group, size=node.size)
			nodeDict['labelName'] = node
			index += 1



# print "eScience Organization Designations:"
# for key in orgDesignations:
# 	print key + ": " + str(len(orgDesignations[key]))

# print ""


# # Calculate and print non-empty intersections of sets
# index = 0
# for L in range(1, len(orgDesignations)+1):
#   for subset in itertools.combinations(orgDesignations, L):
# 	intersection = orgDesignations[subset[0]]
# 	for s in subset:
# 		intersection = intersection & orgDesignations[s]
# 	if len(intersection) > 0:
# 		print subset 
# 		print len(intersection)
# 		print ""
# 		index += 1

# print "total (non-empty) sets: " + str(index)  


# dump graph data to json
data = json_graph.node_link_data(G)
s = json.dumps(data)
print s