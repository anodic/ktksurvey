from django.db import models

# Create your models here.

class Element(models.Model):
	code = models.CharField(max_length=10)
	statement = models.CharField(max_length=500)
	version = models.IntegerField()
	def __unicode__(self):
		return self.statement
		
class Silo(models.Model):
	name = models.CharField(max_length=200)
	elements = models.ManyToManyField(Element)
	version = models.IntegerField()
	def __unicode__(self):
		return self.name
	
	
class ClassificationQ(models.Model):
	TEXT = 'text'
	RADIO = 'radio'
	SELECT = 'select'
	SELECT_MULTIPLE = 'select-multiple'
	INTEGER = 'integer'

	QUESTION_TYPES = (
		(TEXT, 'text'),
		(RADIO, 'radio'),
		(SELECT, 'select'),
		(SELECT_MULTIPLE, 'Select Multiple'),
		(INTEGER, 'integer'),
	)
	statement = models.CharField(max_length=500)
	qType = models.CharField(max_length=200, choices=QUESTION_TYPES, default=TEXT)
	choices = models.TextField(blank=True, null=True)
	def __unicode__(self):
		return self.statement
		
		
class AnswerClassification(models.Model):
	subject = models.CharField(max_length=50)
	questionid = models.ForeignKey(ClassificationQ)
	answer = models.CharField(max_length=50)
	
		
class VigneteQuestion(models.Model):
	question = models.CharField(max_length=200)	
	def __unicode__(self):
		return self.question
		
class AnswerVignetes(models.Model):
	subject = models.CharField(max_length=50)
	vignete = models.IntegerField()
	questionType = models.ForeignKey(VigneteQuestion)
	element = models.ManyToManyField(Element)
	answerType = models.IntegerField()
	answer = models.IntegerField()

	
class UserIds(models.Model):
	sessionId = models.CharField(max_length=100)
