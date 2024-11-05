from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from . import AzureAPI
# Create your views here.
@csrf_exempt
def index(request):
    return render(request, 'index.html')

@csrf_exempt
def chat_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message')

        assistant_response = AzureAPI.Chat(user_message)

        return JsonResponse({'response' : assistant_response})
    return JsonResponse({'error': 'Invalid request method'}, status=400) 