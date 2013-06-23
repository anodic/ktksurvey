from django import forms
from django.forms import models
from django.utils.safestring import mark_safe
from vignete.models import ClassificationQ, AnswerClassification

class Classification_form(forms.Form):
	
	def __init__(self, *args, **kwargs):
		
		super(Classification_form, self).__init__(*args, **kwargs)	
		# TO DO: kako ces prenjeti id subjekta: survey = kwargs.pop('survey')
		
		# for each classification question generate a field
		for q in self.getQuestions():
			self.fields["question_%d" % q.id] = forms.CharField(label=q.statement)
						
	
	def getQuestions(self):
			questions = ClassificationQ.objects.order_by("id")
			return questions
			
	
	def save_answers(self):
				
		# create an answer object for each question and associate it with this
		# response.
		for field_name, field_value in self.cleaned_data.iteritems():
			if field_name.startswith("question_"):
				# warning: this way of extracting the id is very fragile and
				# entirely dependent on the way the question_id is encoded in the
				# field name in the __init__ method of this form class.
				q_id = int(field_name.split("_")[1])
				q = ClassificationQ.objects.get(id=q_id)	
				
				a = AnswerClassification()
				a.subject = 'bla'
				a.questionid = ClassificationQ.objects.get(id=q_id)
				a.answer = field_value
				a.save()
				
		return q_id




