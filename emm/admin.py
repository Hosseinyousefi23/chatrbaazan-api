from django.contrib import admin
from .models import EmailEMM, EmailLog
from django.template.loader import get_template
from django.dispatch import receiver


# Register your models here.

class EmailLogAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        # print(str(obj.user.all().count()))
        if not obj.pk:
            print('*** Save Objects *** ')
            obj.save()
            try:
                for user in form.cleaned_data.get('user'):
                    print('user', str(user))
                    # first_name = instance.user.first_name
                    # print('first name is', first_name)
                    print(str(user))
                    EmailLog.objects.create(
                        user=user,
                        email=get_template('email/emm.html').render(
                            {
                                'user': user,
                                'text': obj.text
                            }
                        )
                    )
            except Exception as e:
                print('error when insert data To Email Log', str(e))
        else:
            super(EmailLogAdmin, self).save_model(request, obj, form, change)


admin.site.register(EmailEMM, EmailLogAdmin)
admin.site.register(EmailLog)
