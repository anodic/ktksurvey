from django import forms
from django.forms import models
from django.utils.safestring import mark_safe
from vignete.models import ClassificationQ, AnswerClassification, AnswerVignetes, VigneteQuestion, UserIds

class HorizontalRadioRenderer(forms.RadioSelect.renderer):
  def render(self):
    return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))

class Classification_form(forms.Form):
	
	def __init__(self, *args, **kwargs):
		
		sessionKey = kwargs.pop('sessionKey')
		self.sessionKey = sessionKey
		super(Classification_form, self).__init__(*args, **kwargs)	
		# TO DO: kako ces prenjeti id subjekta: survey = kwargs.pop('survey')
		
		# for each classification question generate a field
		for q in self.getQuestions():
			if q.qType == ClassificationQ.TEXT:
				self.fields["question_%d" % q.id] = forms.CharField(label=q.statement, widget=forms.TextInput(attrs={'class': 'text_box'}))
			elif q.qType == ClassificationQ.SELECT:
				question_choices = q.get_choices()
				# add an empty option at the top so that the user has to
				# explicitly select one of the options
				question_choices = tuple([('', '-------------')]) + question_choices
				self.fields["question_%d" % q.pk] = forms.ChoiceField(label=q.statement, widget=forms.Select, choices = question_choices)
			elif q.qType == ClassificationQ.RADIO:
				question_choices = q.get_choices()
				self.fields["question_%d" % q.pk] = forms.ChoiceField(label=q.statement, 
					widget=forms.RadioSelect(renderer=HorizontalRadioRenderer), choices = question_choices)
			elif q.qType == ClassificationQ.SELECT_MULTIPLE:
				question_choices = q.get_choices()
				self.fields["question_%d" % q.pk] = forms.MultipleChoiceField(label=q.statement, widget=forms.CheckboxSelectMultiple, choices = question_choices)
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
				subj = UserIds.objects.get(sessionId=self.sessionKey)
				a.subject = subj.id
				a.questionid = ClassificationQ.objects.get(id=q_id)
				a.answer = field_value
				a.save()
				
		return q_id

class VignetteForm(forms.Form):
	#class Meta:
	#	model = AnswerVignetes	
		#fields = ('subject', 'vignete', 'questionType', 'element', 'answerType', 'answer')

			
	def __init__(self, *args, **kwargs):
		# expects a survey object to be passed in initially
		sessionKey = kwargs.pop('sessionKey')
		self.sessionKey = sessionKey
		vignete = kwargs.pop('vignete')
		self.vignete = vignete
		questionTypeId = kwargs.pop('questionTypeId')
		self.questionTypeId = questionTypeId
		elements = kwargs.pop('elements')
		self.elements = elements
		answerType = kwargs.pop('answerType')
		self.answerType = answerType
		super(VignetteForm, self).__init__(*args, **kwargs)
		

		# add a field for each survey question, corresponding to the question
		# type as appropriate.
		
		q = VigneteQuestion.objects.get(id=self.questionTypeId)
		
		if questionTypeId == 1:			
			self.fields["vigneteAnswer"] = forms.ChoiceField(label=q.question, widget=forms.RadioSelect(renderer=HorizontalRadioRenderer), choices = ((1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9)))
		elif questionTypeId == 2:
			self.fields["vigneteAnswer"] = forms.ChoiceField(label=q.question, widget=forms.RadioSelect(renderer=HorizontalRadioRenderer), choices = ((1,1),(2,2),(3,3),(4,4),(5,5))) 			
					
		

	def save(self, commit=True):
		# save the response object
		vignette = AnswerVignetes()
		
		subj = UserIds.objects.get(sessionId=self.sessionKey)
		
		vignette.subject = subj.id
		vignette.vignete = self.vignete
		vignette.questionType = VigneteQuestion.objects.get(id=self.questionTypeId)
		
		vignette.answerType = self.answerType
		
		for field_name, field_value in self.cleaned_data.iteritems():
			vignette.answer = field_value
		
		
		vignette.save()
		for elem in self.elements:
			vignette.element.add(elem) 