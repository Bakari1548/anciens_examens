from django.contrib import admin

from .models import Exam

class ExamAdmin(admin.ModelAdmin):
    list_display=('id', 'title', 'filiere', 'matiere', 'year', 'author', 'date_upload')


admin.site.register(Exam, ExamAdmin)