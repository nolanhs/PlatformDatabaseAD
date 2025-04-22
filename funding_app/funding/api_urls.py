from django.urls import path
from .views import ProtectedView
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('token_test/', ProtectedView.as_view(), name='token_test')
]
