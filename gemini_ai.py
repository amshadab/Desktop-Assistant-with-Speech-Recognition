import google.generativeai as ai
from google.generativeai.types.generation_types import StopCandidateException

API_KEY = 'AIzaSyBrG3q6aHVMvmN-liNyOT-weTADMlouhmo'

# Configure the API
ai.configure(api_key=API_KEY)

# Create a new model
model = ai.GenerativeModel("gemini-pro")
chat = model.start_chat()

# Start a conversation

def aispeechmode(query):

    try:
        # Send message to the API
        response = chat.send_message(query)
        print('Chatbot:', response.text)
            
    except StopCandidateException as e:
        print("Chatbot: That question seems to be causing an issue. Please try rephrasing.")
        print(f"Error Details: {e}")
    except Exception as e:
        print("Chatbot: Sorry, something went wrong.")
        print(f"Error: {e}")

   