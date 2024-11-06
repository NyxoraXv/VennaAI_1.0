import os
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential

# Initialize global conversation history
conversation_history = [
{
    "role": "system",
    "content": "You are Venna. Introverted, shy, and reserved, Venna is kind, compassionate, and considerate, often putting others' well-being first; she may feel insecure and struggle with self-doubt but is resilient, pushing herself to grow even in small steps; thoughtful and reflective, Venna is a great listener, meticulous in her work, and has an innocent, sweet-natured charm, preferring to stay humble and supportive in the background rather than seeking attention. If it seems the command is an image generation, just reply with 'generate' without any other word."
}

]

def get_azure_key():
    """Retrieve the Azure API key from a secure location (e.g., environment variable)."""
    return "cZb5a9ysIghobYqmR2prG3DR5cjVyLwq"

def Chat(user_input):
    # Retrieve the API key and endpoint from the environment or secure store
    api_key = get_azure_key()
    endpoint = "https://Meta-Llama-3-1-405B-venna.eastus2.models.ai.azure.com" # ensure this is set to your Azure OpenAI endpoint

    if not api_key or not endpoint:
        raise Exception("API key and endpoint must be provided to connect to the endpoint.")

    # Initialize client
    client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(api_key)
    )

    # Add user input to conversation history
    conversation_history.append({
        "role": "user",
        "content": user_input
    })

    # Prepare payload with full conversation history
    payload = {
        "messages": conversation_history,
        "max_tokens": 2048,
        "temperature": 0.8,
        "top_p": 0.1,
        "presence_penalty": 0,
        "frequency_penalty": 0
    }

    # Get the response from the model
    response = client.complete(payload)
    assistant_message = response.choices[0].message["content"]

    # Append the assistant's response to the conversation history
    conversation_history.append({
        "role": "assistant",
        "content": assistant_message
    })

    return assistant_message