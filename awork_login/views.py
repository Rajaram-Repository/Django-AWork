from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse,JsonResponse
from .forms import UserCreationForm,UserLoginForm
from .models import CustomUser,OTP
import hashlib
import requests
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
import random
from django_otp.plugins.otp_totp.models import TOTPDevice

def index(request):
    return render(request,'index.html')
def signup(request):
    if request.method =='POST':
        form = UserCreationForm(request.POST)
        print(form)
        if form.is_valid():
            print("done")
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            if CustomUser.objects.filter(username=username).exists():
                response_data = {'message': 'Username is available'}
                return JsonResponse(response_data)
            elif CustomUser.objects.filter(email=email).exists():
                messages.error(request, 'Email already used')
                return HttpResponse('Email already used')
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            password = form.cleaned_data['password']
            user = CustomUser.objects.create_user(username=username,password=password,first_name=first_name,last_name=last_name,email=email)
            set_hash_instance = SetHash(username=username, email=email)
            set_hash_instance.call_api()
            login(request, user)
            return redirect('home')
    form = UserCreationForm()
    login_form=UserLoginForm()
    return render(request,'register.html', {'form': form,'login_form':login_form})

def signin(request):
    if request.method=='POST':
        form = UserLoginForm(request.POST)
        print(form)
        username = form.cleaned_data['username']
        if CustomUser.objects.filter(username=username).exists():
            password =form.cleaned_data['password']
            print(username,password)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                print("mistake")
                messages.info(request, 'invalid login')
    form = UserCreationForm()
    login_form=UserLoginForm()
    return render(request,'register.html', {'form': form,'login_form':login_form})

@csrf_exempt  
def api_auth(request):
    if request.method=='POST':
        username=request.POST.get('username')
        print(username)
        if CustomUser.objects.filter(username=username).exists():
            password =request.POST.get('password')
            print(username,password)
            user = authenticate(request, username=username, password=password)
            if user is not None:
               status='success'
               return JsonResponse({'user': username, 'status' : status}) 
            status='failed'
        status='notfound'
    return JsonResponse({'user': 'invalid', 'status' : status})

@login_required
def user_logout(request):
    logout(request)
    return redirect('awork')

def test(request):
    print("------test")
    add_tag=False
    return render(request,'test.html',{'add_tag':add_tag})

def desktop(request):
    print("done")
    return render(request,'desktop.html')

def send_otp_email(new_email, otp):
    # Implement the logic to send an email with the OTP
    subject = 'Email Verification OTP'
    message = f'Your OTP for email verification is: {otp}'
    from_email = 'rockyram.vip@gmail.com'  # Set your email here
    recipient_list = [new_email]
    send_mail(subject, message, from_email, recipient_list)

def send_otp(request):
    print("send")
    if request.method=='POST':
        user = request.user
        new_email=request.POST.get('email', '')
        if CustomUser.objects.filter(email=new_email).exists() or OTP.objects.filter(new_email=new_email).exists():
            return JsonResponse({ 'message': 'already'})
        else:
            OTP.objects.filter(user=user).delete()
            otp = str(random.randint(100000, 999999))
            OTP.objects.create(user=user, otp_secret=otp,new_email=new_email)

            # Send OTP to the new email
            send_otp_email(new_email, otp)

        return JsonResponse({ 'message': 'scuss'})
    return JsonResponse({ 'message': 'failed'})

def verify_otp(request):
    print("verify")
    user = request.user
    otp_instance = OTP.objects.filter(user=user).first()

    if not otp_instance:
        messages.error(request, 'No OTP found. Please try again.')
        return redirect('send_otp')

    if request.method == 'POST':
        otp_entered=request.POST.get('otp')
        totp_device = TOTPDevice(user=user, confirmed=True, secret=otp_instance.otp_secret)
        if totp_device.verify_token(otp_entered):
            messages.success(request, 'OTP verified successfully!')
            return redirect('send_otp')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
    return render(request, 'home.html')
def home(request):
    if request.user.is_authenticated:
        username=username = request.user.username
        user_details=CustomUser.objects.filter(username=username)

        # url = "http://127.0.0.1:8000/awork/desktop/get_all_list"
        # response=requests.get(url,json={"username":username})

        # if response.status_code==200:
        #     desk_data = response.json()
        #     print(desk_data)
            # return render(request,'home.html',{"personal_data":user_details,"desk_data":desk_data})
        return render(request,'home.html',{"personal_data":user_details})
    return render(request,'home.html')

def profile(request):
    print("done")
    return render(request,'profile.html')

class SetHash():

    def __init__(self,username,email):
        self.username =username
        self.email =email

    def generate_hash_token(self):
        sha256_hash = hashlib.sha256()
        sha256_hash.update(self.email.encode('utf-8'))
        hash_token = sha256_hash.hexdigest()
        return hash_token
    
    def call_api(self):
        url = 'http://localhost:8000/awork/desktop/api/set-hash'
        user_hash = {
            'username': self.username,
            'hash': self.generate_hash_token(),
        }
        response = requests.post(url, user_hash)
        return response.status_code

