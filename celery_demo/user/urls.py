from django.urls import path
from .views import RegisterAPI,verifyOTP,gettokens,LoginAPi,UserDetails


urlpatterns = [
    path('v1/register/',RegisterAPI.as_view(),name='register'),
    path('v1/verifyotp/',verifyOTP.as_view(),name='verifyotp'),
    path('v1/gettoken/', gettokens.as_view(), name= 'gettokens'),
    path('v1/login/', LoginAPi.as_view(), name='loginapi'),
    path('v1/UserDetails/', UserDetails.as_view(), name='userdetail')
]