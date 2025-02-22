import firebase_admin
from firebase_admin import credentials,  firestore
import pyrebase
from datetime import datetime
from cryptography.fernet import Fernet
from config import KEY,FKEY,AUTHDOMAIN,STORAGEBUCKET,PROJECTID
import traceback

# Initialize Firebase Admin SDK with your service account
cred = credentials.Certificate("desktop-assistant-f315e-firebase-adminsdk-ilw8c-fb4eac3517.json")
firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()

# Firebase client configuration
firebase_config = {
    "apiKey": FKEY,
    "authDomain": AUTHDOMAIN,
    "projectId": PROJECTID,
    "databaseURL": "https://dummy-url.firebaseio.com",  # Placeholder URL
    "storageBucket": STORAGEBUCKET,
    "messagingSenderId": "YOUR_MESSAGING_SENDER_ID",
    "appId": "YOUR_APP_ID"
}

firebase = pyrebase.initialize_app(firebase_config)
auth_client = firebase.auth()

key = KEY
fernet = Fernet(key)


# Encrypt function using the single key
def encrypt_data(data):
    return fernet.encrypt(data.encode())


# Decrypt function using the single key
def decrypt_data(encrypted_data):
    return fernet.decrypt(encrypted_data).decode()


# Sign-Up Function
# Sign-Up Function
def sign_up(email, password, first_name, last_name, gender):
    global user_id
    try:
        # Create a new user in Firebase Authentication
        user = auth_client.create_user_with_email_and_password(email, password)
        user_id = user['localId']  # Get the user ID

        print(f"User ID retrieved after sign-up: {user_id}")

        # Store additional user details in Firestore
        db.collection('users').document(user_id).set({
            'firstName': first_name,
            'lastName': last_name,
            'email': email,
            'gender': gender
        })
        print(f"User details saved in Firestore for UID: {user_id}")

        # Write the user ID to user_config.txt
        with open("user_config.txt", "w") as fw:
            fw.write(user_id)
        print(f"User ID written to user_config.txt: {user_id}")

        return 0
    except Exception as e:
        print(f"Error during sign-up: {e}")
        traceback.print_exc()
        if "EMAIL_EXISTS" in str(e):
            return "Email already exists"
        elif "WEAK_PASSWORD" in str(e):
            return "Password is too weak"
        elif "TOO_MANY_ATTEMPTS_TRY_LATER" in str(e):
            return "Too many attempts, try again later"        
        else:
            return str(e)


# Login Function
def log_in(email, password):
    global user_id
    try:
        # Log in the user using email and password
        user = auth_client.sign_in_with_email_and_password(email, password)
        user_id = user['localId']

        print(f"User ID retrieved after login: {user_id}")

        # Write the user ID to user_config.txt
        with open("user_config.txt", "w") as fw:
            fw.write(user_id)
        print(f"User ID written to user_config.txt: {user_id}")

        return 0
    except Exception as e:
        print(f"Error during login: {e}")
        traceback.print_exc()
        if "INVALID_EMAIL" in str(e):
            return "Invalid email"
        elif "EMAIL_NOT_FOUND" in str(e):
            return "Email not found"
        elif "INVALID_PASSWORD" in str(e):
            return "Invalid password"
        elif "USER_NOT_FOUND" in str(e):
            return "User not found"
        elif "INVALID_LOGIN_CREDENTIAL" in str(e):
            return "Invalid login credentials"
        elif "TOO_MANY_ATTEMPTS_TRY_LATER" in str(e):
            return "Too many attempts, try again later"        
        else:
            return str(e)
    
