from django.urls import path
from .views import RegistrationView, LoginView, OtpView,HomeView,PurchaseView,ContactView,AboutView,FarmersView,product_details_view


urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('', LoginView.as_view(), name='login'),
    path('otp_validation/', OtpView.as_view(), name='otp_validation'),
    path('home/', HomeView.as_view(), name='home'),
    path('purchase/', PurchaseView.as_view(), name = 'purchase'),
    path('farmers/', FarmersView.as_view(), name = 'farmers'),
    path('contact/', ContactView.as_view(), name= 'contact'),
    path('about/', AboutView.as_view(), name= 'about'),
    path('product/<int:product_id>/', product_details_view, name= 'product_details')
]