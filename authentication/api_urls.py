from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import UserViewSet, UserProfileViewSet, AuthenticationViewSet, CustomAuthToken

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'profiles', UserProfileViewSet)
router.register(r'auth', AuthenticationViewSet, basename='auth')

urlpatterns = [
    path('', include(router.urls)),
    path('token/', CustomAuthToken.as_view(), name='api_token_auth'),
] 