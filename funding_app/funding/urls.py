from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.funding_event_list, name='event_list'),
    path('event/<int:pk>/', views.funding_event_detail, name='event_detail'),
    path('event/<int:pk>/apply/', views.apply_for_event, name='apply'),
    path('success/', views.funding_event_list, name='application_success'), #placeholder
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
]