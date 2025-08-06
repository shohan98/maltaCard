from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import CardViewSet, CardOrderViewSet, CardTypeViewSet

router = DefaultRouter()
router.register(r'card-types', CardTypeViewSet)
router.register(r'cards', CardViewSet)
router.register(r'orders', CardOrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 