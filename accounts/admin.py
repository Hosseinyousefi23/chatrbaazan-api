from django.contrib import admin

# Register your models here.
from accounts.models import User, UserSendCode
from django.contrib.auth.admin import UserAdmin, User as UserOld


class UserSendCodeAdmin(admin.ModelAdmin):
    list_display = ['user', 'status', 'code']


class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'mobile', 'is_staff']

    def save_model(self, request, obj, form, change):
        super(UserAdmin, self).save_model(request, obj, form, change)
        obj.set_password(obj.password)
        obj.save()


# admin.site.unregister(UserOld)
admin.site.register(User, UserAdmin)
admin.site.register(UserSendCode, UserSendCodeAdmin)
