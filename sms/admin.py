from django.contrib import admin

# Register your models here.
from sms.models import Sms, SmsLog, SmsUser


class SmsUserAdmin(admin.ModelAdmin):
    list_display = ('phone', 'status')


class SmsAdmin(admin.ModelAdmin):
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "sms_user":
            kwargs["queryset"] = SmsUser.objects.filter(status=1)
        return super(SmsAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        super(SmsAdmin, self).save_model(request, obj, form, change)
        print('*** Save Objects *** ')
        try:
            sms_active = []
            for user in form.cleaned_data.get('sms_user'):
                sms_active.append(user)
                if not SmsLog.objects.filter(sms__pk=obj.pk).filter(mobile=user).exists():
                    SmsLog.objects.create(
                        sms=obj,
                        mobile=user,
                        sms_user=SmsUser.objects.filter(phone=user).first()
                    )
                print("user: ", str(user))
            print("pk object", str(obj.pk))
            print(str(sms_active))
            if sms_active:
                print("delete old sms phone")
                query = SmsLog.objects.exclude(
                    mobile__in=sms_active).filter(sms__pk=obj.pk).delete()
        except Exception as e:
            print('error when insert data To Sms Log', str(e))


admin.site.register(Sms, SmsAdmin)
admin.site.register(SmsLog)
admin.site.register(SmsUser, SmsUserAdmin)
