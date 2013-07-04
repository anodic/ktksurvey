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
#from models import Question, Survey, Category
#from forms import ResponseForm


def index(request):
	return render(request, 'index.html')

def survey_classification(request):
	# get session key	
	sessionKey = request.session._session_key
	
	if request.method == 'POST':
		form = Classification_form(request.POST,sessionKey=sessionKey)
		if form.is_valid():
			#questions = ClassificationQ.objects.order_by("id")
			#for q in questions
				#form[]
			
			form.save_answers()
			
			# GET NUMBER OF ELEMENTS PER SILOS FORM THE DATASET
			# get silos from dataset
			silos = Silo.objects.order_by("name")
			# initialize empty list to save elements per silos
			elemsPerSilos = []
			# iterate through silos and count elements
			for silo in silos:
				elemsPerSilos.append(silo.elements.count())
			
			# generate vignettes for this user
			vigGeneratorResult = vrg.generate_vignettes(elemsPerSilos,2,4,5)
			
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
	sessionKey = request.session._session_key
	#subject = 222
	vignete = math.ceil(float(vignettePageNumber)/2)
	if (int(vignettePageNumber) % 2)==0:
		questionTypeId = 2
		answerType = 2
		answerEmotion= True
	else:
		questionTypeId = 1
		answerType = 1
		answerEmotion= False
	
	elementsForVignette = request.session['vigDict'][str(int(vignete))]#["A3","B2","C3","D4"]
	statements=[]
	elements = []
	for elem in elementsForVignette:
		grabbedElement = Element.objects.get(code=elem)
		statements.append(grabbedElement.statement)
		elements.append(grabbedElement)
	#statements = Element.objects.order_by("id")
	if request.method == 'POST':
		form = VignetteForm(request.POST,sessionKey=sessionKey, vignete=vignete, questionTypeId=questionTypeId, elements=elements, answerType=answerType)
		if form.is_valid():
			#questions = ClassificationQ.objects.order_by("id")
			#for q in questions
				#form[]
			
			form.save()
			
			#return render(request,'confirmation.html')
			if int(vignettePageNumber)<2*len(request.session['vigDict']):
				return HttpResponseRedirect("/vignete/%s" % str(int(vignettePageNumber)+1))
			elif int(vignettePageNumber)>=2*len(request.session['vigDict']):
				request.session.flush()
				return render(request,'confirmation.html')
	
	form = VignetteForm(sessionKey=sessionKey, vignete=vignete, questionTypeId=questionTypeId, elements=elements, answerType=answerType)
	
	
	
	return render(request, 'survey_vignete.html',{'statements': statements,'form':form,'answer':answerEmotion})
	
#def SurveyDetail(request, id):
#	survey = Survey.objects.get(id=id)
	#category_items = Category.objects.filter(survey=survey)
	#categories = [c.name for c in category_items]
	#print 'categories for this survey:'
	#print categories
	#if request.method == 'POST':
	#	form = ResponseForm(request.POST, survey=survey)
	#	if form.is_valid():
	#		response = form.save()
	#		return HttpResponseRedirect("/confirm/%s" % response.interview_uuid)
	#else:
	#	form = ResponseForm(survey=survey)
	#	print form
	#	# TODO sort by category
	#return render(request, 'survey.html', {'response_form': form, 'survey': survey, 'categories': categories})

#def Confirm(request, uuid):
#	email = settings.support_email
#	return render(request, 'confirm.html', {'uuid':uuid, "email": email})

#def privacy(request):
#	return render(request, 'privacy.html')


