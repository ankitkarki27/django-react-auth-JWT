from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class CookiesJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):   
        access_token = request.COOKIES.get('access_token')  # Retrieve the token from the cookie
        
        if not access_token:
            return None  # If no token is found, skip authentication
        
        # Validate the token
        validated_token = self.get_validated_token(access_token)
        
        try:
            # Try to get the user from the token
            user = self.get_user(validated_token)
        except AuthenticationFailed:
            return None  # If authentication fails, return None
        
        return (user, validated_token)  # If successful, return user and validated token
