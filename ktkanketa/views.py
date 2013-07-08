from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core import urlresolvers
from django.contrib import messages
from vignete.models import ClassificationQ, Element, UserIds, Silo
from vignete.forms import Classification_form, VignetteForm
import datetime
import settings
import math
import vignRandGen as vrg
import ConfigParser 
#from models import Question, Survey, Category
#from forms import ResponseForm


def index(request):
	return render(request, 'index.html')

def survey_classification(request):
	# get session key	
	sessionKey = request.session._session_key
	#import pdb; pdb.set_trace()
	if request.method == 'POST':
		form = Classification_form(request.POST,sessionKey=sessionKey)
		if form.is_valid():
			#questions = ClassificationQ.objects.order_by("id")
			#for q in questions
				#form[]
			
			form.save_answers()
				
			#READ CONFIGURATION FILE
			confFileName = 'D:/Research/12-KTKanketa/ktksurvey/ktkanketa/survey.cfg'
			config = ConfigParser .RawConfigParser()
			config.read(confFileName)
			numVignettes = int(config.get('randomisationScheme', 'numVignettes'))
			numElemsPerVignettes = int(config.get('randomisationScheme', 'numElemsPerVignettes'))
			numElementAppearances = int(config.get('randomisationScheme', 'numElementAppearances'))
			#import pdb; pdb.set_trace()
					
			# GET NUMBER OF ELEMENTS PER SILOS FORM THE DATASET
			# get silos from dataset
			silos = Silo.objects.order_by("name")
			# initialize empty list to save elements per silos
			elemsPerSilos = []
			# iterate through silos and count elements
			for silo in silos:
				elemsPerSilos.append(silo.elements.count())
			
			# generate vignettes for this user
			vigGeneratorResult = vrg.generate_vignettes(elemsPerSilos,numVignettes,numElemsPerVignettes,numElementAppearances)
			
			# save generated vignettes into session 'vigDict'
			request.session['vigDict']=vigGeneratorResult["vignetteDict"]
						
			#return render(request,'confirmation.html')
			return HttpResponseRedirect("/vignete/1")
			
						
	else:
		form = Classification_form(sessionKey=sessionKey)
		if not UserIds.objects.filter(sessionId=sessionKey).exists(): 
			a = UserIds()
			a.sessionId=sessionKey
			a.save()
		#print form
	return render(request, 'survey_classification.html',{'form': form})

def vignete(request,vignettePageNumber):
	# get session key
	sessionKey = request.session._session_key
	
	#use vignettePageNumber to calculate vignete, question type, answer type
	vignete = math.ceil(float(vignettePageNumber)/2)
	if (int(vignettePageNumber) % 2)==0:
		questionTypeId = 2
		answerType = 2
		answerEmotion= True
	else:
		questionTypeId = 1
		answerType = 1
		answerEmotion= False
	
	# get appropriate elements from vigDict that was saved in survey_classification function
	elementsForVignette = request.session['vigDict'][str(int(vignete))]
	
	# initialize statements and elements
	statements=[]
	elements = []
	
	# fill statements and elements
	for elem in elementsForVignette:
		grabbedElement = Element.objects.get(code=elem)
		statements.append(grabbedElement.statement)
		elements.append(grabbedElement)
	
	# if we came here from submitting the form
	if request.method == 'POST':
		form = VignetteForm(request.POST,sessionKey=sessionKey, vignete=vignete, questionTypeId=questionTypeId, elements=elements, answerType=answerType)
		# if the form is valid save the inputs
		if form.is_valid():
			form.save()
			
			#return render(request,'confirmation.html')
			if int(vignettePageNumber)<2*len(request.session['vigDict']):
				return HttpResponseRedirect("/vignete/%s" % str(int(vignettePageNumber)+1))
			elif int(vignettePageNumber)>=2*len(request.session['vigDict']):
				request.session.flush()
				return render(request,'confirmation.html')
	
	# if we came here from classification form
	form = VignetteForm(sessionKey=sessionKey, vignete=vignete, questionTypeId=questionTypeId, elements=elements, answerType=answerType)
	
	
	
	return render(request, 'survey_vignete.html',{'statements': statements,'form':form,'answer':answerEmotion})
	

