'''
Created on Jul 2, 2013

@author: Ante Odic
'''
import sys
import csv
from vignete.models import Silo, Element

# GET CURRENT PATH
import os
directory = os.path.dirname(os.path.abspath(__file__))

# possible silos names
silosNames = ['A','B','C','D','E','F','G','H','I','J','K','L']

# create path from command line argument file
datasetName = "\\csvdata\\" + sys.argv[1]
csvFilePath = directory + datasetName

# load csv data
dataSet = list( csv.reader( open(csvFilePath, 'r') ) )

# CREATE SILOS
# find last silo code
lastSiloCode = dataset[-1][0][0]
# so, how many silos are there?
numSilos = silosNames.index(lastSiloCode)
# get silo version
siloVersion = dataset[-1][2]
# create each silo in database
for siloIndex in range(int(numSilos)):
	silo = Silo()
	silo.name=silosNames[siloIndex]
	silo.version = siloVersion

# CREATE ELEMENTS	
for line in range(len(dataSet)):
	# write elemet stuff in database
	elementObj = Element()
	elementObj.code = dataSet[line][0]
	elementObj.statement = dataSet[line][1]
	elementObj.version = dataSet[line][2]
	elementObj.save()
	# add element into appropriate silo
	silo = Silo.objects.get(name=dataSet[line][0][0])
	silo.add(elementObj)
 


