from django.contrib import admin

# Register your models here.
from sms.models import Sms, SmsLog, SmsUser


class SmsUserAdmin(admin.ModelAdmin):
    list_display = ('phone', 'status')


admin.site.register(Sms)
admin.site.register(SmsLog)
admin.site.register(SmsUser, SmsUserAdmin)
