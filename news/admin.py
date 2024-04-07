from django.contrib import admin
from .models import Headline, CustomUser

# Register your models here.
admin.site.register(CustomUser)


@admin.register(Headline)
class HeadlineAdmin(admin.ModelAdmin):
    list_display = ['title', 'url']
