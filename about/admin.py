from django.contrib import admin

# Register your models here.
from about.models import About


class AboutAdmin(admin.ModelAdmin):
    pass


admin.site.register(About, AboutAdmin)
