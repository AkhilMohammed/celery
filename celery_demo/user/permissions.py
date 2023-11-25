from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.tokens import Token
import logging
logger = logging.getLogger(__name__)

class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        authToken = request.headers.get('Authorization')
        logger.debug(request.user)
        logger.debug("hhhhhdhhdhd")
        logger.debug(request.user.userType)
        # authToken = authToken.split()[1]
        if request.headers and isinstance(authToken, Token):
            logger.debug("hdhddhhd")
            user_data = request.user
            logger.debug(user_data.userType)
            return user_data.userType == 'admin'
        return False

class RootPermission(BasePermission):
    def has_permission(self, request, view):
        authToken = request.headers.get('Authorization')
        authToken = authToken.split()[1]
        if request.auth and isinstance(authToken, Token):
            user_data = request.user
            return user_data.userType == 'root'
        return False

class SimpleUserPermission(BasePermission):
    def has_permission(self, request, view):
        authToken = request.headers.get('Authorization')
        authToken = authToken.split()[1]
        if request.auth and isinstance(authToken, Token):
            user_data = request.user
            return user_data.userType == 'simple user'
        return False