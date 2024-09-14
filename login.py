import firebase_admin
from firebase_admin import credentials, auth

# Initialize Firebase Admin SDK
cred = credentials.Certificate("desktop-assistant-a066c-firebase-adminsdk-t7095-56c262cf5a.json")  # Your Firebase service account key
firebase_admin.initialize_app(cred)


