import pyttsx3
import speech_recognition as sr
import datetime
import os
import requests
import wikipedia
import webbrowser
import pywhatkit as kit
import pygetwindow as gw
import aiprocess as ap
import AppOpener
import gemini_ai
import time
import io
import sys
import winsound

engine = pyttsx3.init("sapi5")
commands = ["open", "shutdown", "ip address of my device", "minimise window","close window","maximise window","go to","search on google","search on wikipedia",
            "current temperature","send message","ai mode","sleep","current date","restart","play video on youtube","help","close","send message","current time","exit"]
# Text to speak function
def set_speech_rate(rate):
    engine.setProperty('rate', rate)

def speak(text,speed=200):
    set_speech_rate(speed)
    engine.say(text)
    engine.runAndWait()

# Voice to text
def takecmd():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.8
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)  # Increased timeout
            print("Recognizing...")
            query = r.recognize_google(audio)
            print(query)
        except sr.WaitTimeoutError:
            speak("Listening timed out. Please try again.")
            return "none"
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
            return "none"
        except sr.RequestError:
            speak("Sorry, there was an issue with the request.")
            return "none"
        return query.lower()

def wish():
    now = int(datetime.datetime.now().hour)
    if 5 <= now < 12:
        speak("Good Morning")
    elif 12 <= now < 17:
        speak("Good Afternoon")
    else:
        speak("Good Evening")

def wiki(query):
    speak("Searching Wikipedia")
    try: 
        result=wikipedia.summary(query,sentences=2)
        print("According to wikipedia")
        speak("According to wikipedia")
        print(f"{result} for more information go to wikipedia.com")
        speak(f"{result} for more information go to wikipedia.com")
        
    except Exception as e:
        print("Something went wrong ",e)
        speak("Something went wrong")
    

def google_search(query):
    try:
        print(f"{query} Searching from google")
        speak(f"{query} Searching from google")
        kit.search(query)
    except Exception as e:
        print("Something went wrong ",e)
        speak("Something went wrong")


def ytvideo(video_name):
    try:
        print(f"{video_name} is going to play on YouTube")
        speak(f"{video_name} is going to play on YouTube")
        kit.playonyt(video_name)
    except Exception as e:
        print("Something went wrong ",e)
        speak("Something went wrong")

def temperature(city):
    api_key="e1d983b04e077c29b80e04718e8ac714"
    url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    r=requests.get(url)
    wdata=r.json()
    if "main" in wdata:
        temp_k = wdata['main']['temp']
        temp_c = temp_k - 273.15
        print(f"Current temperature in {city} is {temp_c:.2f}° C")
        speak(f"Current temperature in {city} is {temp_c:.2f}° C")
    else:
        print("Please give me valid City name")
        speak("Please give me valid City name")


def send_message(message):
    speak("Please provide the phone number to which I should send messages.")
    number=input("Enter phone no. ")
    while (len(number)<=9):
        speak(f"The provided phone number have only {len(number)} digits Please tell me again")
        number=input("Enter phone no. ")
    
    speak("This process may take a few seconds and during this process i can't do any other work")
    now = datetime.datetime.now()
    future_time = now + datetime.timedelta(minutes=2)
    time_hour = future_time.hour
    time_minute = future_time.minute

    country_code="+91"
    number=f"{country_code}{number}"
    kit.sendwhatmsg(number, message, time_hour, time_minute)

def open_apps(app_name):
    
    try:
        print(f"Openning {app_name}")
        speak(f"Openning {app_name}")
        AppOpener.open(app_name,match_closest=True)
    except Exception as e:
        print("Something went wrong", e)
        speak("Something went wrong")
        
        
        

def process_airesponse(response):
    for command in commands:
        if response.startswith(command): 
            param = response[len(command):].strip()  
            return command,param
    return None,None

