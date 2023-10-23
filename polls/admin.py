from django.contrib import admin
from .models import Question, Choice
# Register your models here.

admin.site.register(Question) # admin사이트에 모델 'Question'을 등록
admin.site.register(Choice) # admin사이트에 모델 'Choice'을 등록
