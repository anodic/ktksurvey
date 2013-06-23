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
	
class ClassificationQ(models.Model):
	statement = models.CharField(max_length=500)
	
class AnswerClassification(models.Model):
	subject = models.CharField(max_length=50)
	questionid = models.ForeignKey(ClassificationQ)
	answer = models.CharField(max_length=50)
	
	
class AnswerVignetes(models.Model):
	subject = models.CharField(max_length=50)
	elements = models.ManyToManyField(Element)
	a1 = models.IntegerField()
	a2 = models.IntegerField()
	a3 = models.IntegerField()
	a4 = models.IntegerField()