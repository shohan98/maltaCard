from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as filters
from .utils import APIResponse, PaginationHelper

class BaseModelViewSet(viewsets.ModelViewSet):
    """Base ViewSet with common functionality"""
    
    def get_queryset(self):
        """Filter queryset to show only active items"""
        return self.queryset.filter(is_active=True)
    
    def list(self, request, *args, **kwargs):
        """Override list to use standardized response"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            # Use DRF's built-in pagination response
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return APIResponse.success(data=serializer.data)
    
    def create(self, request, *args, **kwargs):
        """Override create to use standardized response"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return APIResponse.created(serializer.data)
        return APIResponse.error(
            message="Validation failed",
            errors=serializer.errors
        )
    
    def retrieve(self, request, *args, **kwargs):
        """Override retrieve to use standardized response"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return APIResponse.success(data=serializer.data)
    
    def update(self, request, *args, **kwargs):
        """Override update to use standardized response"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if serializer.is_valid():
            self.perform_update(serializer)
            return APIResponse.success(data=serializer.data, message="Updated successfully")
        return APIResponse.error(
            message="Validation failed",
            errors=serializer.errors
        )
    
    def destroy(self, request, *args, **kwargs):
        """Override destroy to use standardized response"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return APIResponse.deleted()
