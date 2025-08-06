from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import FilterSet, CharFilter, DateTimeFromToRangeFilter
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.authtoken.models import Token
from django.contrib.auth import logout
from django.contrib.auth import get_user_model
from social_django.utils import load_strategy, load_backend
from social_core.exceptions import AuthTokenError
from social_core.backends.google import GoogleOAuth2

from .models import UserProfile, CustomUser
from .serializers import (
    UserSerializer, UserProfileSerializer, LoginSerializer, 
    UserRegistrationSerializer, AuthTokenSerializer
)
from core.utils import APIResponse, PaginationHelper

User = get_user_model()

class CustomAuthToken(APIView):
    """Custom token authentication view"""
    permission_classes = [permissions.AllowAny]
    
    @swagger_auto_schema(
        operation_description="Authenticate user and return access token",
        request_body=AuthTokenSerializer,
        responses={
            200: openapi.Response(
                description="Login successful",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'success': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                        'data': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'token': openapi.Schema(type=openapi.TYPE_STRING),
                                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'email': openapi.Schema(type=openapi.TYPE_STRING),
                            }
                        )
                    }
                )
            ),
            401: openapi.Response(description="Invalid credentials")
        },
        tags=['Authentication']
    )
    def post(self, request, *args, **kwargs):
        serializer = AuthTokenSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return APIResponse.success(
                data={
                    'token': token.key,
                    'user_id': user.pk,
                    'email': user.email
                },
                message="Login successful"
            )
        return APIResponse.error(
            message="Invalid credentials",
            errors=serializer.errors,
            status_code=status.HTTP_401_UNAUTHORIZED
        )

