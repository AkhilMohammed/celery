from rest_framework_simplejwt.tokens import TokenError,RefreshToken
from user.models import UserToken
from rest_framework.response import Response
from rest_framework import status

class TokenBlacklistMiddleware:
    BLACKLISTED_PATHS = ['/user/v1/register/','/user/v1/verifyotp/','/user/v1/login/','/user/v1/gettoken/']
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)  # Create the response variable
        if request.path not in self.BLACKLISTED_PATHS:
            try:
                # Validate the token and check against the blacklist
                authorization_header = request.headers.get('Authorization')
                if authorization_header and authorization_header.startswith('Bearer '):
                    access_token = RefreshToken(authorization_header.split()[1]).access_token
                    if UserToken.objects.filter(token_id=authorization_header.split()[1], is_active=False).exists():
                        raise TokenError('Token is blacklisted')
            except TokenError as e:
                # Handle TokenError as needed (e.g., logout the user)
                response.data = {'detail': str(e)}
                response.status_code = status.HTTP_403_FORBIDDEN

        return response