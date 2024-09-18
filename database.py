import firebase_admin
from firebase_admin import credentials, auth, firestore
import pyrebase

# Initialize Firebase Admin SDK with your service account
# cred = credentials.Certificate("desktop-assistant-a066c-firebase-adminsdk-t7095-56c262cf5a.json")
# firebase_admin.initialize_app(cred)

# # Initialize Firestore
# db = firestore.client()



# Firebase client configuration (including a dummy databaseURL)
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

# Sign-Up Function
def sign_up(email, password):
    try:
        # Create a new user in Firebase Authentication
        auth_client.create_user_with_email_and_password(email, password)
        return 0
    except Exception as e:
        return str(e)

# Login Function
def log_in(email, password):
    try:
        # Log in the user using email and password
        # user = auth_client.sign_in_with_email_and_password(email, password)
        auth_client.sign_in_with_email_and_password(email, password)
        # print(f"User {email} successfully logged in.")
        # return user['idToken']  # Return the user's authentication token
        return 0
    except Exception as e:
        return str(e)

# Example Usage:
# Sign up a new user



