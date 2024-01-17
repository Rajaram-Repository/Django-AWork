from django.shortcuts import render
from .models import IPDetails,Schedule,Message
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import IPDetailsForm
from django.contrib.auth import get_user_model
from django.db.models import Prefetch
import requests
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import IPDetails
import secrets
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render, get_object_or_404, redirect
from .models import Schedule
from .forms import ScheduleForm
from django.utils import timezone
import json
from django.db.models import Max

@csrf_exempt
def generate_token(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        desk_name=request.POST.get('desk_name')
        desk_password=request.POST.get('desk_password')
        login_response = requests.post('http://127.0.0.1:8000/awork/api_auth', data={'username': username, 'password': password})
        if login_response.status_code == 200 :
            if login_response.json()['status']=='success':
                desk_name =username+desk_name
                if IPDetails.objects.filter(name=desk_name).exists():
                    obj = IPDetails.objects.filter(name=desk_name).first()
                    token_value = obj.token
                    return JsonResponse({'user':username,'token': token_value})
                ip_details_instance = IPDetails(
                    username=username,
                    ipadress='192.168.1.1',
                    name=desk_name,
                    query_id='example_query_id'
                )
                token_value=ip_details_instance.generate_token()
                hashed_password = make_password(desk_password)
                ip_details_instance.password = hashed_password
                ip_details_instance.save()
                return JsonResponse({'user':username,'token': token_value})
            return JsonResponse({'user':'invalid','token': 'username or password in correct'}, status=404)
        return JsonResponse({'user':'invalid','token': 'connection error'}, status=404)
    return JsonResponse({'user':'invalid','token': 'invalid'}, status=404)

@csrf_exempt
def verify_token(request):
    token = request.headers.get('Authorization')
    username = request.headers.get('Username')
    if IPDetails.objects.filter(name=username,token=token).exists():
        return JsonResponse({'detail': 'Token is valid', 'user_id': username})
    return JsonResponse({'detail': 'Token is invalid', 'user_id': "invalid"}, status=404)

def desk_sync(request,sync, flag):
    
    try:
        data = json.loads(request.body)
        desk_name = data.get("desk_name")
        print("__________+",desk_name)
        val=False
        if flag =='1':
            val =True
        ip_details = IPDetails.objects.filter(name=desk_name).first()  
        if ip_details:
            if sync == 'web_sync':
                IPDetails.objects.filter(name=desk_name).update(web_sync=val)
            else:
                IPDetails.objects.filter(name=desk_name).update(desk_sync=val)
            
            return JsonResponse({"success": "success"})
        else:
            return JsonResponse({"error": "Desk not found"})
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON in request body"})
    except Exception as e:
        return JsonResponse({"error": str(e)})
def is_valid_room ():
    pass
@csrf_exempt
def hash(request):

    return ""

from django.core.serializers import serialize
from django.http import JsonResponse

def get_list(request):
    data = json.loads(request.body)
    desk_name = data.get("desk_name")
    ip_details = IPDetails.objects.filter(name=desk_name).first()
    
    if ip_details:
        desk_list = Schedule.objects.filter(schedule_ipadress=ip_details)
        serialized_desk_list = serialize('json', desk_list)
        return JsonResponse({'desk_list': serialized_desk_list}, safe=False)

    return JsonResponse({'error': 'No IPDetails found for the given desk_name'}, status=400)
def get_all_list(request):
    data = json.loads(request.body)
    user_name = data.get("username")
    user_details = IPDetails.objects.filter(username=user_name)
    if user_details:
        data = serialize('json', user_details)
        return JsonResponse(data, safe=False)
    return JsonResponse({'error': 'No Data'}, status=400)
# def all_messages(request):
#     username =request.user.username
#     ip_details = get_object_or_404(IPDetails, username=username)
#     schedules = Schedule.objects.filter(schedule_ipadress=ip_details)
#     messages = Message.objects.filter(schedule_id__in=schedules)
#     context = {
#         'username': username,
#         'message_schedule_pairs': zip(messages, schedules),
#     }
#     return JsonResponse(context)

def all_messages(request):
    username = request.user.username
    ip_details_data = IPDetails.objects.filter(username=username).prefetch_related(
        Prefetch('schedule_ip_books', queryset=Schedule.objects.prefetch_related(
            Prefetch('schedule_id', queryset=Message.objects.all(), to_attr='messages')
        ))
    )

    message_schedule_pairs = []

    for ip_details in ip_details_data:
        for schedule in ip_details.schedule_ip_books.all():
            for message in schedule.messages:
                message_schedule_pairs.append({
                    'message': message.message,
                    'schedule_details': {
                        'desk_name': ip_details.name,
                        'time': message.created_at,
                        'schedule_name': schedule.schedule_name,
                        # Add more schedule details as needed
                    }
                })

    print(message_schedule_pairs)
    return JsonResponse({'message_schedule_pairs': message_schedule_pairs})

@csrf_exempt
def save_result(request):
    print("save__")
    data = json.loads(request.body)
    id = data.get("id_schedule")
    msg = data.get("output")
    print(id,msg)
    schedule =Schedule.objects.filter(pk=id).first()
    if schedule:
        Message.objects.create(message=msg,schedule_id=schedule)
        return JsonResponse({"success": "success"})
    return JsonResponse({"error": "Desk not found"})

def check_query(query):
    c = 1
    result = {"query":{}}
    for i,j in query["query"].items():
        print(i," ",j)
        if "ID" in j:
            url = "http://127.0.0.1:8000/awork/post/get_data/"+j["ID"]
            response=requests.get(url)
            if response.status_code==200:
                data=response.json()
                print(data["json_data"])
                for a,b in data['json_data']["query"].items():
                    result['query'][c]=b
                    c+=1
            else:
                return False
        else:
            result['query'][c]=j
            c+=1
    
    return result
def edit_schedule(request):
    username=request.user.username
    if request.method =='POST':
        data = json.loads(request.body)
        desk_name=data.get("desk_name")
        id_schedule = data.get("id_schedule")
        row_id = data.get("row_id")
        name=data.get("task_name")
        date=data.get("date")
        time=data.get("time")  
        utc=data.get("utc")
        query=check_query(data.get("query"))
        if query==False:
            print("false - ",query)
            return JsonResponse({"Error":"Query Error"})
        print(data,desk_name,id_schedule,row_id,name,date,time,utc,query)
        ip_details = IPDetails.objects.filter(name=desk_name).first()
        
        if row_id =="":
            max_row_id = 0
            if Schedule.objects.filter(schedule_ipadress=ip_details).exists():
                max_row_id = Schedule.objects.filter(schedule_ipadress=ip_details).aggregate(Max('row_id'))['row_id__max']
            schedule =  Schedule.objects.create(
                    row_id = int(max_row_id)+1,
                    schedule_name=name,
                    schedule_query_id=1,
                    updated_at=timezone.now(),
                    date=date,
                    time=time,
                    utc=utc,
                    query=query,
                    schedule_ipadress=ip_details,                
                )
            schedule.save()
            return JsonResponse({"success ":"Query success "})
        else:
            schedule = Schedule.objects.filter(row_id = row_id).update(
                schedule_name=name,
                schedule_query_id=1,
                updated_at=timezone.now(),
                date=date,
                time=time,
                utc=utc,
                query=query,
                schedule_ipadress=ip_details,                
                )
            schedule.save()
            return JsonResponse({"success ":"Query success "})
    desk_list = IPDetails.objects.filter(username=username).prefetch_related('schedule_ip_books')
    if desk_list.exists() :
        return render(request,'desktop.html',{'add_tag':False,'desk_list':desk_list})
    return render(request,'desktop.html',{'add_tag':True})

def desktop(request):
    username=request.user.username
    if request.method == 'POST':
        desk_name = request.POST.get('desk_name')
        password = request.POST.get('password')
        if IPDetails.objects.filter(name=desk_name).exists():
            obj = IPDetails.objects.get(name=desk_name)
            if check_password(password, obj.password):
                obj.web_sync=True
                obj.save()
    desk_list = IPDetails.objects.filter(username=username).prefetch_related('schedule_ip_books')
    if desk_list.exists() :
         return render(request,'desktop.html',{'add_tag':False,'desk_list':desk_list})
    return render(request,'desktop.html',{'add_tag':True})

def my_json_view(request):
    # Your data to be returned as JSON
    data = [
        {'key1': 'value1'},
        {'key2': 'value2'},
    ]
    return JsonResponse(data, safe=False)



