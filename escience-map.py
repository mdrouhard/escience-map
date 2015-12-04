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

args = parser.parse_args()

# setup the path argument if provided
if args.inputpath:
    path = args.inputpath
else:
    sys.exit('Error: missing input path.')


G = nx.Graph()			# Graph data structure
group = 0						# group number (category of labels; e.g., department)
groupDict = dict()	# label -> group number
labelDict = dict()	# label -> label set

# traverse subdirectories of inputpath
# stupid os.walk doesn't work the way I need it to
subdirs = os.listdir(path)
for subdir in subdirs:
	subdirpath = os.path.join(path,subdir)
	if os.path.isdir(subdirpath):
		group+=1
		print subdir
		files = os.listdir(subdirpath)
		for f in files:
			labelName = f[:-4]
			print "\t" + labelName
			fpath = os.path.join(subdirpath,f)




# for root, subdirs, files in os.walk(path):
# 	for subdir in subdirs:
# 		group+=1
# 		print subdir
# 		files = files in subdir only
# 		for f in files:
# 			print f

# 	for f in files:
# 		print f

# subdirs = [x[0] for x in os.walk(path)]                                                                            
# for subdir in subdirs:                                                                                            
#     files = os.walk(subdir).next()[2] 
#     for f in files:
# 			print subdir + "\t" + f


# # Save dictionary of organizational designations
# orgDesignations = dict()
# orgDesignations["Leadership"] = build_set("data/leadership.txt")  			
# orgDesignations["Staff"] = build_set("data/staff.txt")						
# orgDesignations["DSFellows"] = build_set("data/fellows.txt")				
# orgDesignations["PostdocFellows"] = build_set("data/postdocs.txt")			
# orgDesignations["Affiliates"] = build_set("data/affiliates.txt")		


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

