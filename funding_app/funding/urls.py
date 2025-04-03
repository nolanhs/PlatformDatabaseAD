# funding_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),                            # homepage
    path('events/', views.funding_events, name='funding_events'),   # events page
]