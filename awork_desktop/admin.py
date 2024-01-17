from django.contrib import admin
from .models import IPDetails,Schedule,Message
# Register your models here.

admin.site.register(IPDetails)
admin.site.register(Schedule)
admin.site.register(Message)