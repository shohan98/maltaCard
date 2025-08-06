from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as filters
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Card, CardOrder, CardType
from .serializers import (
    CardSerializer, CardOrderSerializer, 
    CardOrderCreateSerializer, CardOrderUpdateSerializer,
    CardTypeSerializer, CardTypeCreateSerializer, CardTypeUpdateSerializer
)
from core.viewsets import BaseModelViewSet
from core.utils import APIResponse, PaginationHelper


class CardTypeFilter(filters.FilterSet):
    """Filter for CardType model"""
    name = filters.CharFilter(lookup_expr='icontains')
    description = filters.CharFilter(lookup_expr='icontains')
    duration_type = filters.CharFilter()
    price_min = filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = filters.NumberFilter(field_name='price', lookup_expr='lte')
    is_popular = filters.BooleanFilter()
    created_at = filters.DateTimeFromToRangeFilter()
    
    class Meta:
        model = CardType
        fields = ['duration_type', 'is_popular', 'price', 'created_at']

class CardTypeViewSet(BaseModelViewSet):
    """ViewSet for CardType model"""
    queryset = CardType.objects.all()
    serializer_class = CardTypeSerializer
    filterset_class = CardTypeFilter
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price', 'sort_order', 'created_at']
    ordering = ['sort_order', 'name']
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        """Use different serializers based on action"""
        if self.action == 'create':
            return CardTypeCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return CardTypeUpdateSerializer
        return CardTypeSerializer
    
    def list(self, request, *args, **kwargs):
        """Override list to use standardized response with security"""
        return super().list(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        """Override create to use standardized response with security"""
        return super().create(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        """Override retrieve to use standardized response with security"""
        return super().retrieve(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        """Override update to use standardized response with security"""
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """Override destroy to use standardized response with security"""
        return super().destroy(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Get popular card types",
        tags=['Card Types'],
        security=[{'Token': []}]
    )
    @action(detail=False, methods=['get'])
    def popular(self, request):
        """Get popular card types"""
        card_types = self.get_queryset().filter(is_popular=True)
        serializer = self.get_serializer(card_types, many=True)
        return APIResponse.success(data=serializer.data, message="Popular card types")
    
    @swagger_auto_schema(
        operation_description="Get card types by duration",
        tags=['Card Types'],
        security=[{'Token': []}]
    )
    @action(detail=False, methods=['get'])
    def by_duration(self, request):
        """Get card types by duration"""
        duration = request.query_params.get('duration', 'monthly')
        card_types = self.get_queryset().filter(duration_type=duration)
        serializer = self.get_serializer(card_types, many=True)
        return APIResponse.success(
            data=serializer.data, 
            message=f"Card types for {duration} duration"
        )
    
    @swagger_auto_schema(
        operation_description="Get card types by price range",
        tags=['Card Types'],
        security=[{'Token': []}]
    )
    @action(detail=False, methods=['get'])
    def price_range(self, request):
        """Get card types by price range"""
        min_price = request.query_params.get('min_price')
        max_price = request.query_params.get('max_price')
        
        queryset = self.get_queryset()
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        serializer = self.get_serializer(queryset, many=True)
        return APIResponse.success(
            data=serializer.data,
            message="Card types in price range"
        )
    
    @swagger_auto_schema(
        operation_description="Toggle popular status of a card type",
        tags=['Card Types'],
        security=[{'Token': []}]
    )
    @action(detail=True, methods=['post'])
    def toggle_popular(self, request, pk=None):
        """Toggle popular status"""
        card_type = self.get_object()
        card_type.is_popular = not card_type.is_popular
        card_type.save()
        
        message = "Marked as popular" if card_type.is_popular else "Removed from popular"
        return APIResponse.success(
            data=self.get_serializer(card_type).data,
            message=message
        ) 
    

class CardFilter(filters.FilterSet):
    """Filter for Card model"""
    name = filters.CharFilter(lookup_expr='icontains')
    description = filters.CharFilter(lookup_expr='icontains')
    card_type = filters.CharFilter()
    price_min = filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = filters.NumberFilter(field_name='price', lookup_expr='lte')
    created_at = filters.DateTimeFromToRangeFilter()
    
    class Meta:
        model = Card
        fields = ['card_type', 'is_active', 'price', 'created_at']

class CardViewSet(BaseModelViewSet):
    """ViewSet for Card model"""
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    filterset_class = CardFilter
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price', 'created_at']
    ordering = ['name']
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter queryset based on user permissions"""
        if self.request.user.is_staff:
            return Card.objects.all()
        return Card.objects.filter(is_active=True)
    
    @swagger_auto_schema(
        operation_description="List all cards",
        tags=['Cards'],
        security=[{'Token': []}]
    )
    def list(self, request, *args, **kwargs):
        """Override list to use standardized response with security"""
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Create a new card",
        tags=['Cards'],
        security=[{'Token': []}]
    )
    def create(self, request, *args, **kwargs):
        """Override create to use standardized response with security"""
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Retrieve a specific card",
        tags=['Cards'],
        security=[{'Token': []}]
    )
    def retrieve(self, request, *args, **kwargs):
        """Override retrieve to use standardized response with security"""
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Update a card",
        tags=['Cards'],
        security=[{'Token': []}]
    )
    def update(self, request, *args, **kwargs):
        """Override update to use standardized response with security"""
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Delete a card",
        tags=['Cards'],
        security=[{'Token': []}]
    )
    def destroy(self, request, *args, **kwargs):
        """Override destroy to use standardized response with security"""
        return super().destroy(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Get cards by type",
        tags=['Cards'],
        security=[{'Token': []}]
    )
    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """Get cards by type"""
        card_type = request.query_params.get('type', 'virtual')
        cards = self.get_queryset().filter(card_type=card_type)
        serializer = self.get_serializer(cards, many=True)
        return APIResponse.success(
            data=serializer.data, 
            message=f"{card_type.title()} cards"
        )
    
    @swagger_auto_schema(
        operation_description="Get cards by price range",
        tags=['Cards'],
        security=[{'Token': []}]
    )
    @action(detail=False, methods=['get'])
    def by_price_range(self, request):
        """Get cards by price range"""
        min_price = request.query_params.get('min_price')
        max_price = request.query_params.get('max_price')
        
        queryset = self.get_queryset()
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        serializer = self.get_serializer(queryset, many=True)
        return APIResponse.success(
            data=serializer.data,
            message="Cards in price range"
        )
    
    
class CardOrderFilter(filters.FilterSet):
    """Filter for CardOrder model"""
    user = filters.NumberFilter()
    card = filters.NumberFilter()
    status = filters.CharFilter()
    total_amount_min = filters.NumberFilter(field_name='total_amount', lookup_expr='gte')
    total_amount_max = filters.NumberFilter(field_name='total_amount', lookup_expr='lte')
    order_date = filters.DateTimeFromToRangeFilter()
    city = filters.CharFilter(lookup_expr='icontains')
    country = filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = CardOrder
        fields = ['user', 'card', 'status', 'total_amount', 'order_date', 'city', 'country']

class CardOrderViewSet(BaseModelViewSet):
    """ViewSet for CardOrder model"""
    queryset = CardOrder.objects.all()
    serializer_class = CardOrderSerializer
    filterset_class = CardOrderFilter
    search_fields = ['user__email', 'card__name', 'city', 'country']
    ordering_fields = ['order_date', 'total_amount', 'status', 'user__email']
    ordering = ['-order_date']
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter queryset based on user permissions"""
        if self.request.user.is_staff:
            return CardOrder.objects.select_related('user', 'card')
        return CardOrder.objects.filter(user=self.request.user).select_related('user', 'card')
    
    def get_serializer_class(self):
        """Use different serializers based on action"""
        if self.action == 'create':
            return CardOrderCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return CardOrderUpdateSerializer
        return CardOrderSerializer
    
    @swagger_auto_schema(
        operation_description="List all card orders",
        tags=['Card Orders'],
        security=[{'Token': []}]
    )
    def list(self, request, *args, **kwargs):
        """Override list to use standardized response with security"""
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Create a new card order",
        tags=['Card Orders'],
        security=[{'Token': []}]
    )
    def create(self, request, *args, **kwargs):
        """Override create to use standardized response with security"""
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Retrieve a specific card order",
        tags=['Card Orders'],
        security=[{'Token': []}]
    )
    def retrieve(self, request, *args, **kwargs):
        """Override retrieve to use standardized response with security"""
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Update a card order",
        tags=['Card Orders'],
        security=[{'Token': []}]
    )
    def update(self, request, *args, **kwargs):
        """Override update to use standardized response with security"""
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Delete a card order",
        tags=['Card Orders'],
        security=[{'Token': []}]
    )
    def destroy(self, request, *args, **kwargs):
        """Override destroy to use standardized response with security"""
        return super().destroy(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Get current user's orders",
        tags=['Card Orders'],
        security=[{'Token': []}]
    )
    @action(detail=False, methods=['get'])
    def my_orders(self, request):
        """Get current user's orders"""
        orders = self.get_queryset().filter(user=request.user)
        serializer = self.get_serializer(orders, many=True)
        return APIResponse.success(data=serializer.data, message="User orders")
    
    @swagger_auto_schema(
        operation_description="Get pending orders",
        tags=['Card Orders'],
        security=[{'Token': []}]
    )
    @action(detail=False, methods=['get'])
    def pending_orders(self, request):
        """Get pending orders"""
        orders = self.get_queryset().filter(status='pending')
        serializer = self.get_serializer(orders, many=True)
        return APIResponse.success(data=serializer.data, message="Pending orders")
    
    @swagger_auto_schema(
        operation_description="Cancel an order",
        tags=['Card Orders'],
        security=[{'Token': []}]
    )
    @action(detail=True, methods=['post'])
    def cancel_order(self, request, pk=None):
        """Cancel an order"""
        order = self.get_object()
        
        if order.status in ['shipped', 'delivered']:
            return APIResponse.error(
                message="Cannot cancel order that has been shipped or delivered",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        order.status = 'cancelled'
        order.save()
        
        return APIResponse.success(
            data=self.get_serializer(order).data,
            message="Order cancelled successfully"
        )
    
    @swagger_auto_schema(
        operation_description="Update order status",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'status': openapi.Schema(type=openapi.TYPE_STRING, description="New status")
            }
        ),
        tags=['Card Orders'],
        security=[{'Token': []}]
    )
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """Update order status"""
        order = self.get_object()
        new_status = request.data.get('status')
        
        if not new_status:
            return APIResponse.error(
                message="Status is required",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        valid_statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
        if new_status not in valid_statuses:
            return APIResponse.error(
                message=f"Invalid status. Must be one of: {', '.join(valid_statuses)}",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        order.status = new_status
        order.save()
        
        return APIResponse.success(
            data=self.get_serializer(order).data,
            message=f"Order status updated to {new_status}"
        ) 