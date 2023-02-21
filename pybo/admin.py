from django.contrib import admin
from .models import Question, Answer # = from pybo.models import ...

# Register your models here.
class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject']
    list_display = ['id', 'subject', 'create_date']
    ordering = ['-id'] #컬럼명 앞에 +:오름차순, -:내림차순

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)