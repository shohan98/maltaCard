from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import UserProfile, CustomUser
from core.serializers import BaseModelSerializer

class EmailLoginSerializer(serializers.Serializer):
    """Serializer for email-based login requests"""
    email = serializers.EmailField(help_text="Email address")
    password = serializers.CharField(max_length=128, write_only=True, help_text="Password")
    
    def validate_email(self, value):
        """Validate email field"""
        if not value:
            raise serializers.ValidationError("Email is required")
        return value
    
    def validate_password(self, value):
        """Validate password field"""
        if not value:
            raise serializers.ValidationError("Password is required")
        return value
    
    def validate(self, data):
        """Validate login credentials"""
        email = data.get('email')
        password = data.get('password')
        
        if email and password:
            # Try to authenticate with email
            user = authenticate(email=email, password=password)
            if user:
                data['user'] = user
                return data
            else:
                raise serializers.ValidationError("Invalid email or password")
        else:
            raise serializers.ValidationError("Email and password are required")
        
        return data

class LoginSerializer(serializers.Serializer):
    """Serializer for login requests with email support"""
    email = serializers.EmailField(help_text="Email address")
    password = serializers.CharField(max_length=128, write_only=True, help_text="Password")
    
    def validate_email(self, value):
        """Validate email field"""
        if not value:
            raise serializers.ValidationError("Email is required")
        return value
    
    def validate_password(self, value):
        """Validate password field"""
        if not value:
            raise serializers.ValidationError("Password is required")
        return value
    
    def validate(self, data):
        """Validate login credentials"""
        email = data.get('email')
        password = data.get('password')
        
        if email and password:
            # Try to authenticate with email
            user = authenticate(email=email, password=password)
            if user:
                data['user'] = user
                return data
            else:
                raise serializers.ValidationError("Invalid email or password")
        else:
            raise serializers.ValidationError("Email and password are required")
        
        return data

class AuthTokenSerializer(serializers.Serializer):
    """Serializer for token authentication"""
    email = serializers.EmailField(help_text="Email address")
    password = serializers.CharField(max_length=128, write_only=True, help_text="Password")
    
    def validate_email(self, value):
        """Validate email field"""
        if not value:
            raise serializers.ValidationError("Email is required")
        return value
    
    def validate_password(self, value):
        """Validate password field"""
        if not value:
            raise serializers.ValidationError("Password is required")
        return value
    
    def validate(self, data):
        """Validate login credentials"""
        email = data.get('email')
        password = data.get('password')
        
        if email and password:
            # Try to authenticate with email
            user = authenticate(email=email, password=password)
            if user:
                data['user'] = user
                return data
            else:
                raise serializers.ValidationError("Invalid email or password")
        else:
            raise serializers.ValidationError("Email and password are required")
        
        return data

class UserProfileSerializer(BaseModelSerializer):
    """Serializer for UserProfile model"""
    
    class Meta:
        model = UserProfile
        fields = [
            'id', 'phone_number', 'address', 'city', 'state', 
            'postal_code', 'country', 'created_at', 'updated_at'
        ]

class UserSerializer(serializers.ModelSerializer):
    """Serializer for CustomUser model"""
    profile = UserProfileSerializer(read_only=True)
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomUser
        fields = [
            'id', 'email', 'first_name', 'last_name', 
            'date_joined', 'profile', 'password'
        ]
        read_only_fields = ['id', 'date_joined']
    
    def create(self, validated_data):
        profile_data = validated_data.pop('profile', {})
        user = CustomUser.objects.create_user(**validated_data)
        
        # Create or update profile
        UserProfile.objects.update_or_create(
            user=user,
            defaults=profile_data
        )
        
        return user
    
    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        
        # Update user fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update profile
        if hasattr(instance, 'profile'):
            for attr, value in profile_data.items():
                setattr(instance.profile, attr, value)
            instance.profile.save()
        
        return instance

class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True, min_length=8, help_text="Password (minimum 8 characters)")
    password_confirm = serializers.CharField(write_only=True, help_text="Password confirmation")
    phone_number = serializers.CharField(required=False, max_length=20, help_text="Phone number")
    address = serializers.CharField(required=False, max_length=255, help_text="Address")
    city = serializers.CharField(required=False, max_length=100, help_text="City")
    state = serializers.CharField(required=False, max_length=100, help_text="State/Province")
    country = serializers.CharField(required=False, max_length=100, help_text="Country")
    postal_code = serializers.CharField(required=False, max_length=20, help_text="Postal code")
    
    class Meta:
        model = CustomUser
        fields = [
            'email', 'password', 'password_confirm', 
            'first_name', 'last_name', 'phone_number', 'address', 
            'city', 'state', 'country', 'postal_code'
        ]
    
    def validate_email(self, value):
        """Validate email uniqueness"""
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value
    
    def validate_password(self, value):
        """Validate password strength"""
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long")
        return value
    
    def validate(self, data):
        """Validate password confirmation and overall data"""
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return data
    
    def create(self, validated_data):
        """Create user and profile, then generate authentication token"""
        # Extract profile data
        profile_data = {
            'phone_number': validated_data.pop('phone_number', ''),
            'address': validated_data.pop('address', ''),
            'city': validated_data.pop('city', ''),
            'state': validated_data.pop('state', ''),
            'country': validated_data.pop('country', ''),
            'postal_code': validated_data.pop('postal_code', ''),
        }
        
        # Remove password confirmation
        validated_data.pop('password_confirm')
        
        # Create user (profile will be created automatically by signal)
        user = CustomUser.objects.create_user(**validated_data)
        
        # Update the automatically created profile with provided data
        if hasattr(user, 'profile'):
            for key, value in profile_data.items():
                if value:  # Only update if value is not empty
                    setattr(user.profile, key, value)
            user.profile.save()
        
        # Generate authentication token for the new user
        token, created = Token.objects.get_or_create(user=user)
        
        # Store token in the user object for access in the view
        user.auth_token = token
        
        return user 