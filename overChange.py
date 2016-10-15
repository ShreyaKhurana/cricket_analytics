# -*- coding: utf-8 -*-
"""
Created on Sat Jan 02 13:45:15 2016

@author: Shreya Khurana
"""

import numpy as np
from tqdm import *

maxRuns = 601
batsmen = 12
numBalls = 300

keyMat = np.zeros([maxRuns, batsmen, batsmen], dtype = np.float_)
keyMatCopy = np.zeros([maxRuns, batsmen, batsmen], dtype = np.float_) #to keep track of previous iteration values of the matrix

keyMatCopy[0][0][1] = 1

# print keyMat[0][0][1]

# We have different probability matrices for different batting orders.
# Essentialy, just one matrix whose rows are shuffled according to the 
# order whose total runs you want to check. 

# If we want to find the optimal bating order we'll have to check 11!
# orders. However since that is not efficient at all, we use some strategy 
# to check. We check the current order of the ODI batting team, the 'best'
# according to us i.e. according to the best batsmen first and then the bowlers
# Then we see the 'worst' batting order in which players like Umesh Yadav and 
# Shami come first and then the batsmen. The opposite of the 'best'.

# We decide who's the best according to our own funny algo. For each of the 
# player we take the whole team to be made of that player itself. For eg.
# an ODI team made of 11 Shikhar Dhawans..................looooool
# Then we compare the runs each of these 'one-man teams' would make
# and rank them accordingly.

# Comment out any two matrices to see the result one order

#probRunType = {'P_d':0.1, 'P0':0.2, 'P1':0.2, 'P2':0.1,'P3':0.1, 'P4':0.2, 'P6':0.1}
#probRunType = {'P_d':0.027, 'P0':0.513, 'P1':0.311, 'P2':0.071,'P3':0.006, 'P4':0.060, 'P6':0.012}
#probRunType = {0:{'P0':.561, 'P1': .231, 'P2': .066, 'P3':.013, 'P4': .108, 'P6':.011, 'P_d': .022},
#               1:{'P0':.515, 'P1': .311, 'P2': .071, 'P3':.006, 'P4': .084, 'P6':.009, 'P_d': .021},\
#               2:{'P0':.541, 'P1': .280, 'P2': .078, 'P3':.010, 'P4': .069, 'P6':.020, 'P_d': .024},\
#               3:{'P0':.540, 'P1': .295, 'P2': .058, 'P3':.012, 'P4': .071, 'P6':.018, 'P_d': .025},\
#               4:{'P0':.527, 'P1': .294, 'P2': .070, 'P3':.007, 'P4': .080, 'P6':.020, 'P_d': .032},\
#               5:{'P0':.563, 'P1': .284, 'P2': .058, 'P3':.008, 'P4': .078, 'P6':.009, 'P_d': .025},\
#               6:{'P0':.533, 'P1': .319, 'P2': .060, 'P3':.004, 'P4': .067, 'P6':.016, 'P_d': .039},\
#               7:{'P0':.533, 'P1': .313, 'P2': .055, 'P3':.007, 'P4': .078, 'P6':.007, 'P_d': .075},\
#               8:{'P0':.595, 'P1': .271, 'P2': .053, 'P3':.003, 'P4': .070, 'P6':.007, 'P_d': .106},\
#               9:{'P0':.575, 'P1': .304, 'P2': .013, 'P3':.000, 'P4': .056, 'P6':.048, 'P_d': .168},\
#               10:{'P0':.663, 'P1': .214, 'P2': .026, 'P3':.000, 'P4': .084, 'P6':.012, 'P_d': .205}}

#probRunType = {0:{'P0':.663, 'P1': .214, 'P2': .026, 'P3':.000, 'P4': .084, 'P6':.012, 'P_d': .205},
#               1:{'P0':.575, 'P1': .304, 'P2': .013, 'P3':.000, 'P4': .056, 'P6':.048, 'P_d': .168},\
#               2:{'P0':.595, 'P1': .271, 'P2': .053, 'P3':.003, 'P4': .070, 'P6':.007, 'P_d': .106},\
#               3:{'P0':.533, 'P1': .313, 'P2': .055, 'P3':.007, 'P4': .078, 'P6':.007, 'P_d': .075},\
#               4:{'P0':.533, 'P1': .319, 'P2': .060, 'P3':.004, 'P4': .067, 'P6':.016, 'P_d': .039},\
#               5:{'P0':.563, 'P1': .284, 'P2': .058, 'P3':.008, 'P4': .078, 'P6':.009, 'P_d': .025},\
#               6:{'P0':.527, 'P1': .294, 'P2': .070, 'P3':.007, 'P4': .080, 'P6':.020, 'P_d': .032},\
#               7:{'P0':.540, 'P1': .295, 'P2': .058, 'P3':.012, 'P4': .071, 'P6':.018, 'P_d': .025},\
#               8:{'P0':.541, 'P1': .280, 'P2': .078, 'P3':.010, 'P4': .069, 'P6':.020, 'P_d': .024},\
#               9:{'P0':.515, 'P1': .311, 'P2': .071, 'P3':.006, 'P4': .084, 'P6':.009, 'P_d': .021},\
#               10:{'P0':.561, 'P1': .231, 'P2': .066, 'P3':.013, 'P4': .108, 'P6':.011, 'P_d': .022}}

# Probability matrix of the type of runs each player can score. This was collected manually, although
# we tried to scrape it at first. n00bs.

# For example, the first player has a 0.563 probability that he'll play a dot ball, a .284 that he'll
# take a single and so on.