class AuthenticationViewSet(viewsets.ViewSet):
    """ViewSet for authentication operations"""
    permission_classes = [permissions.AllowAny]
    
    @swagger_auto_schema(
        operation_description="Login with email and password",
        request_body=LoginSerializer,
        responses={
            200: openapi.Response(
                description="Login successful",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'success': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                        'data': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'token': openapi.Schema(type=openapi.TYPE_STRING),
                                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'email': openapi.Schema(type=openapi.TYPE_STRING),
                                'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                                'last_name': openapi.Schema(type=openapi.TYPE_STRING),
                            }
                        )
                    }
                )
            ),
            401: openapi.Response(description="Invalid credentials"),
            400: openapi.Response(description="Validation failed")
        },
        tags=['Authentication']
    )
    @action(detail=False, methods=['post'])
    def login(self, request):
        """Login with email and password"""
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return APIResponse.success(
                data={
                    'token': token.key,
                    'user_id': user.pk,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                },
                message="Login successful"
            )
        return APIResponse.error(
            message="Invalid credentials",
            errors=serializer.errors,
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    
    @swagger_auto_schema(
        operation_description="Logout user and invalidate token",
        responses={
            200: openapi.Response(
                description="Logout successful",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'success': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                )
            )
        },
        tags=['Authentication'],
        security=[{'Token': []}]
    )
    @action(detail=False, methods=['post'])
    def logout(self, request):
        """Logout user and invalidate token"""
        if request.user.is_authenticated:
            # Delete the token
            Token.objects.filter(user=request.user).delete()
            # Logout the user
            logout(request)
            return APIResponse.success(message="Logout successful")
        return APIResponse.error(
            message="No user to logout",
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    @swagger_auto_schema(
        operation_description="Get Google OAuth authorization URL",
        responses={
            200: openapi.Response(
                description="Google OAuth URL generated",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'success': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                        'data': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'auth_url': openapi.Schema(type=openapi.TYPE_STRING),
                            }
                        )
                    }
                )
            )
        },
        tags=['Authentication']
    )
    @action(detail=False, methods=['get'])
    def google_login_url(self, request):
        """Get Google OAuth authorization URL"""
        try:
            strategy = load_strategy(request)
            backend = load_backend(strategy=strategy, name='google-oauth2', redirect_uri=None)
            auth_url = backend.auth_url()
            return APIResponse.success(
                data={'auth_url': auth_url},
                message="Google OAuth URL generated"
            )
        except Exception as e:
            return APIResponse.error(
                message="Failed to generate Google OAuth URL",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @swagger_auto_schema(
        operation_description="Handle Google OAuth callback and authenticate user",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'access_token': openapi.Schema(type=openapi.TYPE_STRING, description="Google OAuth access token")
            }
        ),
        responses={
            200: openapi.Response(
                description="Google login successful",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'success': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                        'data': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'token': openapi.Schema(type=openapi.TYPE_STRING),
                                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'email': openapi.Schema(type=openapi.TYPE_STRING),
                                'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                                'last_name': openapi.Schema(type=openapi.TYPE_STRING),
                                'is_google_user': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                            }
                        )
                    }
                )
            ),
            400: openapi.Response(description="Google authentication failed"),
            500: openapi.Response(description="Google OAuth error")
        },
        tags=['Authentication']
    )
    @action(detail=False, methods=['post'])
    def google_callback(self, request):
        """Handle Google OAuth callback and authenticate user"""
        access_token = request.data.get('access_token')
        if not access_token:
            return APIResponse.error(
                message="Access token is required",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            strategy = load_strategy(request)
            backend = load_backend(strategy=strategy, name='google-oauth2', redirect_uri=None)
            
            # Get user info from Google
            user_data = backend.user_data(access_token)
            email = user_data.get('email')
            
            if not email:
                return APIResponse.error(
                    message="Email not provided by Google",
                    status_code=status.HTTP_400_BAD_REQUEST
                )
            
            # Try to get existing user or create new one
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'first_name': user_data.get('given_name', ''),
                    'last_name': user_data.get('family_name', ''),
                    'is_active': True
                }
            )
            
            # Generate token
            token, created = Token.objects.get_or_create(user=user)
            
            return APIResponse.success(
                data={
                    'token': token.key,
                    'user_id': user.pk,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'is_google_user': True
                },
                message="Google login successful"
            )
            
        except AuthTokenError:
            return APIResponse.error(
                message="Invalid Google access token",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return APIResponse.error(
                message="Google OAuth error",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UserProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for UserProfile model"""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter queryset based on user permissions"""
        if self.request.user.is_staff:
            return UserProfile.objects.all()
        return UserProfile.objects.filter(user=self.request.user)

class UserFilter(FilterSet):
    """Filter for CustomUser model"""
    email = CharFilter(lookup_expr='icontains')
    first_name = CharFilter(lookup_expr='icontains')
    last_name = CharFilter(lookup_expr='icontains')
    date_joined = DateTimeFromToRangeFilter()
    
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'date_joined', 'is_active']

class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for CustomUser model"""
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    filterset_class = UserFilter
    search_fields = ['email', 'first_name', 'last_name']
    ordering_fields = ['email', 'date_joined', 'last_name']
    ordering = ['email']
    
    def get_permissions(self):
        """Set permissions based on action"""
        if self.action in ['create', 'register']:
            permission_classes = [permissions.AllowAny]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """Filter queryset based on user permissions"""
        if self.request.user.is_staff:
            return CustomUser.objects.all()
        return CustomUser.objects.filter(id=self.request.user.id)
    
    def list(self, request, *args, **kwargs):
        """Override list to use standardized response"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return APIResponse.success(data=serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        """Override retrieve to use standardized response"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return APIResponse.success(data=serializer.data)
    
    def create(self, request, *args, **kwargs):
        """Override create to use standardized response"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return APIResponse.created(
                data=serializer.data,
                message="User created successfully"
            )
        return APIResponse.error(
            message="Failed to create user",
            errors=serializer.errors
        )
    
    def update(self, request, *args, **kwargs):
        """Override update to use standardized response"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            user = serializer.save()
            return APIResponse.success(
                data=serializer.data,
                message="User updated successfully"
            )
        return APIResponse.error(
            message="Failed to update user",
            errors=serializer.errors
        )
    
    def destroy(self, request, *args, **kwargs):
        """Override destroy to use standardized response"""
        instance = self.get_object()
        instance.delete()
        return APIResponse.success(message="User deleted successfully")
    
    @swagger_auto_schema(
        operation_description="Get current authenticated user information",
        responses={
            200: openapi.Response(
                description="Current user information",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'success': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                        'data': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'email': openapi.Schema(type=openapi.TYPE_STRING),
                                'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                                'last_name': openapi.Schema(type=openapi.TYPE_STRING),
                                'date_joined': openapi.Schema(type=openapi.TYPE_STRING),
                                'profile': openapi.Schema(type=openapi.TYPE_OBJECT),
                            }
                        )
                    }
                )
            )
        },
        tags=['Users'],
        security=[{'Token': []}]
    )
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current authenticated user information"""
        serializer = self.get_serializer(request.user)
        return APIResponse.success(data=serializer.data)
    
    @swagger_auto_schema(
        operation_description="Register a new user with profile information and return authentication token",
        request_body=UserRegistrationSerializer,
        responses={
            201: openapi.Response(
                description="User registered successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'success': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                        'data': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'token': openapi.Schema(type=openapi.TYPE_STRING),
                                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'email': openapi.Schema(type=openapi.TYPE_STRING),
                                'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                                'last_name': openapi.Schema(type=openapi.TYPE_STRING),
                                'profile_created': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                            }
                        )
                    }
                )
            ),
            400: openapi.Response(description="Validation failed"),
            409: openapi.Response(description="Email already exists")
        },
        tags=['Users']
    )
    @action(detail=False, methods=['post'])
    def register(self, request):
        """Register a new user and return authentication token"""
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return APIResponse.created(
                data={
                    'token': user.auth_token.key,
                    'user_id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'profile_created': hasattr(user, 'profile')
                },
                message="User registered successfully"
            )
        return APIResponse.error(
            message="Registration failed",
            errors=serializer.errors
        ) 