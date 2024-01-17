from django.http import HttpResponse
from django.views.generic import View
import os

class DownloadScriptView(View):
    def get(self, request, *args, **kwargs):
        # Path to the script file
        script_path = os.path.join(os.path.dirname(__file__), 'downloads', 'workapp.exe')

        # Open and read the content of the file
        with open(script_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = 'attachment; filename=AWork.exe'
            return response
