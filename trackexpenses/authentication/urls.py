from .views import RegistrationView,UsernameValidateView,EmailValidateView,VerificationView, LoginView,LogoutView
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import views as auth_views

urlpatterns=[
 path('register/',RegistrationView.as_view() ,name='register'),
 path('login/',LoginView.as_view() ,name='login'),
 path('logout/',auth_views.LogoutView.as_view() ,name='logout'),
 path('validate-username/',csrf_exempt(UsernameValidateView.as_view()), name='validate-username'),
 path('validate-email/',csrf_exempt(EmailValidateView.as_view()), name='validate-email'),
 path('activate/<uidb64>/<token>',VerificationView.as_view(), name='activate')
 
]