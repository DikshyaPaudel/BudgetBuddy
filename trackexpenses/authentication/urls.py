from .views import (
    RegistrationAPIView, 
    UsernameValidateAPIView, 
    EmailValidateAPIView, 
    VerificationAPIView, 
    LoginAPIView, 
    LogoutAPIView
)
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('register/', RegistrationAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    
    path('validate-username/', csrf_exempt(UsernameValidateAPIView.as_view()), name='validate-username'),
    path('validate-email/', csrf_exempt(EmailValidateAPIView.as_view()), name='validate-email'),
    
    path('activate/<uidb64>/<token>/', VerificationAPIView.as_view(), name='activate'),
]
