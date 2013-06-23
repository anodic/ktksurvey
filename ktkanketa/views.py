from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core import urlresolvers
from django.contrib import messages
from vignete.models import ClassificationQ, Element
from vignete.forms import Classification_form
import datetime
import settings

#from models import Question, Survey, Category
#from forms import ResponseForm


def index(request):
	return render(request, 'index.html')

def survey_classification(request):
	#questions = ClassificationQ.objects.order_by("id")
	if request.method == 'POST':
		form = Classification_form(request.POST)
		if form.is_valid():
			#questions = ClassificationQ.objects.order_by("id")
			#for q in questions
				#form[]
			
			form.save_answers()
			
			#return render(request,'confirmation.html')
			return HttpResponseRedirect("/vignete/")
			
						
	else:
			form = Classification_form()
			
	return render(request, 'survey_classification.html',{'form': form})

def vignete(request):

	
	statements = Element.objects.order_by("id")
	

	return render(request, 'survey_vignete.html',{'statements': statements})
	
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


