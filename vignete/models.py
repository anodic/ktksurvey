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
	statement = models.CharField(max_length=500)
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