def restart():
    print("Are you sure you want to restart your PC? (yes/no)")
    speak("Are you sure you want to restart your PC? yes or no")
    user=takecmd().lower()
    
    try:
        if "yes" in user:
            speak("Your pc is restarting")
            os.system("shutdown /r /t 0")
        else:
            speak("Restart canceled")
    except Exception as e:
        print("Something went wrong",e)
        speak("Something went wrong")
    

def help_function():
    help_text = (
        "Welcome to the Command Assistant!, My name is Nova, Here are some commands you can use:\n\n"
        "1. **Go to <website name>**\n"
        "   - Example: 'Go to amazon' or 'Go to google'\n"
        "   - Opens the website in your browser. The assistant will append '.com' to the website name if not specified.\n\n"
        
        "2. **Search on Google <query>**\n"
        "   - Example: 'Search on Google Python tutorials'\n"
        "   - Performs a Google search with the specified query.\n\n"
        
        "3. **Open <app/system tool>**\n"
        "   - Example: 'Open calculator' or 'Open notepad'\n"
        "   - Opens the specified application or system tool.\n\n"
        
        "4. **IP address of my device**\n"
        "   - Example: 'IP address of my device'\n"
        "   - Provides the IP address of your device.\n\n"
        
        "5. **Search on Wikipedia <topic>**\n"
        "   - Example: 'Search on Wikipedia Python programming'\n"
        "   - Searches Wikipedia for the specified topic and reads a summary.\n\n"
        
        "6. **Send message**\n"
        "   - Example: 'Send message'\n"
        "   - Prompts you to provide a phone number and a message to send via WhatsApp.\n\n"
        
        "7. **Current temperature <city_name>**\n"
        "   - Example: 'Current temperature in New York'\n"
        "   - Provides the current temperature for the specified city.\n\n"
        
        "8. **Play video on YouTube <video_name>**\n"
        "   - Example: 'Play video on YouTube Python tutorial'\n"
        "   - Searches for and plays the specified video on YouTube.\n\n"
        
        "9. **Current time**\n"
        "   - Example: 'Current time'\n"
        "   - Provides the current time.\n\n"
        
        "10. **AI mode <query>**\n"
        "    - Example: 'AI mode What is the weather like?'\n"
        "    - Interacts with the AI model to process your query in AI mode.\n\n"
        
        "11. **Shutdown**\n"
        "    - Example: 'Shutdown'\n"
        "    - Shuts down the computer.\n\n"
        
        "12. **Restart**\n"
        "    - Example: 'Restart'\n"
        "    - Restarts the computer.\n\n"
        
        "13. **Sleep**\n"
        "    - Example: 'Sleep'\n"
        "    - Puts the computer into sleep mode.\n\n"
        
        "14. **Minimise window**\n"
        "    - Example: 'Minimise window'\n"
        "    - Minimizes the currently active window.\n\n"
        
        "15. **Maximise window**\n"
        "    - Example: 'Maximise window'\n"
        "    - Maximizes the currently active window.\n\n"
        
        "16. **Close window**\n"
        "    - Example: 'Close window'\n"
        "    - Closes the currently active window.\n\n"
        
        "17. **No thanks exit**\n"
        "    - Example: 'No thanks exit'\n"
        "    - Exits the assistant.\n\n"
        
        "If you need help with a specific command or have any questions, just ask!"
    )
    print(help_text)
    speak(help_text)
          
  

def sleep():
    print("Are you sure you want to Sleep your PC? (yes/no)")
    speak("Are you sure you want to Sleep your PC? yes or no")
    user=takecmd().lower()
    
    try:
        if "yes" in user:
            speak("Your pc is go to sleep mode")
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        else:
            print("Sleep canceled")
            speak("Sleep canceled")
    except Exception as e:
        print("Something went wrong",e)
        speak("Something went wrong")
        
        
def ip_address():
    
    try:
        ip=requests.get("https://api.ipify.org").text
        print(ip)
        speak(f"Your IP Address is {ip}")
    except Exception as e:
        print("Something went wrong",e)
        speak("Something went wrong")

