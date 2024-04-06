from django.urls import path
from . import views

urlpatterns = [
    path('break/',views.news_list,name='home'),
    path('scrape/', views.scrape, name="scrape"),
    path('',views.index,name='break'),
    path('base/',views.base,name='base'),
    path('register/',views.user_register,name='user_register'),
    path('login/',views.login,name='login'),
    path('userprofile/',views.userp,name='userprofile'),
    path('save_preference/', views.save_preference, name='save_preference'),
]
