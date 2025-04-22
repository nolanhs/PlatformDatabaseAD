from django.urls import path
from .views import ProtectedView
from rest_framework.routers import DefaultRouter
from .views import (
    FundingEventViewSet,
    CategorizationViewSet,
    ApplicationViewSet,
    ProfileViewSet,
    UserViewSet,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'fundingevents', FundingEventViewSet)
router.register(r'categorizations', CategorizationViewSet)
router.register(r'applications', ApplicationViewSet)
router.register(r'profiles', ProfileViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('token_test/', ProtectedView.as_view(), name='token_test'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += router.urls