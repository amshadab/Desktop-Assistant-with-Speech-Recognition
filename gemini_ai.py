import google.generativeai as ai
from google.generativeai.types.generation_types import StopCandidateException
from config import API_KEY


# Configure the API


# Start a conversation

def aispeechmode(query):

    ai.configure(api_key=API_KEY)

# Create a new model and chat object once
    model = ai.GenerativeModel("gemini-pro")
    chat = model.start_chat()
    try:
        # Send message to the API
        response = chat.send_message(query)
        return f"Chatbot: {response.text}"
        
            
    except StopCandidateException as e:
        return "Chatbot: That question seems to be causing an issue. Please try rephrasing."
    except Exception as e:
        return f"Chatbot: Sorry, something went wrong. {e}"

   