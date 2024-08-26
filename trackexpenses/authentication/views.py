from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_generator
from django.contrib import auth
from django.contrib.auth import authenticate, login
import threading
from django.views.decorators.csrf import csrf_exempt

class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)


class UsernameValidateAPIView(APIView):
    def post(self, request):
        data = request.data
        username = data['username']
        if not str(username).isalnum():
            return Response({'username_error': 'Username should only have alphanumeric characters'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            return Response({'username_error': 'This Username is already used, choose another one'}, status=status.HTTP_409_CONFLICT)
        return Response({'username_valid': True})


class EmailValidateAPIView(APIView):
    def post(self, request):
        data = request.data
        email = data['email']
        if not validate_email(email):
            return Response({'email_error': 'Email is invalid'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            return Response({'email_error': 'This email is already used, choose another one'}, status=status.HTTP_409_CONFLICT)
        return Response({'email_valid': True})


class RegistrationAPIView(APIView):
    def post(self, request):
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        confirm_password=request.data.get('confirm_password')
        

        if not first_name or not last_name or  not username or not email or not password or not confirm_password:
            return Response({'error': 'All fields are requirored'}, status=status.HTTP_400_BAD_REQUEST)
        
        if password !=confirm_password:
            return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_409_CONFLICT)
        
        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists'}, status=status.HTTP_409_CONFLICT)

        if len(password) < 6:
            return Response({'error': 'Password is too short'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, email=email,password=password)
        user.first_name=first_name
        user.last_name=last_name
        user.set_password(password)
        user.is_active = False
        user.save()

        #Generate email verifica

        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        domain = get_current_site(request).domain
        link = reverse('activate', kwargs={'uidb64': uidb64, 'token': token_generator.make_token(user)})
        activate_url = f'http://{domain}{link}'

        email_subject = 'Activate your account'
        email_body = f'Hi {user.username}, please use this link to verify your account: {activate_url}'

        email = EmailMessage(
            email_subject,
            email_body,
            'your-email@example.com',
            [email],
        )
        EmailThread(email).start()

        return Response({'success': 'Account successfully created, check your email for activation'}, status=status.HTTP_201_CREATED)


class VerificationAPIView(APIView):
    def get(self, request, uidb64, token):
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'error': 'Invalid activation link'}, status=status.HTTP_400_BAD_REQUEST)

        if user.is_active:
            return Response({'warning': 'User already activated'}, status=status.HTTP_400_BAD_REQUEST)

        if token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({'success': 'Account activated successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Activation link is invalid'}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    def post(self, request):
        # username = request.data.get('username')
        # password = request.data.get('password')
        email = request.data.get('email')
        password = request.data.get('password')
        print(f"Email: {email}, Password: {password}")


        if not email or not password:
            return Response({'error': 'Both fields are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
            print(f"User found: {user.username}") 
        except User.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate using email and password
        user = authenticate(username=user.username, password=password)

        # user = auth.authenticate(username=username, password=password)

        if user:
            if user.is_active:
                # auth.login(request, user)
                login(request,user)
                return Response({'success': f'Welcome. You are logged in!'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Account is not activated, please check your email'}, status=status.HTTP_403_FORBIDDEN)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    def post(self, request):
        auth.logout(request)
        return Response({'success': 'You have been logged out'}, status=status.HTTP_200_OK)
