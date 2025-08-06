from rest_framework.response import Response
from rest_framework import status
from typing import Any, Dict, List, Optional

class APIResponse:
    """Standardized API response format"""
    
    @staticmethod
    def success(
        data: Any = None,
        message: str = "Success",
        status_code: int = status.HTTP_200_OK,
        pagination: Optional[Dict] = None
    ) -> Response:
        """Success response"""
        response_data = {
            "success": True,
            "message": message,
            "data": data,
        }
        
        if pagination:
            response_data["pagination"] = pagination
            
        return Response(response_data, status=status_code)
    
    @staticmethod
    def error(
        message: str = "Error",
        errors: Optional[List] = None,
        status_code: int = status.HTTP_400_BAD_REQUEST
    ) -> Response:
        """Error response"""
        response_data = {
            "success": False,
            "message": message,
        }
        
        if errors:
            response_data["errors"] = errors
            
        return Response(response_data, status=status_code)
    
    @staticmethod
    def created(
        data: Any = None,
        message: str = "Created successfully"
    ) -> Response:
        """Created response"""
        return APIResponse.success(data, message, status.HTTP_201_CREATED)
    
    @staticmethod
    def deleted(
        message: str = "Deleted successfully"
    ) -> Response:
        """Deleted response"""
        return APIResponse.success(None, message, status.HTTP_204_NO_CONTENT)
    
    @staticmethod
    def not_found(
        message: str = "Resource not found"
    ) -> Response:
        """Not found response"""
        return APIResponse.error(message, status_code=status.HTTP_404_NOT_FOUND)
    
    @staticmethod
    def unauthorized(
        message: str = "Unauthorized"
    ) -> Response:
        """Unauthorized response"""
        return APIResponse.error(message, status_code=status.HTTP_401_UNAUTHORIZED)
    
    @staticmethod
    def forbidden(
        message: str = "Forbidden"
    ) -> Response:
        """Forbidden response"""
        return APIResponse.error(message, status_code=status.HTTP_403_FORBIDDEN)

class PaginationHelper:
    """Helper for pagination metadata"""
    
    @staticmethod
    def get_pagination_data(paginator, page_obj) -> Dict:
        """Get pagination metadata"""
        # For DRF PageNumberPagination, the page_obj is the paginated data
        # and paginator is the paginator instance
        try:
            return {
                "count": paginator.page.paginator.count,
                "total_pages": paginator.page.paginator.num_pages,
                "current_page": paginator.page.number,
                "has_next": paginator.page.has_next(),
                "has_previous": paginator.page.has_previous(),
                "next_page": paginator.page.next_page_number() if paginator.page.has_next() else None,
                "previous_page": paginator.page.previous_page_number() if paginator.page.has_previous() else None,
            }
        except AttributeError:
            # Fallback for different pagination types
            return {
                "count": getattr(paginator, 'count', 0),
                "total_pages": getattr(paginator, 'num_pages', 1),
                "current_page": getattr(page_obj, 'number', 1),
                "has_next": getattr(page_obj, 'has_next', lambda: False)(),
                "has_previous": getattr(page_obj, 'has_previous', lambda: False)(),
                "next_page": None,
                "previous_page": None,
            } 