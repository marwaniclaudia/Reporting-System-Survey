from django.contrib import admin

# Register your models here.
from .models import User, Csv, Question, QuestionValue, Responden, Survey, SurveyQuestion, ResponSurvey, CsvValue, Layanan

admin.site.register(User)
admin.site.register(Csv)
admin.site.register(Question)
admin.site.register(QuestionValue)
admin.site.register(Responden)
admin.site.register(Survey)
admin.site.register(SurveyQuestion)
admin.site.register(ResponSurvey)
admin.site.register(CsvValue)
admin.site.register(Layanan)