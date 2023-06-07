from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.db import IntegrityError
from .models import Profile
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    return render(request,'authentication/home.html')

def tokensent(request):
    return render(request,'authentication/tokensent.html')

def success(request):
    return render(request,'authentication/success.html')

def signupuser(request):
    if request.method == 'GET':
        return render(request,'authentication/signupuser.html')
    else:
        try:
            if request.POST['P1'] == request.POST['P2']:
                if User.objects.filter(username = request.POST['username']).first():
                    messages.success(request,'Username is already taken!')
                    return redirect('signupuser')
                if User.objects.filter(email = request.POST['email']).first():
                    messages.success(request,'Email is already taken!')
                    return redirect('signupuser')
                
                myuser = User.objects.create_user(username = request.POST['username'],password=request.POST['P1'],email = request.POST['email'])
                myuser.save()
                auth_token = str(uuid.uuid4())
                profile_obj = Profile.objects.create(user = myuser,auth_token = auth_token)
                profile_obj.save()
                send_mail_for_registration(request.POST['email'],auth_token)
                return redirect('tokensent')
                
            else:
                messages.success(request,"passwords doesn't match")
                return redirect('signupuser')
        except Exception as e:
                print(e)

def send_mail_for_registration(email,token):
    subject = "You account need to be verified"
    message = f'Hi paste this link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipitent_list = [email]
    send_mail(subject,message,email_from,recipitent_list)

def verify(request,auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('loginuser')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account is verified Succesfully!.')
            return redirect('success')
        else:
            return redirect('error')
    except Exception as e:
        print(e)
        return redirect('home')
    
def error(request):
    return  render(request , 'authentication/error.html')
@login_required(login_url='authentication/loginuser')
def welcome(request):
    return  render(request , 'authentication/welcome.html')

def loginuser(request):
    if request.method == "POST":
        user = authenticate(request,username = request.POST['username'],password = request.POST['password'])
        if user is None:
            messages.success(request, 'User Not Found.')
            return redirect('loginuser')
        profile_obj = Profile.objects.filter(user = user ).first()

        if not profile_obj.is_verified:
            messages.success(request, 'Profile is not verified check your mail.')
            return redirect('loginuser')
        login(request , user)    
        return redirect('welcome') 
    else:
        return render(request,'authentication/loginuser.html')

def logoutuser(request):
    if request.method == "POST":
        logout(request)
        return redirect("loginuser")