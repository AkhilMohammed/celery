
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser,UserToken

def invalidate_tokens_for_user(user):
    # Invalidate all tokens for a user by blacklisting them
    tokens = UserToken.objects.filter(user=user,is_active=True)
    for token in tokens:
        token.is_active = False
        token.save()