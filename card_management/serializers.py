from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Card, CardOrder, CardType
from authentication.serializers import UserSerializer
from core.serializers import BaseModelSerializer

class CardTypeSerializer(BaseModelSerializer):
    """Serializer for CardType model"""
    duration_type_display = serializers.CharField(source='get_duration_type_display', read_only=True)
    
    class Meta:
        model = CardType
        fields = [
            'id', 'name', 'description', 'duration_type', 'duration_type_display',
            'price', 'features', 'max_transactions', 'daily_limit', 'monthly_limit',
            'is_popular', 'sort_order', 'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class CardTypeCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating CardType"""
    
    class Meta:
        model = CardType
        fields = [
            'name', 'description', 'duration_type', 'price', 'features',
            'max_transactions', 'daily_limit', 'monthly_limit', 'is_popular', 'sort_order'
        ]

class CardTypeUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating CardType"""
    
    class Meta:
        model = CardType
        fields = [
            'name', 'description', 'duration_type', 'price', 'features',
            'max_transactions', 'daily_limit', 'monthly_limit', 'is_popular', 'sort_order', 'is_active'
        ] 


class CardSerializer(BaseModelSerializer):
    
    class Meta:
        model = Card
        fields = [
            'id', 'name', 'card_type', 
            'description', 'price', 'created_at', 
            'updated_at', 'is_active'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class CardOrderSerializer(BaseModelSerializer):
    """Serializer for CardOrder model"""
    user = UserSerializer(read_only=True)
    card = CardSerializer(read_only=True)
    card_id = serializers.CharField(write_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = CardOrder
        fields = [
            'id', 'user', 'card', 'card_id', 'quantity', 'status', 'status_display',
            'total_amount', 'shipping_address', 'city', 'state', 'postal_code', 
            'country', 'phone_number', 'order_date', 'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['id', 'user', 'total_amount', 'order_date', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        # Set the user from the request
        validated_data['user'] = self.context['request'].user
        
        # Get the card
        card_id = validated_data.pop('card_id')
        card = Card.objects.get(id=card_id)
        validated_data['card'] = card
        
        # Calculate total amount
        validated_data['total_amount'] = card.price * validated_data.get('quantity', 1)
        
        return super().create(validated_data)

class CardOrderCreateSerializer(serializers.ModelSerializer):
    """Simplified serializer for creating orders"""
    card_id = serializers.CharField()
    
    class Meta:
        model = CardOrder
        fields = [
            'card_id', 'quantity', 'shipping_address', 'city', 'state', 
            'postal_code', 'country', 'phone_number'
        ]
    
    def create(self, validated_data):
        card_id = validated_data.pop('card_id')
        card = Card.objects.get(id=card_id)
        
        order = CardOrder.objects.create(
            user=self.context['request'].user,
            card=card,
            **validated_data
        )
        
        return order

class CardOrderUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating orders"""
    class Meta:
        model = CardOrder
        fields = ['status']
        read_only_fields = ['id', 'user', 'card', 'quantity', 'total_amount', 
                           'shipping_address', 'city', 'state', 'postal_code', 
                           'country', 'phone_number', 'order_date', 'created_at', 'updated_at'] 