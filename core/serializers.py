from rest_framework import serializers
from .models import BaseModel
from .utils import APIResponse

class BaseModelSerializer(serializers.ModelSerializer):
    """Base serializer with common functionality"""
    
    class Meta:
        model = BaseModel
        fields = ['id', 'created_at', 'updated_at', 'is_active']
        read_only_fields = ['id', 'created_at', 'updated_at']
