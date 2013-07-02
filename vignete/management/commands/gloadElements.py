'''
Created on Jul 2, 2013

@author: Ante Odic
'''
import sys
import csv

import os
#directory = os.path.dirname(os.path.abspath(__file__))
directory = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../../..'))
print directory

datasetName = "\\csvdata\\" + sys.argv[1]
#print datasetName

#print directory

csvFilePath = directory + datasetName
print csvFilePath