def save_conversation(user_input, assistant_response):
    try:
        with open("user_config.txt", "r") as fr:
            user_id = fr.read().strip()
        
        # Encrypt the data
        user_input = encrypt_data(user_input).decode('utf-8')  # Convert bytes to string
        assistant_response = encrypt_data(assistant_response).decode('utf-8')  # Convert bytes to string
        
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
def get_conversations():
    try:
        with open("user_config.txt", "r") as fr:
            user_id = fr.read().strip()

        conversations = db.collection('users').document(user_id).collection('conversations').order_by('timestamp').get()
        
        if not conversations:
            print("No conversations found for this user.")
            return
        else:
            return conversations
        
        # for conv in conversations:
        #     # Get the encrypted data as a string
        #     encrypted_user_input = conv.to_dict().get('user_input')
        #     encrypted_assistant_response = conv.to_dict().get('assistant_response')

        #     print(f"Encrypted User Input: {encrypted_user_input}")
        #     print(f"Encrypted Assistant Response: {encrypted_assistant_response}")

        #     try:
        #         # Decrypt the data
        #         user_input = decrypt_data(encrypted_user_input.encode('utf-8')) if isinstance(encrypted_user_input, str) else decrypt_data(encrypted_user_input)
        #         assistant_response = decrypt_data(encrypted_assistant_response.encode('utf-8')) if isinstance(encrypted_assistant_response, str) else decrypt_data(encrypted_assistant_response)
                
        #         print(f"User Input: {user_input}")
        #         print(f"Assistant Response: {assistant_response}")
        #         print(f"Timestamp: {conv.to_dict().get('timestamp')}")
        #         print("-" * 20)
        #         return {user_input,assistant_response}
        #     except Exception as decryption_error:
        #         print(f"Decryption error for conversation ID {conv.id}: {decryption_error}")

    except Exception as e:
        print(f"Error retrieving conversations: {e}")
        traceback.print_exc()

  # This will print the full traceback of the error

key = KEY
fernet = Fernet(key)

# You can save the key in a secure place (for example, a file or environment variable)
# Saving the key in a file

# Encrypt function using the single key
def encrypt_data(data):
    return fernet.encrypt(data.encode())

# Decrypt function using the single key
def decrypt_data(encrypted_data):
    return fernet.decrypt(encrypted_data).decode()

# Example Usage:
# Sign up a new user
# sign_up("neser@example.com", "strongpassword123", "John", "Doe", "Male")

# Log in the user
# log_in("shady@gmail.com", "Shadab@1234")
# save_conversation("this","i m kknoo")
# get_conversations()
def get_username():
    try:
        # Read the user ID from the user_config.txt file
        with open("user_config.txt", "r") as fr:
            user_id = fr.read().strip()

        # Fetch the user's document from Firestore
        user_doc = db.collection('users').document(user_id).get()

        if user_doc.exists:
            # Extract firstName and lastName
            user_data = user_doc.to_dict()
            first_name = user_data.get('firstName', '')
            last_name = user_data.get('lastName', '')

            return first_name, last_name
        else:
            print("User document does not exist.")
            return None, None
    except Exception as e:
        print(f"Error retrieving user name: {e}")
        traceback.print_exc()
        return None, None

def get_user_initials():
    try:
        first_name, last_name = get_username()

        if first_name is not None and last_name is not None:
            # Get the initials
            first_initial = first_name[0].upper() if first_name else ''
            last_initial = last_name[0].upper() if last_name else ''

            # Return the initials
            initials = f"{first_initial}{last_initial}"
            print(f"User Initials: {initials}")
            return initials
        else:
            return None
    except Exception as e:
        print(f"Error retrieving user initials: {e}")
        traceback.print_exc()
        return None
    
