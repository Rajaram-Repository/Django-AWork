import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.contrib.auth.models import AnonymousUser
import requests
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        
        self.room_name = self.scope['url_route']['kwargs']['room_slug']
        self.roomGroupName = 'connect_%s' % self.room_name
        headers = dict(self.scope['headers'])
        if b'authorization' in headers:
            print("user-if")
            try:
                token_name, token_key = headers[b'authorization'].decode().split()
                verify = await self.verify_token(self.room_name,token_key)
                if verify :
                    self.scope['username'] = self.room_name
                    self.scope['token'] = token_key
                else :
                    return await self.close()
            except Exception as e:
                self.scope['user'] = AnonymousUser()
                return await self.close()
        else :
            print("user-else")
            query_string = self.scope.get('query_string', b'').decode('utf-8')
            query_params = dict(x.split('=') for x in query_string.split('&'))
            token = query_params.get('token', None)
            if not token:
                return await self.close() 
            else:
                verify = await self.verify_token(self.room_name,token)
                if verify :
                    self.scope['username'] ="#$web$#-"+self.room_name
                    self.scope['token'] = token
                else :
                    return await self.close()
        await self.channel_layer.group_add(
            self.roomGroupName,
            self.channel_name
        )
        await self.accept()
        print("accept-user",self.scope['username'])
        if "#$web$#-" not in self.scope['username']:
            await self.set_desk_sync(self.scope['username'],"desk_sync","1")
        data = await self.get_list(self.scope['username'])
        res = json.dumps(data, indent=2)
        parsed_data = json.loads(res)
        desk_list_str = parsed_data["desk_list"]
        desk_list = json.loads(desk_list_str)
        # await self.send(text_data=json.dumps({"message": desk_list}))
        await self.channel_layer.group_send(
        self.roomGroupName,
        {
            'type': 'sendMessage',
            'message': json.dumps({"message": desk_list}),
        }
    )
        
    async def disconnect(self, close_code):
        if "#$web$#-" not in self.scope['username']:
            await self.set_desk_sync(self.scope['username'],"desk_sync","0")
        await self.channel_layer.group_discard(
            self.roomGroupName,
            self.channel_name
        )

        
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        desk_name = self.scope['username']
        if '#$message$#-' in text_data_json:
            print("message",text_data_json)
            msg = await self.save_message(text_data_json['#$message$#-'])
            print(msg)
        elif '#$result$#-' in text_data_json:
            print("result",text_data_json)
            msg = await self.save_result(text_data_json['#$result$#-'])
            print(msg)
        print(desk_name)
        data = await self.get_list(desk_name)
        res = json.dumps(data, indent=2)
        parsed_data = json.loads(res)
        desk_list_str = parsed_data["desk_list"]
        desk_list = json.loads(desk_list_str)
        print("recive get list : ",desk_list)
        # await self.send(text_data=json.dumps({"message": desk_list}))
        await self.channel_layer.group_send(
        self.roomGroupName,
        {
            'type': 'sendMessage',
            'message': json.dumps({"message": desk_list}),
        }
    )

    async def sendMessage(self, event):
        message = event["message"]
        await self.send(text_data= message)
        
    @sync_to_async
    def get_list(self,data):
        if "#$web$#-" in data:
            data = data.replace("#$web$#-","")
        url = "http://127.0.0.1:8000/awork/desktop/get_list"
        response=requests.get(url,json={"desk_name":data})
        msg = {'error': 'API request failed'}
        if response.status_code == 200:
            msg=response.json()
        return msg
    @sync_to_async
    def set_desk_sync(self,user,sync,data):
        print(data)
        url = "http://127.0.0.1:8000/awork/desktop/sync/"+sync+"/"+data
        response=requests.get(url,json={"desk_name":user})
        print(response.text)


    @sync_to_async
    def save_message(self,data):
        print("message",data)
        url = "http://127.0.0.1:8000/awork/desktop/edit_schedule"
        headers = {
            'Content-Type': 'application/json',
            'X-CSRFToken': data['csrfmiddlewaretoken'],
        }
        msg = {'error': 'API request failed'}
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            msg={'success': 'API request save'}
        return msg
    
    @sync_to_async
    def save_result(self,data):
        print("result",data)
        url = "http://127.0.0.1:8000/awork/desktop/save_result"
        msg = {'error': 'API request failed'}
        response = requests.post(url, json=data)
        if response.status_code == 200:
            msg={'success': 'API request save'}
        return msg
    
    @sync_to_async
    def verify_token(self,username,token):
        url = "http://127.0.0.1:8000/awork/desktop/api/verify_token"
        headers = {
            "Authorization": token,
            "Username": username,
            "Content-Type": "application/json",  
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return True
        return False