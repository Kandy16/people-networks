# -*- coding: utf-8 -*-
"""
@version: 1.2 // 01.03.2017
@author: Tobias Thesing

This class is handles input, output and calculations of the network analysis part
and should make a communication process between the steps possible.
"""


import networkx as nx
import numpy as np
from pprint import pprint
import csv


filename = '2016_12.csv'
attfilename = 'politician-data.csv'


# Reads a csv file containing an edgelist and generates a networkX graph out of it.

def readedgelist(filename):

    with open(filename, 'rb') as inf:
        next(inf, '')   # skip a line
        G = nx.read_edgelist(inf, delimiter=',', create_using=nx.DiGraph(), nodetype=int, encoding="utf-8")
    
    return G


# Reads a csv file containing node IDs and attributes, and generates a dictionary.
# The dictionary has the node ID as key and maps it to an attributes array with
# [name, gender, birthDate and nationality] in this order.
# To retrieve a value from the dictionary, use attdic[id][p]
# where p is the position of the attribute (0 for name, 1 for gender,
# 2 for birthDate, 3 for nationality)

def readattributes(filename):
    
    a = np.genfromtxt(filename, delimiter='\t', names=True, dtype=None)
        
    attdic = {} 
    
    ids = a['ID']
    names = a['name']
    genders = a['gender']
    bdays = a['birthDate']
    nats = a['nationality']
    
    attributes = np.vstack((names, genders, bdays, nats)).T


    for i in range(len(ids)):
        attdic[ids[i]] = attributes[i]    
    
#    print (attdic[786391][3])
        
    return attdic    


# Creates a dictionary containing all node IDs of the given network as keys.
# The values are tuples consisting of different statistics:
# index 0: in-degree
# index 1: out-degree
# (to be expanded)
# values can be accessed with valtab[id][index]

def createvaluetable(network):
        
    nodes = nx.nodes(network)
    
    indegrees = calcindegrees(network)    
    outdegrees = calcoutdegrees(network) 
    kcores = calckcores(network)

    values = [indegrees, outdegrees, kcores]

    valtab = {}

    for n in nodes:
        valtab[n] = [v[n] for v in values]
    
    return valtab;


# Converts the value table, given as a dictionary with node id as key and
# a list as value to a .csv file. The file contains only numbers, delimited
# by a colon. The first number in each row is the node id by which the list
# is sorted.

def writevalues(table, filename):
    
    with open(filename, 'w', newline='') as csvfile:

        writer = csv.writer(csvfile, delimiter=',')

        writer.writerow(['node','indegree','outdegree','kcore'])        
        
        for key in sorted(table.keys()):
            
            v1 = table[key][0]
            v2 = table[key][1]
            v3 = table[key][2]
            
            writer.writerow([key,v1,v2,v3])
    
    return


# Creates a list of all time frame names.

def generatetimeframes():
    
    tf = []
    
    for y in range (2001, 2017):
        for m in range (1, 13):
            ys = str(y)
            if (m <= 9):
                ms = '0'+str(m)
            else:
                ms = str(m)
            tf.append(ys+'_'+ms)
    
    return tf


# Runs the complete per-node analysis process for all time frames.
# Requires all source files in the directory and may take up to 5 minutes.  
        
def processall():
    
    tf = generatetimeframes()
    
    for t in tf:
        network = readedgelist(t+'.csv')
        network.remove_edges_from(network.selfloop_edges())
        valtab = createvaluetable(network)
        writevalues(valtab, 'values_'+t+'.csv')
        
    return
    

# Creates a dictionary that contains indegree values for each node in a given network.

def calcindegrees(network):
    
    d = network.in_degree()
    return d


# Creates a dictionary that contains outdegree values for each node in a given network.	
	
def calcoutdegrees(network):
    
    d = network.out_degree()
    
    return d


# Creates a dictionary that for each node contains the k of the larges k-core
# that is containing that node.
	
def calckcores(network):
    
    d = nx.core_number(network)
    
    return d
	

processall()


# some commands for testing purposes

# vtable = createvaluetable(readedgelist(filename))
# writevalues(vtable, 'values_2016_12.csv')
# pprint(vtable)
# pprint(readattributes(attfilename))


