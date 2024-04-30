from django.shortcuts import render,redirect
from django.views import View #rewuest,response
from django.http import JsonResponse
from django.contrib.auth.models import User
import json
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from django.urls import reverse


from django.utils.encoding import force_bytes,force_str,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_generator
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import threading

class EmailThread(threading.Thread):
  def __init__(self, email):
    self.email=email
    threading.Thread.__init__(self)

  def run(self):
    self.email.send(fail_silently=False)



class UsernameValidateView(View):
 def post(self,request):
  data= json.loads(request.body)
  username=data['username']
  if not str(username).isalnum():
   return JsonResponse({'username_error':'Username should  only have alphanumeic value'},status=400)
  if User.objects.filter(username=username).exists():
   return JsonResponse({'username_error':'This Username is already used, choose another one '},status=409)
  return JsonResponse({'username_valid':True})

  
 #For EMAIL

class EmailValidateView(View):
 def post(self,request):
  data= json.loads(request.body)
  email=data['email']
  if not validate_email(email):
   return JsonResponse({'email_error':'Email is invalid '},status=400)
  if User.objects.filter(email=email).exists():
   return JsonResponse({'email_error':'This email is already used, choose another one '},status=409)
  return JsonResponse({'email_valid':True})

class RegistrationView(View):
 def get(self,request):
  return render(request,'authentication/register.html')
 

 #after clicking submit
 def post(self,request):
  username = request.POST['username']
  email = request.POST['email']
  password = request.POST['password']

  context={
   'fieldValues': request.POST
  }
  if not username or not email or not password:
   messages.error(request,"All fields are required")
   return render(request,'authentication/register.html',context)

  if not User.objects.filter(username=username).exists():
   if not User.objects.filter(email=email).exists():
    if len(password)<6:
     messages.error(request,"Password is short.")
     return render(request,'authentication/register.html',context)
    else:
     user=User.objects.create_user(username=username,email=email)
     user.set_password(password)
     user.is_active=False
     user.save()



     # uidb64 = force_bytes(urlsafe_base64_encode(user.pk))
     uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

     domain = get_current_site(request).domain
     link=reverse('activate',kwargs={'uidb64':uidb64,'token':token_generator.make_token(user)})
     email_subject='Activate your account'

     acivate_url = 'http://'+domain+link
     email_body='Hi'+ user.username + 'Please use this link for verification of your account\n'+ acivate_url
     email = EmailMessage(
     email_subject,
     email_body,
    'dikshyapaudel9@gmail.com', #from the emaiik
    # from_email=settings.EMAIL_HOST_USER
    
     [email], #where you are sending email, so this is receipt who already have email when they are sending form 
  
)
     EmailThread(email).start()
     messages.success(request,"Account successfully created")
     return redirect('login')
   

  return render(request,'authentication/register.html')
 

#   return redirect('login')
class VerificationView(View):
  def get(self, request, uidb64, token):
    try:
      id = force_str(urlsafe_base64_decode(uidb64))
      user = User.objects.get(pk=id)
      
    except(TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
        user = None
        messages.error(request, 'Error verifying account activation: {}'.format(str(e)))
        return redirect('login')
   
    if user is not None and token_generator.check_token(user, token):
        user.is_active = True 
        user.save()

        messages.success(request, 'Account activated successfully')
        return redirect('login')
     
    elif not token_generator.check_token(user, token):
        
        messages.warning(request,'User already activated')
        return redirect('login')
     
    elif user.is_active:
        messages.warning(request,'User already activated')
        return redirect('login')

    else:
        messages.error(request, 'Activation link is invalid!')
        return redirect('login')
    


 
class LoginView(View):
 def get(self,request):
  return render(request, 'authentication/login.html')
 def post(self, request):
  username=request.POST['username'];
  password=request.POST['password'];

  if username and password:
    user= auth.authenticate(username=username, password=password)

    if user:
      if user.is_active:
        auth.login(request, user)
        messages.success(request,"Welcome, "+user.username+" You are loggged in !")
        return redirect('expenses')
    

      messages.error(request,"Account is not activated, please check your email")  
      return render(request,'authentication/login.html')
    
    messages.error(request,"Invalid credentials")  
    return render(request,'authentication/login.html')
  
  messages.error(request,"")  
  return render(request,'authentication/login.html')


class LogoutView(View):
  def post(self,request):
    auth.logout(request)
    messages.success(request,'You have been logged out')
    return redirect('login')