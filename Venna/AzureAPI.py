import os
import json
from django.http import JsonResponse
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential

def Chat(request):
    if request.method == 'POST':
        user_message = json.loads(request.body).get('message')

        # Retrieve system content from environment variable
        system_content = os.getenv("SYSTEM_CONTENT", "default system content if not set")

        # Get conversation history from cookies
        conversation_history = json.loads(request.COOKIES.get("conversation_history", "[]"))

        # If no previous conversation history, add system content as the initial message
        if not conversation_history:
            conversation_history.append({"role": "system", "content": system_content})

        # Add the user message to the conversation history
        conversation_history.append({"role": "user", "content": user_message})

        # API client initialization and call
        client = ChatCompletionsClient(
            endpoint="https://Meta-Llama-3-1-405B-venna.eastus2.models.ai.azure.com",
            credential=AzureKeyCredential(get_azure_key())
        )
        payload = {
            "messages": conversation_history,
            "max_tokens": 2048,
            "temperature": 0.8,
            "top_p": 0.1,
            "presence_penalty": 0,
            "frequency_penalty": 0
        }

        response = client.complete(payload)
        assistant_message = response.choices[0].message["content"]

        # Add the assistant's response to the conversation history
        conversation_history.append({"role": "assistant", "content": assistant_message})

        # Return the assistant response, and set updated conversation history in cookies
        response_data = JsonResponse({"response": assistant_message})
        response_data.set_cookie("conversation_history", json.dumps(conversation_history), max_age=3600)  # Cookie lasts 1 hour
        return response_data

    return JsonResponse({"error": "Only POST requests are allowed."}, status=400)

def get_azure_key():
    return os.getenv("AZURE_API_KEY")  # Ensure AZURE_API_KEY is set in the environment variables
