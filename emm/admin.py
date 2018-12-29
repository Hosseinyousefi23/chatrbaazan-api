from django.contrib import admin
from .models import EmailEMM, EmailLog
from django.template.loader import get_template
from django.dispatch import receiver


# Register your models here.

class EmailAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        # print(str(obj.user.all().count()))
        if not obj.pk:
            print('*** Save Objects *** ')
            obj.save()
            try:
                for user in form.cleaned_data.get('user'):
                    EmailLog.objects.create(
                        user=user,
                        body=get_template('email/emm.html').render(),
                        email_address=user.email,
                        title_email=form.cleaned_data.get('title')
                    )
                print('clean data', str(form.cleaned_data.get('email_register')))
                for email in form.cleaned_data.get('email_register'):
                    print('email', str(email))
                    EmailLog.objects.create(
                        body=get_template('email/emm.html').render(),
                        email_address=email,
                        title_email=form.cleaned_data.get('title')
                    )
            except Exception as e:
                print('error when insert data To Email Log', str(e))
        else:
            super(EmailAdmin, self).save_model(request, obj, form, change)


class EmailLogAdmin(admin.ModelAdmin):
    list_display = ('get_email', 'status',)

    def get_email(self, obj):
        return obj.user if obj.user else obj.email_address


admin.site.register(EmailEMM, EmailAdmin)
admin.site.register(EmailLog, EmailLogAdmin)
