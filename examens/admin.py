from django.contrib import admin

from .models import Exam
# Register your models here.

class ExamAdmin(admin.ModelAdmin):
    list_display=('title', 'branch', 'year', 'author', 'date_upload')


admin.site.register(Exam, ExamAdmin)