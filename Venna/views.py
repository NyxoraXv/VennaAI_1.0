from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
from . import AzureAPI

@csrf_exempt
def index(request):
    return render(request, 'index.html')

@csrf_exempt
def chat_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message')

        # Retrieve system content from environment variable
        system_content = os.getenv("SYSTEM_CONTENT", "default system content if not set")

        # Get conversation history from cookies
        conversation_history = json.loads(request.COOKIES.get("conversation_history", "[]"))

        # If no previous conversation history, add system content as the initial message
        if not conversation_history:
            conversation_history.append({"role": "system", "content": system_content})

        # Add the user message to the conversation history
        conversation_history.append({"role": "user", "content": user_message})

        # Get assistant response from AzureAPI
        try:
            assistant_response = AzureAPI.Chat(conversation_history)
            # Add assistant's message to the conversation history
            conversation_history.append({"role": "assistant", "content": assistant_response})

            # Prepare JSON response and update conversation history in cookies
            response_data = JsonResponse({'response': assistant_response})
            response_data.set_cookie("conversation_history", json.dumps(conversation_history), max_age=3600)  # Cookie lasts 1 hour
            return response_data

        except Exception as e:
            return JsonResponse({"error": "Failed to retrieve response from API", "details": str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)
