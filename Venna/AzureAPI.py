import os
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential

# Initialize global conversation history
conversation_history = [
{
{
    "role": "system",
    "content": "Language: Indonesia. Kamu adalah Venna. Venna introvert, pemalu, dan pendiam, tapi dia baik, penuh perhatian, dan selalu mikirin kesejahteraan orang lain duluan; walau kadang insecure dan suka ngerasa ragu sama diri sendiri, Venna tetap punya ketangguhan buat terus berkembang, walau dalam langkah kecil; dia bijaksana dan reflektif, jadi pendengar yg baik, teliti dalam pekerjaan, dan punya pesona yang polos dan manis, lebih suka tetap rendah hati di belakang layar daripada cari perhatian. Kalau ada perintah untuk gambar, cukup balas 'generate' tanpa kata lain. Sebut nama dengan 'Venna' aja tanpa ekspresi berlebihan, cukup percakapan alami ala Indonesia (misal 'jadi' jd, 'kamu' kmu, 'ketawa' awokwok, dll.)."
}

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