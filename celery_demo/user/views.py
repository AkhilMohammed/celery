from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser,UserToken
from random import randint
from .serializers import *
from random import randint
import logging
logger = logging.getLogger(__name__)
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from .utils import invalidate_tokens_for_user
from .permissions import *
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.conf import settings



class RegisterAPI(APIView):
    def post(self,request):
        try:
            try:
                logger.debug("hdjdhdh")
                logger.debug(request.data)
                userAvailable = CustomUser.objects.get(email=request.data['email'])
                logger.debug("fyffyfy")
                logger.debug("userAvailable")
                logger.debug(userAvailable)
                if userAvailable:
                    if userAvailable.is_active:
                        return Response({"message":"User is available"},status=status.HTTP_400_BAD_REQUEST)
                    elif not userAvailable.is_active and userAvailable.expiry_time < timezone.now():
                        userAvailable.otp = randint(1000,9999)
                        userAvailable.expiry_time = timezone.now()+timedelta(minutes=5)
                        userAvailable.save()
                        logger.debug("its got 1")
                        return Response({"message":"Please verify with New OTP"},status=status.HTTP_400_BAD_REQUEST)
                    else:
                        logger.debug("its got 2")
                        return Response({"message":"Please Verify with Current Otp"},status=status.HTTP_400_BAD_REQUEST)
            except :
                logger.debug("its here")
                username = request.data['userName']
                password = request.data['password']
                email = request.data['email']
                firstName = request.data['firstName']
                lastName = request.data['lastName']
                otp = randint(1000,9999)
                userType = request.data['userType']

                # logger.debug(username,password,email,firstName,lastName)

                data = {
                         'userName': username,
                         'password': password,
                         'firstName' : firstName,
                         'email' : email,
                         'lastName' : lastName,
                         'otp' : otp,
                         'userType' : userType
                }
                logger.debug(data)
                serializer = UserSerializer(data = data)
                if serializer.is_valid():
                    serializer.save()
                    try:
                        subject = "Welcome Here is your OTP For Registration"
                        message = str(data['otp'])
                        # message = 'your activation pin is' + str(ot)
                        to = [data['email']]
                        msg = EmailMessage(subject, message, to=to,
                                           from_email=settings.EMAIL_HOST_USER)
                        msg.send()
                    except Exception as e:
                        logger.debug("its there 3")
                        return Response({"data": str(e),
                                         "message": "Unable To Register",
                                         "requestStatus": 1},
                                        status=status.HTTP_400_BAD_REQUEST)
                    return Response ({"message":"User stored"}, status=status.HTTP_201_CREATED)
                else:
                    logger.debug("its there i 4")
                    return Response({"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.debug(str(e))
            logger.debug("its there i 5")
            return Response ({"message":str(e)}, status=status.HTTP_400_BAD_REQUEST)


class verifyOTP(APIView):
    def post(self,request):
        try:
            email = request.data['email']
            otp = request.data['otp']
            user = CustomUser.objects.get(email=email)
            logger.debug(user.otp)
            logger.debug(email)
            if user.expiry_time < timezone.now():
                user.otp = randint(1000,9999)
                user.expiry_time = timezone.now()+timezone.timedelta(minutes=5)
                user.save()
                return Response({"message":"Please verify with New OTP"},status=status.HTTP_400_BAD_REQUEST)
            elif int(otp) == user.otp:
                user.is_active = True
                user.save()
                refresh = RefreshToken.for_user(user)
                usertoken = UserToken(user = user,token_id=refresh.access_token,is_active=True)
                usertoken.save()
                return Response({
                                    'refresh': str(refresh),
                                    'access': str(refresh.access_token),
                                }, status=status.HTTP_200_OK)
            else:
                return Response({"message":"Invalid OTP"},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message":str(e)},status=status.HTTP_400_BAD_REQUEST)


class gettokens(APIView):
    def get(self,request):
     
            email = request.data['email']
            user = CustomUser.objects.get(email=email)
            refresh_tokens = RefreshToken.for_user(user)
            if refresh_tokens:
                    logger.debug("hfjda")
                    logger.debug(refresh_tokens)
                    for token in refresh_tokens.payload['tokens']:
                        logger.debug(token.access_token)
                        return Response({"message":"Sucess"},status=status.HTTP_200_OK)
            else:
                logger.debug("fjfj")


class LoginAPi(APIView):
    def post(self,request):

            email = request.data['email']
            password = request.data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                if not user.is_active:
                    return Response({"message":"please verify your otp"}, status=status.HTTP_400_BAD_REQUEST)
                invalidate_tokens_for_user(user)
                refresh = RefreshToken.for_user(user)
                logger.debug("jhuyu")
                payload_data = {
                        'email' : user.email,
                        'userName' : user.userName,
                        'full_name' : user.firstName+user.lastName
                }
                refresh.payload.update(payload_data)

                return Response({'data':{'refresh':str(refresh),'access':str(refresh.access_token),\
                    'user_data':UserPayloadSerializer(payload_data).data}},status=status.HTTP_200_OK)
            return Response({"message":"Invalid credentials"},status=status.HTTP_400_BAD_REQUEST)
        


class UserDetails(APIView):
    permission_classes = [AdminPermission]
    def get(self,request):
        try:
            logger.debug("*****")
            user = request.user
            logger.debug(request.user.firstName)
            logger.debug("*****")
            authorization_header = request.headers.get('Authorization')
            logger.debug('jdjdjdjdj')

            if authorization_header and authorization_header.startswith('Bearer '):
                logger.debug("kjid  ")
                logger.debug(authorization_header.split()[1])
                token = AccessToken(authorization_header.split()[1])
                logger.debug("kklkkk")

                # Access the payload from the authentication token
                payload = {
                    'email': token.payload.get('email'),
                    'username': token.payload.get('username'),
                    'full_name': token.payload.get('full_name'),
                }

                return Response({
                    'message': 'Token is valid',
                    'user_data': payload,
                },status=status.HTTP_200_OK)
            else:
                return Response({"message":"Invalid token"},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message":str(e)},status=status.HTTP_400_BAD_REQUEST)
