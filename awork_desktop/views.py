from django.shortcuts import render
from .models import UserDesk,IPDetails,Schedule
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import IPDetailsForm

import requests

@csrf_exempt
def hash(request):
    if request.method=='POST':
        username = request.POST.get('username', '')
        hash = request.POST.get('hash', '')
        print(username,hash)
        user = UserDesk.objects.create(username=username,hashtoken=hash)
        user.save()
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=400)

def desktop(request):
    username=request.user.username
    id = UserDesk.objects.get(username=username)
    flask_api_url = 'http://localhost:5001/api/method_to_call'

    try:
        response = requests.get(flask_api_url)
        if response.status_code == 200:
            flask_result = response.json()
            print(flask_result)
        else:
            print(response.status_code)

    except requests.RequestException as e:
        print(f'Request to Flask API failed: {e}')
    if request.method=='POST':
        form = IPDetailsForm(request.POST)
        if form.is_valid():
            ip=form.cleaned_data['ipadress']
            name=form.cleaned_data['name']
            password=form.cleaned_data['password']
            query_id=form.cleaned_data['query_id']
            print(form)
            ip = IPDetails.objects.create(ipadress=ip,name=name,password=password,query_id=query_id,user_id=id)
            ip.save()
            id = ip.user_id
    form_desk = IPDetailsForm()
    desk_list = IPDetails.objects.filter(user_id=id.pk)
    if desk_list.exists():
        return render(request,'desktop.html',{'add_tag':False,'form_desk':form_desk,'desk_list':desk_list})
    return render(request,'desktop.html',{'add_tag':True,'form_desk':form_desk})

def my_json_view(request):
    # Your data to be returned as JSON
    data = [
        {'key1': 'value1'},
        {'key2': 'value2'},
    ]

    # Using JsonResponse with safe=False for non-dictionary data
    return JsonResponse(data, safe=False)