def minimize():
    
    try:
        window = gw.getActiveWindow()
        speak("current window is minimizing")
        if window:
            window.minimize()
        else:
            print("Current window can't recognize")
    except Exception as e:
        print("Something went wrong",e)
        speak("Something went wrong")
        
        
def maximize():
    
    try:
        window = gw.getActiveWindow()
        if window:
            print("Current Window is Maximizing")
            speak("Current Window is Maximizing")
            window.maximize()
        else:
            print("Current window can't recognize")
            speak("Current window can't recognoze")
    except Exception as e:
        print("Something went wrong",e)
        speak("Something went wrong")
        
        
        
def closewindow():
    
    try:
        window = gw.getActiveWindow()
        if window:
            print("Current Window is Closing")
            speak("Current Window is Closing")
            window.close()
        else:
            print("Current can't recognize")
            speak("Current can't recognize")
    except Exception as e:
        print("Something went wrong",e)
        speak("Something went wrong")
        
def sleep():
    print("Are you sure you want to Sleep your PC? (yes/no)")
    speak("Are you sure you want to Sleep your PC? yes or no")
    user=takecmd().lower()
    
    try:
        if "yes" in user:
            print("Your pc is go to sleep mode")
            speak("Your pc is go to sleep mode")
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        else:
            print("Sleep canceled")
            speak("Sleep canceled")
    except Exception as e:
        print("Sleep canceled ",e)
        speak("Sleep canceled")

def open_website(web_name):
    try:
        webbrowser.open(f"http://{web_name}")
        print(f"Opening {web_name} in your browser...")
        speak(f"Opening {web_name} in your browser...")
    except Exception as e:
        print(f"Failed to open {web_name}. Error: {e}")
        speak(f"Failed to open {web_name}")
        
        
def close_apps(app_name):
    try:
        captured_output = io.StringIO()
        sys.stdout = captured_output
        speak(f"Closing {app_name}")
        AppOpener.close(app_name)
        sys.stdout = sys.__stdout__
        result = captured_output.getvalue().strip()
        
        if "not running" in result:
            print("Sorry I can't close the app due to security concern and permission issues, If the app you want to close is your current app then try again and say close the current window")
            speak("Sorry I can't close the app due to security concern and permission issues, If the app you want to close is your current window, then try again and say close the current window",speed=150)
    except Exception as e:
        print("Something went wrong ",e)
        speak("Something went wrong")

def ai_mode(query):
    gemini_ai.aispeechmode(query)

def current_time():
    time = datetime.datetime.now().strftime("%I:%M %p") 
    print(time)
    speak(f"The current time is {time}")

def set_alarms(alarm_time):
    pass
    

def current_date():
    date=date=datetime.datetime.now().strftime("%B %d, %Y")
    print(f"Today's date is {date}")
    speak(f"Today's date is {date}")

def unknown_command():
    pass

command_actions={
    "open":open_apps,
    "search on wikipedia":wiki,
    "sleep":sleep,
    "minimise window":minimize,
    "maximize":maximize,
    "close window":closewindow,
    "go to":open_website,
    "search on google":google_search,
    "ip address of my device":ip_address,
    "play video on youtube":ytvideo,
    "restart":restart,
    "sleep":sleep,
    "current date":current_date,
    "send message":send_message,
    "current temperature":temperature,
    "current time":current_time,
    "ai mode":ai_mode,
    "help":help_function,
    "close":close_apps,
    "exit":exit
}

if __name__ == "__main__":
    wish()
    speak("How can I help you, Sir?")
    
    while True:
        
        query = takecmd().lower()
        if query=="none":
            continue
        query=ap.processcmd(query)
        command,param=process_airesponse(query)
        
        try:
            if command:
                action = command_actions.get(command, unknown_command)
                if param:
                    action(param)  # If there is a parameter, pass it to the function
                else:
                    action()
        except Exception as e:
            print(e)
        
        
        time.sleep(5)
        speak("Sir, Do you have any other work")
    
    
        
    
 
    
    
    
    
        
        