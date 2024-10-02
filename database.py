import firebase_admin
from firebase_admin import credentials, auth, firestore
import pyrebase
from datetime import datetime

# Initialize Firebase Admin SDK with your service account
cred = credentials.Certificate("desktop-assistant-a066c-firebase-adminsdk-t7095-56c262cf5a.json")
firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()

# Firebase client configuration
firebase_config = {
    "apiKey": "AIzaSyCYprTDXIKbYnlDjgkE3rHIu_PyeIVszSY",
    "authDomain": "desktop-assistant-a066c.firebaseapp.com",
    "projectId": "desktop-assistant-a066c",
    "databaseURL": "https://dummy-url.firebaseio.com",  # Placeholder URL
    "storageBucket": "desktop-assistant-a066c.appspot.com",
    "messagingSenderId": "YOUR_MESSAGING_SENDER_ID",
    "appId": "YOUR_APP_ID"
}

# Initialize Firebase for client-side operations (Pyrebase)
firebase = pyrebase.initialize_app(firebase_config)
auth_client = firebase.auth()


user_id = None

# Sign-Up Function
# Sign-Up Function
def sign_up(email, password, first_name, last_name, gender):
    global user_id
    try:
        # Create a new user in Firebase Authentication
        user = auth_client.create_user_with_email_and_password(email, password)
        user_id = user['localId']  # Get the user ID
        
        # Store additional user details in Firestore
        try:
            db.collection('users').document(user_id).set({
                'firstName': first_name,
                'lastName': last_name,
                'email': email,
                'gender': gender
            })
            print(f"User details saved in Firestore for UID: {user_id}")
        except Exception as e:
            print(f"Error saving user details to Firestore: {e}")

        return user_id
    except Exception as e:
        return str(e)


# Login Function
def log_in(email, password):
    global user_id
    try:
        # Log in the user using email and password
        user=auth_client.sign_in_with_email_and_password(email, password)
        user_id = user['localId']
        return user_id
    except Exception as e:
        return str(e)

def save_conversation(user_id, user_input, assistant_response):
    try:
        # Create a conversation document in the user's conversation subcollection
        conversation_ref = db.collection('users').document(user_id).collection('conversations').document()
        conversation_ref.set({
            'user_input': user_input,
            'assistant_response': assistant_response,
            'timestamp': datetime.utcnow()
        })
        print(f"Conversation saved for UID: {user_id}")
    except Exception as e:
        print(f"Error saving conversation: {e}")


# Retrieve user conversations
def get_conversations(user_id):
    try:
        # Retrieve all conversations for the user
        conversations = db.collection('users').document(user_id).collection('conversations').order_by('timestamp').get()
        
        for conv in conversations:
            print(f"User Input: {conv.to_dict().get('user_input')}")
            print(f"Assistant Response: {conv.to_dict().get('assistant_response')}")
            print(f"Timestamp: {conv.to_dict().get('timestamp')}")
            print("-" * 20)
            
    except Exception as e:
        print(f"Error retrieving conversations: {e}")

# Example Usage:
# Sign up a new user
# sign_up("neser@example.com", "strongpassword123", "John", "Doe", "Male")

# Log in the user
# log_in("shady@gmail.com", "Shadab@1234")
# save_conversation(user_id,"Hello","i m nnoo")
# get_conversations(user_id)
