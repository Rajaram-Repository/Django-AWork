from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse,JsonResponse
from .forms import UserCreationForm,UserLoginForm
from .models import CustomUser
import hashlib
import requests


def index(request):
    return render(request,'index.html')

def signup(request):
    if request.method =='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
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
                messages.info(request, 'invalid login')
    form = UserCreationForm()
    login_form=UserLoginForm()
    return render(request,'register.html', {'form': form,'login_form':login_form})

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

def home(request):
    print("done")
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

