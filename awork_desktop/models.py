import secrets
from django.conf import settings
from django.db import models
import json

class IPDetails(models.Model):
    username = models.CharField(max_length=128, blank=True, null=True) 
    ipadress = models.CharField(max_length=128, blank=True, null=True)
    name = models.CharField( max_length=255 , unique=True)
    password = models.CharField(max_length=128, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    query_id = models.TextField(blank=True, null=True) 
    token = models.CharField(max_length=255, null=True)
    desk_sync = models.BooleanField(default=False)
    web_sync = models.BooleanField(default=False)


    def generate_token(self):
        """
        Generate a random token and save it to the model.
        """
        self.token = secrets.token_hex(32)
        self.save()
        return self.token

class Schedule(models.Model):
    row_id = models.IntegerField(blank=True, null=True)
    schedule_name = models.CharField(blank=True, max_length=255, null=True)
    schedule_query_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date = models.DateField(null=True)
    time = models.TimeField(null=True)
    utc = models.CharField(max_length=255,null=True)
    query = models.JSONField()
    schedule_ipadress = models.ForeignKey(IPDetails, on_delete=models.CASCADE, related_name='schedule_ip_books')
    def set_query_data(self, data):
        self.query_data = json.dumps(data)

    def get_query_data(self):
        return json.loads(self.query_data) if self.query_data else {}

class Message(models.Model):
    message = models.TextField(blank=True, null=True) 
    type = models.TextField(blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    schedule_id = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='schedule_id')


