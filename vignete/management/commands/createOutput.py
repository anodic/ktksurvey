'''
Created on Jul 2, 2013

@author: Ante Odic
'''
import sys
import csv
from django.core.management.base import BaseCommand, CommandError
from vignete.models import AnswerClassification, ClassificationQ, AnswerVignetes

import csv



# GET CURRENT PATH
import os
directory = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../../..'))

class Command(BaseCommand):
	#args = '<poll_id poll_id ...>'
	#help = 'Closes the specified poll for voting'

	def handle(self, *args, **options):
		
		#output file name
		outputFile = sys.argv[2]
		
		# create path from command line argument file
		datasetName = "\\output\\" + outputFile
		outputFilePath = directory + datasetName
		
		# open file
		with open(outputFilePath, 'wb') as myfile:
			writerIntoFile = csv.writer(myfile, quoting=csv.QUOTE_NONE)
			# GET SUBJECTS' IDS
			# get distinct subjects' ids from clasification answers
			subjectIdsQuerySet = AnswerClassification.objects.values('subject').distinct()
			# initialize empty list for user ids
			subjectIds=[]
			# parse subjects' ids from QuerySet
			for k in range(len(subjectIdsQuerySet)):
				subjectIds.append(int(subjectIdsQuerySet[k]["subject"]))
			subjectIds = sorted(subjectIds)
			
			# FOR EACH SUBJECT CREATE AN OUTPUT LINE
			for subjectId in subjectIds:
				# initialize list for each subject's output row
				outputRow = []	
				# add subject's Id to output row
				outputRow.append(str(subjectId))
				# GET CLASSIFICATION QUESTIONS' IDS
				# get distinct classification questions' ids from clasification questions
				classQIdsQuerySet = ClassificationQ.objects.values('id').distinct()
				# initialize empty list for classQ ids
				classQIds=[]
				#parse classqs' ids from QuerySet
				for k in range(len(classQIdsQuerySet)):
					classQIds.append(int(classQIdsQuerySet[k]["id"])) 
				classQIds = sorted(classQIds)
				# ADD ANSWER FOR EACH CLASIFICATION QUESTION IN OUTPUT ROW
				for i, classQuestion in enumerate(classQIds):
					classAnswer = AnswerClassification.objects.get(subject=subjectId,questionid=classQuestion)
					outputRow.append(str(classAnswer.answer))
				# GET VIGNETTES' IDS
				# get distinct vignettes ids from vignette answers
				vignetteIdsQuerySet = AnswerVignetes.objects.values('vignete').distinct()
				# initialize empty list for classQ ids
				vignetteIds=[]
				#parse classqs' ids from QuerySet
				for k in range(len(vignetteIdsQuerySet)):
					vignetteIds.append(int(vignetteIdsQuerySet[k]["vignete"])) 
				vignetteIds = sorted(vignetteIds)	
				# FOR EACH VIGNETTE FIND ELEMENTS USED
				for vignetteId in vignetteIds:
					# get vignette unique database id
					vignetteUniqueID = AnswerVignetes.objects.get(subject=subjectId,vignete=vignetteId,questionType=1)
					# get elements for specific vignette unique database id
					elements = vignetteUniqueID.element.all()
					# add each element id into output row
					for k in range(len(elements)):
						outputRow.append(str(elements[k].id))
					# add answer to type 1 question into outputRow
					outputRow.append(str(AnswerVignetes.objects.get(subject=subjectId,vignete=vignetteId,questionType=1).answer))
					# add answer to type 1 question into outputRow
					outputRow.append(str(AnswerVignetes.objects.get(subject=subjectId,vignete=vignetteId,questionType=2).answer))
				
				# ADD OUTPUTROW INTO OUTPUT FILE
				writerIntoFile.writerow(outputRow)
					
		#import pdb; pdb.set_trace()
		#ante=43	