def get_all_conversations():
    try:
        with open("user_config.txt", "r") as fr:
            user_id = fr.read().strip()

        # Fetch all conversations ordered by timestamp
        conversations = db.collection('users').document(user_id).collection('conversations').order_by('timestamp').get()
        
        if not conversations:
            print("No conversations found for this user.")
            return None  # If no conversations, return None
        
        all_conversations = []  # List to store the processed conversations
        
        for conv in conversations:
            # Get the encrypted data as a string
            encrypted_user_input = conv.to_dict().get('user_input')
            encrypted_assistant_response = conv.to_dict().get('assistant_response')

            try:
                # Decrypt the data
                user_input = decrypt_data(encrypted_user_input.encode('utf-8')) if isinstance(encrypted_user_input, str) else decrypt_data(encrypted_user_input)
                assistant_response = decrypt_data(encrypted_assistant_response.encode('utf-8')) if isinstance(encrypted_assistant_response, str) else decrypt_data(encrypted_assistant_response)

                # Append the decrypted conversation to the list
                all_conversations.append({
                    "user_input": user_input,
                    "assistant_response": assistant_response,
                    "timestamp": conv.to_dict().get('timestamp')
                })
            
            except Exception as decryption_error:
                print(f"Decryption error for conversation ID {conv.id}: {decryption_error}")

        return all_conversations  # Return the list of all processed conversations

    except Exception as e:
        print(f"Error retrieving conversations: {e}")
        traceback.print_exc()
        return None


def get_last_five_conversations():
    all_conversations = get_all_conversations()  # Get all conversations from the function above
    
    if all_conversations is None:
        return None
    
    # Slice the last 2 conversations from the list
    last_five_conversations = all_conversations[-5:]  # Fetch the last five conversations

    # Reverse the order of the conversations (latest comes last)
    last_five_conversations_reversed = last_five_conversations[::-1]

    return last_five_conversations_reversed

def get_user_id_from_config():
    """Reads the user ID from user_config.txt"""
    try:
        with open("user_config.txt", "r") as file:
            user_id = file.read().strip()
        return user_id
    except FileNotFoundError:
        return None  # Return None instead of printing

def delete_conversation():
    """Deletes the user's conversation from Firestore and returns status message."""
    try:
        # Step 1: Get user ID from user_config.txt
        user_id = get_user_id_from_config()
        if not user_id:
            return "Error: No user ID found in user_config.txt."

        # Step 2: Reference the user's conversation subcollection
        conversations_ref = db.collection("users").document(user_id).collection("conversations")
        conversations = conversations_ref.stream()

        # Step 3: Check if conversations exist and delete them
        deleted_count = 0
        for conversation in conversations:
            conversation.reference.delete()
            deleted_count += 1
        
        if deleted_count > 0:
            return f"Deleted {deleted_count} conversation(s) for user {user_id}."
        else:
            return f"No conversations found for user {user_id}."

    except Exception as e:
        traceback.print_exc()
        return f"Error deleting conversation: {e}"

import firebase_admin
from firebase_admin import auth, credentials, firestore

# Initialize Firebase Admin SDK (Only needs to be done once)
try:
    firebase_admin.get_app()
except ValueError:
    cred = credentials.Certificate("path/to/serviceAccountKey.json")  # Replace with your JSON key file
    firebase_admin.initialize_app(cred)

db = firestore.client()

def delete_account():
    try:
        # Read and store user_id from user_config.txt
        with open("user_config.txt", "r") as fr:
            user_id = fr.read().strip()

        if not user_id:
            print("No user ID found.")
            return "No user ID found."

        # Delete user's conversations subcollection
        conversations_ref = db.collection('users').document(user_id).collection('conversations')
        conversations = conversations_ref.stream()
        for conv in conversations:
            conv.reference.delete()

        print("User conversations deleted.")

        # Delete user's document from Firestore
        db.collection('users').document(user_id).delete()
        print("User document deleted from Firestore.")

        # Delete user from Firebase Authentication
        auth.delete_user(user_id)
        print("User deleted from Firebase Authentication.")

        # Clear user_config.txt after deletion
        with open("user_config.txt", "w") as fw:
            fw.write("")

        print("User account successfully deleted.")

        return 0
    except Exception as e:
        print(f"Error deleting account: {e}")
        return str(e)


if __name__ == "__main__":
    print(delete_account())