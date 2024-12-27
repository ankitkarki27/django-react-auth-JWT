from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Note
from .serializers import NoteSearilizer, UserRegistrationSerializer, UserSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# 1. IMPORT NECESSARY MODULES
# - Import all required Django modules, models, serializers, permissions, etc.


# 2. CUSTOM JWT TOKEN VIEW
class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom view to handle token generation and store tokens in cookies.
    """
    def post(self, request, *args, **kwargs):
        try:
            # 2.1 Generate tokens using parent method
            response = super().post(request, *args, **kwargs)
            tokens = response.data

            # 2.2 Extract tokens
            access_token = tokens['access']
            refresh_token = tokens['refresh']

            # 2.3 Set tokens in HTTP-only cookies
            res = Response({'success': True})
            res.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=True,
                samesite='None',
                path='/',
            )
            res.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                secure=True,
                samesite='None',
                path='/',
            )
            return res

        except Exception as e:
            # 2.4 Handle token generation errors
            return Response({'success': False, 'error': str(e)}, status=400)


# 3. CUSTOM TOKEN REFRESH VIEW
class CustomRefreshTokenView(TokenRefreshView):
    """
    Custom view to refresh JWT access token using the refresh token from cookies.
    """
    def post(self, request, *args, **kwargs):
        try:
            # 3.1 Retrieve refresh token from cookies
            refresh_token = request.COOKIES.get('refresh_token')
            request.data['refresh'] = refresh_token

            # 3.2 Call parent method to refresh access token
            response = super().post(request, *args, **kwargs)
            tokens = response.data
            access_token = tokens['access']

            # 3.3 Update access token in cookies
            res = Response()
            res.data = {'refreshed': True}
            res.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=True,
                samesite='None',
                path='/'
            )
            return res

        except:
            # 3.4 Handle token refresh errors
            return Response({'refreshed': False})


# 4. LOGOUT VIEW
@api_view(['POST'])
def logout(request):
    """
    Logout user by deleting access and refresh token cookies.
    """
    try:
        # 4.1 Clear token cookies
        res = Response()
        res.data = {'success': True}
        res.delete_cookie('access_token', path='/', samesite='None')
        res.delete_cookie('refresh_token', path='/', samesite='None')
        return res

    except:
        # 4.2 Handle logout errors
        return Response({'success': False})


# 5. AUTHENTICATION STATUS CHECK VIEW
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def is_authenticated(request):
    """
    Check if the user is authenticated using tokens.
    """
    return Response({'authenticated': True})


# 6. USER REGISTRATION VIEW
@api_view(['POST'])
@permission_classes([AllowAny])  # Allow anyone to access this view
def register(request):
    """
    Register a new user with validated input data.
    """
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        # 6.1 Save user if data is valid
        serializer.save()
        return Response(serializer.data)
    # 6.2 Return errors if validation fails
    return Response(serializer.errors)


# 7. GET NOTES VIEW
@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Only authenticated users can access
def get_notes(request):
    """
    Retrieve notes associated with the authenticated user.
    """
    user = request.user  # 7.1 Get the authenticated user
    notes = Note.objects.filter(owner=user)  # 7.2 Query notes owned by the user
    serializer = NoteSearilizer(notes, many=True)  # 7.3 Serialize the notes
    return Response(serializer.data)  # 7.4 Return the serialized data
