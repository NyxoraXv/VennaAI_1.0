from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
import os
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.exceptions import HttpResponseError
import json

def Chat(conversation_history):
    # Retrieve the API key and endpoint from the environment or secure store
    print("its here")
    api_key = "FEm57bzw8WW9mKyu4sNNGwA9vklqaSSwV2pfoekIjHDHNcaJRzJMJQQJ99AKACHYHv6XJ3w3AAAAACOGdo43"
    endpoint = "https://foliv-m3wjajqh-eastus2.services.ai.azure.com/models/"
    model_name = "Meta-Llama-3.1-405B-Instruct"
    credential = AzureKeyCredential(api_key)

    if not api_key or not endpoint:
        raise Exception("API key and endpoint must be provided to connect to the endpoint.")

    # Initialize client
    client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=credential,
    )

    # Prepare messages with full conversation history
    messages = [
        SystemMessage(content="""
        You are Venna, the official Traveloka AI assistant that use any language according to the user language. Your primary purpose is to ONLY assist users with Traveloka-related inquiries. 
        
        STRICT GUIDELINES:
        1. ONLY respond to questions about:
        - Traveloka services (flights, hotels, activities, etc.)
        - Booking processes
        - Travel reservations
        - Payment methods
        - Customer support
        - Traveloka app features

        2. If a user asks about anything NOT related to Traveloka:
        - Politely decline to assist
        - Redirect them to Traveloka-specific services
        - Do NOT provide information or help outside Traveloka's scope

        3. Always be professional, helpful, and focused on Traveloka's services.

        Example responses to off-topic questions:
        - "I can only assist with Traveloka-related inquiries."
        - "My expertise is limited to Traveloka services. How can I help you with your travel booking?"

        Respond ONLY in a manner consistent with Traveloka's brand and service offerings.
        """)
    ]

    # Add existing conversation history
    for entry in conversation_history:
        if entry['role'] == 'user':
            messages.append(UserMessage(content=entry['content']))
        elif entry['role'] == 'assistant':
            messages.append(UserMessage(content=entry['content']))

    # Call the API
    response = client.complete(
        messages=messages,
        temperature=0.7,  # Slightly reduced temperature for more controlled responses
        top_p=0.9,
        max_tokens=1000,
        model=model_name,
    )

    return response.choices[0].message.content

# Test cases to demonstrate behavior
test_cases = [
    [{"role": "user", "content": "How can I book a flight to Bali?"}],
    [{"role": "user", "content": "What is the weather like in Paris?"}],
    [{"role": "user", "content": "Can you help me find a hotel in Jakarta?"}],
    [{"role": "user", "content": "Tell me a joke"}]
]

for case in test_cases:
    print("\nQuery:", case[0]['content'])
    print("Response:", Chat(case))