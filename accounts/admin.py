from django.contrib import admin

# Register your models here.
from accounts.models import User, UserSendCode


class UserSendCodeAdmin(admin.ModelAdmin):
    list_display = ['user', 'status', 'code']


class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'mobile', 'is_staff']


admin.site.register(User, UserAdmin)
admin.site.register(UserSendCode, UserSendCodeAdmin)
