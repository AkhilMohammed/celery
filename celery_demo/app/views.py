from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.http import JsonResponse
import requests  # Import the requests library for making API requests
from .forms import *
from user.models import CustomUser
import logging
logger = logging.getLogger(__name__)


class RegistrationView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Assuming your API endpoint is '/api/register/'
            api_url = request.build_absolute_uri('/user/v1/register/')
            data = {
                'userName': form.cleaned_data['userName'],
                'password': form.cleaned_data['password'],
                'email' : form.cleaned_data['email'],
                
                'firstName' : form.cleaned_data['firstName'],
                'lastName' : form.cleaned_data['lastName'],
                'userType' : form.cleaned_data['userType']
                # Add other fields as needed
            }

            # Make a POST request to the registration API endpoint
            response = requests.post(api_url, data=data)

            if response.status_code == 201:  # Assuming the API returns a 201 status on success
                messages.success(request, 'Registration successful')
                request.session['registration_email'] = form.cleaned_data['email']
                return redirect('otp_validation')
            else:
                error_message = response.json().get('detail', 'Registration failed')
                messages.error(request, error_message)
        return render(request, 'register.html', {'form': form, 'error': 'Invalid form'})


class OtpView(View):
    def get(self, request):
        form = otpForm()
        return render(request, 'otp.html', {'form': form})

    def post(self, request):
        form = otpForm(request.POST)
        if form.is_valid():
            api_url = request.build_absolute_uri('/user/v1/verifyotp/')
            email = request.session.get('registration_email')
            data = {
                'email': email,  # Assuming you have a user object in the request
                'otp': form.cleaned_data['otp'],
            }
            logger.debug('here 63')

            # Make a POST request to the OTP verification API endpoint
            response = requests.post(api_url, data=data)

            if response.status_code == 200:  # Assuming the API returns a 200 status on successful OTP verification
                # Store the JWT in a cookie
                logger.debug("here 67")
                logger.debug(response.json())
                jwt_token = response.json().get('access')
                if jwt_token:
                    response = redirect('home')  # Adjust the redirect URL as needed
                    response.set_cookie('jwt_token', jwt_token)
                    return response
                else:
                    messages.error(request, 'Failed to get JWT token from the API')
            else:
                error_message = response.json().get('detail', 'OTP validation failed')
                messages.error(request, error_message)
        return render(request, 'otp.html', {'form': form, 'error': 'Invalid OTP'})



class LoginView(View):
    def get(self, request):
        form = loginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = loginForm(request.POST)
        if form.is_valid():
            api_url = request.build_absolute_uri('/user/v1/login/')
            data = {    
                'email': form.cleaned_data['email'],  # Assuming you have a user object in the request
                'password': form.cleaned_data['password'],
            }

            # Make a POST request to the OTP verification API endpoint
            response = requests.post(api_url, data=data)
            logger.debug("came 95")

            if response.status_code == 200:  # Assuming the API returns a 200 status on successful OTP verification
                # Store the JWT in a cookie
                logger.debug('came 99')
                logger.debug(response.json()['data'].get('access'))
                try:
                    jwt_token = response.json()['data'].get('access')
                except Exception as e:
                    logger.debug(str(e))
                if jwt_token:
                    logger.debug('came 102')
                    response = redirect('home')  # Adjust the redirect URL as needed
                    response.set_cookie('jwt_token', jwt_token)
                    return response
                else:
                    logger.debug("came 112")
                    messages.error(request, 'Failed to get JWT token from the API')
            else:
                logger.debug("came 115")
                error_message = response.json().get('detail', 'login validation failed')
                messages.error(request, error_message)
        logger.debug('came 118')
        return render(request, 'login.html', {'form': form, 'error': 'Invalid Creds'})


class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')


class PurchaseView(View):
    def get(self, request):
        return render(request, 'purchase.html')


class AboutView(View):
    def get(self, request):
        return render(request, 'about.html')

class ContactView(View):
    def get(self, request):
        return render(request, 'contact.html')

class FarmersView(View):
    def get(self, request):
        return  render(request, 'farmers.html')


