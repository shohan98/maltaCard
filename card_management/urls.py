from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .api_views import CardTypeViewSet

router = DefaultRouter()
router.register(r'card-types', CardTypeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('cards/', views.card_list, name='card_list'),
    path('cards/<str:card_id>/order/', views.order_card, name='order_card'),
    path('orders/', views.my_orders, name='my_orders'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('orders/<int:order_id>/cancel/', views.cancel_order, name='cancel_order'),
] 