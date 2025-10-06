from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, EmailVerification


class UserAdmin(UserAdmin):
    list_display=('id', 'first_name', 'last_name', 'username', 'email', 'date_joined', 'is_active', 'is_staff')

class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'created_at', 'is_verified')

admin.site.register(User, UserAdmin)
admin.site.register(EmailVerification, EmailVerificationAdmin)