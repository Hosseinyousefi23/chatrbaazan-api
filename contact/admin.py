from django.contrib import admin

# Register your models here.
from contact.models import Contact


class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone']


admin.site.register(Contact, ContactAdmin)
