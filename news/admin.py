from django.contrib import admin
from .models import Headline,intrest, CustomUser, newsCategory

# Register your models here.
admin.site.register(CustomUser)


@admin.register(Headline)
class HeadlineAdmin(admin.ModelAdmin):
    list_display = ['title', 'url']
    list_filter = ['news_category']


@admin.register(intrest)
class intrestAdmin(admin.ModelAdmin):
    list_display=['PreferencedNews']


@admin.register(newsCategory)
class newsCategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name']