probRunType = {0:{'P0':.563, 'P1': .284, 'P2': .058, 'P3':.008, 'P4': .078, 'P6':.009, 'P_d': .025},
               1:{'P0':.561, 'P1': .231, 'P2': .066, 'P3':.013, 'P4': .108, 'P6':.011, 'P_d': .022},\
               2:{'P0':.515, 'P1': .311, 'P2': .071, 'P3':.006, 'P4': .084, 'P6':.009, 'P_d': .021},\
               3:{'P0':.540, 'P1': .295, 'P2': .058, 'P3':.012, 'P4': .071, 'P6':.018, 'P_d': .025},\
               4:{'P0':.527, 'P1': .294, 'P2': .070, 'P3':.007, 'P4': .080, 'P6':.020, 'P_d': .032},\
               5:{'P0':.541, 'P1': .280, 'P2': .078, 'P3':.010, 'P4': .069, 'P6':.020, 'P_d': .024},\
               6:{'P0':.533, 'P1': .319, 'P2': .060, 'P3':.004, 'P4': .067, 'P6':.016, 'P_d': .039},\
               7:{'P0':.533, 'P1': .313, 'P2': .055, 'P3':.007, 'P4': .078, 'P6':.007, 'P_d': .075},\
               8:{'P0':.595, 'P1': .271, 'P2': .053, 'P3':.003, 'P4': .070, 'P6':.007, 'P_d': .106},\
               9:{'P0':.575, 'P1': .304, 'P2': .013, 'P3':.000, 'P4': .056, 'P6':.048, 'P_d': .168},\
               10:{'P0':.663, 'P1': .214, 'P2': .026, 'P3':.000, 'P4': .084, 'P6':.012, 'P_d': .205}}
               
# For each ball, we'll take into account all the actions that can happen
# For eg. a 1, a 2, a 4 or 6 etc. The batsman can be bowled/run out/ stumped/caught too, so we'll 
# take the probability that he's out as well.

for ball in tqdm(range(numBalls)):

    # To actually see how slow our algo is, you can just see how as he game progresses, and the no of
    # computations increase, notice the difference in time after each ball is processes.

    print 'ball', ball

    nonZero = np.transpose(np.nonzero(keyMatCopy))
 
    exhausted = []

    for index in nonZero:
        if (max(index[1], index[2]) < 11)  & (index[0] < (maxRuns-6)):
            runs = index[0]
            B1 = index[1]
            B2 = index[2]
            if (ball > 0) & (ball % 6 == 0):
                keyMat[runs][max(B1,B2) + 1][B1] += keyMatCopy[runs][B1][B2]*probRunType[B2]['P_d']/sum(probRunType[B2].values())
                keyMat[runs + 1][B1][B2] += keyMatCopy[runs][B1][B2]*probRunType[B2]['P1']/sum(probRunType[B2].values())
                keyMat[runs + 2][B2][B1] += keyMatCopy[runs][B1][B2]*probRunType[B2]['P2']/sum(probRunType[B2].values())
                keyMat[runs + 3][B1][B2] += keyMatCopy[runs][B1][B2]*probRunType[B2]['P3']/sum(probRunType[B2].values())
                keyMat[runs + 4][B2][B1] += keyMatCopy[runs][B1][B2]*probRunType[B2]['P4']/sum(probRunType[B2].values())
                keyMat[runs + 6][B2][B1] += keyMatCopy[runs][B1][B2]*probRunType[B2]['P6']/sum(probRunType[B2].values())
                keyMat[runs][B2][B1] += keyMatCopy[runs][B1][B2]*probRunType[B2]['P0']/sum(probRunType[B2].values())
            else:
                keyMat[runs][max(B1,B2) + 1][B2] += keyMatCopy[runs][B1][B2]*probRunType[B1]['P_d']/sum(probRunType[B1].values())
                keyMat[runs + 1][B2][B1] += keyMatCopy[runs][B1][B2]*probRunType[B1]['P1']/sum(probRunType[B1].values())
                keyMat[runs + 2][B1][B2] += keyMatCopy[runs][B1][B2]*probRunType[B1]['P2']/sum(probRunType[B1].values())
                keyMat[runs + 3][B2][B1] += keyMatCopy[runs][B1][B2]*probRunType[B1]['P3']/sum(probRunType[B1].values())
                keyMat[runs + 4][B1][B2] += keyMatCopy[runs][B1][B2]*probRunType[B1]['P4']/sum(probRunType[B1].values())
                keyMat[runs + 6][B1][B2] += keyMatCopy[runs][B1][B2]*probRunType[B1]['P6']/sum(probRunType[B1].values())
                keyMat[runs][B1][B2] += keyMatCopy[runs][B1][B2]*probRunType[B1]['P0']/sum(probRunType[B1].values())
        else: 
          exhausted.append(index)

#    totRuns = 0
#    for runs in range(maxRuns):
#        totRuns += sum(sum(keyMat[runs][:][:]))*runs
                
    #print totRuns
    keyMatCopy = np.copy(keyMat)
    keyMat = np.zeros([maxRuns, batsmen, batsmen], dtype = np.float_)
    for i in exhausted:
        keyMat[i[0]][i[1]][i[2]] = keyMatCopy[i[0]][i[1]][i[2]]
           
totRuns = 0
for runs in range(maxRuns):
    totRuns += sum(sum(keyMatCopy[runs][:][:]))*runs
    
print 'Total Runs' + str(totRuns)