'''
Created on Jul 2, 2013

@author: Ante Odic
'''
import sys
import csv
from django.core.management.base import BaseCommand, CommandError
from vignete.models import VigneteQuestion

# GET CURRENT PATH
import os
directory = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../../..'))

class Command(BaseCommand):
	#args = '<poll_id poll_id ...>'
	#help = 'Closes the specified poll for voting'

	def handle(self, *args, **options):
		
		# create path from command line argument file
		datasetName = "\\csvdata\\" + sys.argv[2]
		csvFilePath = directory + datasetName
		
		# load csv data
		dataSet = list( csv.reader( open(csvFilePath, 'r') ) )

		#import pdb; pdb.set_trace()

		# CREATE QUESTIONS	
		for line in range(len(dataSet)):
			# write elemet stuff in database
			questionObject = VigneteQuestion()
			questionObject.question = dataSet[line][0]
			questionObject.save() 