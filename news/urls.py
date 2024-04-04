from django.urls import path
from . import views

urlpatterns = [
    path('break/',views.news_list,name='home'),
    path('scrape/', views.scrape, name="scrape"),
    path('',views.index,name='break'),
    path('base/',views.base,name='base'),
    path('register/',views.registerView,name='register'),
    path('login/',views.login,name='login')


]
