from django.contrib import admin
from vignete.models import Element, Silo, ClassificationQ, AnswerClassification, AnswerVignetes

admin.site.register(Element)
admin.site.register(Silo)
admin.site.register(ClassificationQ)
admin.site.register(AnswerClassification)
admin.site.register(AnswerVignetes)