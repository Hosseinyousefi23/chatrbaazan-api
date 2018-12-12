from django.contrib import admin

# Register your models here.
from sms.models import Sms, SmsLog, SmsUser

admin.site.register(Sms)
admin.site.register(SmsLog)
admin.site.register(SmsUser)
