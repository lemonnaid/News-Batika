from django.urls import path
from . import views

urlpatterns = [
    path('scrape/', views.scrape, name="scrape"),
    path('',views.index,name='home'),
    path('register/',views.user_register,name='user_register'),
    path('login/',views.login,name='login'),
    path('userprofile/',views.userp,name='userprofile'),
    # path('save_preference/', views.save_preference, name='save_preference'),
]
