'''
Created on Jul 2, 2013

@author: Ante Odic
'''
import sys
import csv
from django.core.management.base import BaseCommand, CommandError
from vignete.models import Silo, Element

# GET CURRENT PATH
import os
directory = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../../..'))

class Command(BaseCommand):
	#args = '<poll_id poll_id ...>'
	#help = 'Closes the specified poll for voting'

	def handle(self, *args, **options):
		# possible silos names
		silosNames = ['A','B','C','D','E','F','G','H','I','J','K','L']

		# create path from command line argument file
		datasetName = "\\csvdata\\" + sys.argv[2]
		csvFilePath = directory + datasetName
		
		# load csv data
		dataSet = list( csv.reader( open(csvFilePath, 'r') ) )

		# CREATE SILOS
		# find last silo code
		lastSiloCode = dataSet[-1][0][0]
		# so, how many silos are there?
		numSilos = silosNames.index(lastSiloCode)
		# get silo version
		siloVersion = dataSet[-1][2]
		# create each silo in database
		for siloIndex in range(int(numSilos)+1):
			silo = Silo()
			silo.name=silosNames[siloIndex]
			silo.version = siloVersion
			silo.save()

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
			silo.elements.add(elementObj)
 


