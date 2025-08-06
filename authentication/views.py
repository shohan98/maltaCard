from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login
from social_django.models import UserSocialAuth
from rest_framework.authtoken.models import Token
from .models import UserProfile
import json

def register(request):
    """User registration view"""
    if request.method == 'POST':
        # Handle registration logic
        pass
    return render(request, 'authentication/register.html')

@login_required
def dashboard(request):
    """Dashboard view"""
    return render(request, 'authentication/dashboard.html')

@login_required
def profile(request):
    """User profile view"""
    return render(request, 'authentication/profile.html')

def google_oauth_callback(request):
    """Handle Google OAuth callback and return token"""
    if request.user.is_authenticated:
        # User is authenticated via Google OAuth
        try:
            # Get or create token
            token, created = Token.objects.get_or_create(user=request.user)
            
            # Ensure user has a profile
            if not hasattr(request.user, 'profile'):
                UserProfile.objects.create(user=request.user)
            
            # Return token as JSON response
            return JsonResponse({
                'success': True,
                'token': token.key,
                'user_id': request.user.pk,
                'username': request.user.username,
                'email': request.user.email,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'is_google_user': True
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    else:
        return JsonResponse({
            'success': False,
            'error': 'User not authenticated'
        }, status=401)

@csrf_exempt
def google_oauth_token(request):
    """Handle Google OAuth token exchange"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            access_token = data.get('access_token')
            
            if not access_token:
                return JsonResponse({
                    'success': False,
                    'error': 'Access token required'
                }, status=400)
            
            # Here you would validate the access token with Google
            # and create/authenticate the user
            # This is a simplified version - you'd need to implement
            # proper Google token validation
            
            return JsonResponse({
                'success': True,
                'message': 'Token received, implement validation'
            })
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'Invalid JSON'
            }, status=400)
    
    return JsonResponse({
        'success': False,
        'error': 'Method not allowed'
    }, status=405)
