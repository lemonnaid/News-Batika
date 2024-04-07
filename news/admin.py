from django.contrib import admin

from .models import CustomUser
from .models import Headline

# Register your models here.
admin.site.register(CustomUser)


@admin.register(Headline)
class HeadlineAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "url", "news_source"]
