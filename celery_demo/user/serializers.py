
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import CustomUser
from django.contrib.auth.hashers import make_password
import logging
logger = logging.getLogger(__name__)

'''
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    otp = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name', 'otp')

    def create(self, validated_data):
        log.debug(validated_data)
        password = validated_data.pop('password')
        otp = validated_data.pop('otp', None)
        user = User(**validated_data)
        user.set_password(password)
        if otp:
            # Code to handle OTP functionality, send and validate OTP
            pass  # You should implement this part based on your OTP mechanism
        user.save()
        return user

 '''   



class UserSerializer(serializers.Serializer):
    userName = serializers.CharField()
    otp = serializers.CharField(required=False)
    email = serializers.EmailField()
    firstName = serializers.CharField()
    lastName = serializers.CharField()
    password = serializers.CharField(write_only=True)
    userType = serializers.CharField()
    profilePicture = serializers.CharField(required=False)

    def create(self, validated_data):
    
        user = CustomUser.objects.create(
            email=validated_data['email'],
            userName=validated_data['userName'],
            firstName=validated_data['firstName'],
            lastName=validated_data['lastName'],
            otp = validated_data['otp'],
            userType = validated_data['userType']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    

class UserPayloadSerializer(serializers.Serializer):
    email = serializers.EmailField()
    userName = serializers.CharField()
    full_name = serializers.CharField()