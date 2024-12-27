from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Note
from .serializers import NoteSearilizer,UserRegistrationSerializer,UserSerializer

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from rest_framework_simplejwt.views import (  # type: ignore
    TokenObtainPairView,
    TokenRefreshView,
)

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        try:
            # Call the parent class's post method
            response = super().post(request, *args, **kwargs)
            tokens = response.data

            access_token = tokens['access']
            refresh_token = tokens['refresh']

            # Create a new response object to modify cookies
            res = Response({'success': True})

            # Set the cookies for tokens
            res.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=True,  # Set to False in development if HTTPS is not used
                samesite='None',  # Use 'Lax' or 'Strict' if appropriate
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
            # Log or debug the error if needed
            return Response({'success': False, 'error': str(e)}, status=400)




class CustomRefreshTokenView(TokenRefreshView):
    def post(self,request,*args, **kwargs):
        try:
            refresh_token=request.COOKIES.get('refresh_token')
            
            request.data['refresh']=refresh_token
            
            response=super().post(request,*args, **kwargs)
            
            tokens=response.data
            access_token=tokens['access']
            
            res=Response()
            
            res.data={'refreshed':True}
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
            return Response({'refreshed':False})


@api_view(['POST'])
def logout(request):
    try:
        res=Response()
        res.data={'success':True}
        res.delete_cookie('access_token',path='/',samesite='None')
        res.delete_cookie('refresh_token',path='/',samesite='None')
        return res
        
    except:
        return Response({'success':False})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def is_authenticated(request):
    return Response({'authenticated':True})

@api_view(['POST'])
@permission_classes([AllowAny])
# user should not be authenticated so allow any to register
def register(request):
    serializer=UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response (serializer.data)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Only authenticated users can access


def get_notes(request):
    """
    Retrieves the notes for the authenticated user.
    Only accessible by authenticated users with valid JWT cookies.
    """
    user = request.user
    notes = Note.objects.filter(owner=user)  # Get notes owned by the authenticated user
    serializer = NoteSearilizer(notes, many=True)  # Serialize the notes data
    return Response(serializer.data)  # Return the serialized data
