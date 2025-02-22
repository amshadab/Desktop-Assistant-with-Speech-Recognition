import sys,os,threading
import time,re,datetime
from PyQt5.QtWidgets import QApplication, QWidget,QMenu, QVBoxLayout,QAction, QHBoxLayout,QStackedWidget, QLabel, QPushButton, QTextEdit,  QScrollArea, QFrame
from PyQt5.QtCore import Qt, QSize, QThread, pyqtSignal,QPropertyAnimation,QEvent
from PyQt5.QtGui import QIcon,QMovie,QPixmap
from PyQt5 import QtGui
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
import ctypes
from CustomMessageBox import *
from backend import *
import backend as b
import database as db
BtnTextFont = '25px'
toggleMic = True
themeColor = '#0085FF'
speaking = True
prompt = "none"
thread = True
btnStyle = f"background-color: #07151E; font-size: {BtnTextFont}; color: {themeColor}; padding: 5px; border-radius:30px; border:5px solid {themeColor}"
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))
movie = None
ret = None

class PopupWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.initUI()

    def initUI(self):
        self.setWindowTitle('NOVA')
        self.setStyleSheet("background-color: #07151E; color: #ffffff;")
        self.setGeometry(0, 0, 300, 300)
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint | Qt.WindowStaysOnTopHint)
        btnStyle = f"background-color: #07151E; font-size: {BtnTextFont}; color: {themeColor}; padding: 10px; border-radius:15px; border:5px solid {themeColor}"

        # Main vertical layout
        layout = QVBoxLayout()
        
        # Top section with centered mic button
        mic_container = QHBoxLayout()
        mic_container.addStretch()
        self.mic_button = self.main_window.create_mic_button()
        self.mic_button.clicked.connect(self.main_window.micon)
        mic_container.addWidget(self.mic_button)
        mic_container.addStretch()
        
        # Create controls
        self.show_main_button = QPushButton(self)
        self.show_main_button.setIcon(QIcon('icons/popup_open.png'))
        self.show_main_button.setIconSize(QSize(40, 40))
        self.show_main_button.clicked.connect(self.show_main_window)
        self.show_main_button.setStyleSheet(btnStyle)
        self.show_main_button.setFixedSize(60, 60)

        self.state = QLabel("")
        self.state.setStyleSheet(f"""
                        color:{themeColor};
                        font-size: 30px;
                        font-weight: bold;
                    """)
        self.state.setFixedWidth(200)
        
        self.mute_button = QPushButton()
        self.mute_button.setStyleSheet(btnStyle)
        self.mute_button.setIcon(QIcon('icons/mute.png'))
        self.mute_button.setIconSize(QSize(40, 40))
        self.mute_button.setFixedSize(60, 60)

        # Bottom section with controls
        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.state, alignment=Qt.AlignCenter)
        bottom_layout.addWidget(self.mute_button)
        bottom_layout.addWidget(self.show_main_button)

        # Add all layouts to main layout
        layout.addLayout(mic_container)
        layout.addLayout(bottom_layout, Qt.AlignRight)

        self.setLayout(layout)

    def show_main_window(self):
        self.hide()
        self.main_window.show_main_interface()

class ChatWindow(QWidget,QThread):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        # Scrollable area for chat bubbles
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("background-color: #0F1C25; border: none;")
        self.message_history = []


        # Widget to hold the layout of chat bubbles
        self.chat_container = QWidget()
        
        self.chat_layout = QVBoxLayout(self.chat_container)
        print(self.maximumWidth())
        self.chat_layout.setContentsMargins(int(self.maximumWidth()*0.00002),0,int(self.maximumWidth()*0.00002),0)
        self.chat_layout.setAlignment(Qt.AlignTop)

        self.scroll_area.setWidget(self.chat_container)

        layout.addWidget(self.scroll_area)


        # Input area

        self.input_layout = QHBoxLayout()
        self.input_layout.addStretch()
        self.message_input = QTextEdit()
        self.message_input.setPlaceholderText("Enter Your Prompt")
        self.message_input.setStyleSheet(f"background-color: #07151E; font-size: {BtnTextFont}; color: #6CCAFF; padding: 5px; border-radius:20px; border:5px solid {themeColor}")
        self.message_input.setFixedSize(600,100)
        self.input_layout.addWidget(self.message_input)

        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)
        self.send_button.setFixedWidth(100)
        self.send_button.setStyleSheet(f"background-color: #07151E; font-size: {BtnTextFont}; color: {themeColor}; padding: 5px; border-radius:20px; border:5px solid {themeColor}")
        self.input_layout.addWidget(self.send_button)
        self.input_layout.addStretch()
    
        layout.addLayout(self.input_layout)
        self.setLayout(layout)
        # Styling
        self.setStyleSheet("""
            QTextEdit {
                background-color: #07151E;
                color: white;
                border: 1px solid #ccc;
                border-radius: 20px;
                font-size: 20px;
                padding: 5px;
            }
            QPushButton {
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 20px;
                padding: 10px;
                background-color: #07151E;
            }
            QPushButton:hover {
                background-color: #128C7E;
            }
        """)
        scrollbar = self.scroll_area.verticalScrollBar()
        animation = QPropertyAnimation(scrollbar, b"value")
        animation.setDuration(500)  # 500ms animation
        animation.setStartValue(scrollbar.value())
        animation.setEndValue(scrollbar.maximum())
        animation.start()

    def send_message(self):
        global prompt
        message = self.message_input.toPlainText().strip()
        if message:
            prompt = message
            self.message_input.clear()

    def add_message(self, message, is_sent=False):
        # Create a bubble widget for the message
        bubble_widget = self.create_bubble_widget(message, is_sent)
        self.chat_layout.addWidget(bubble_widget)
        # print(bubble_widget.height())
        self.scroll_area.verticalScrollBar().setSliderPosition(self.scroll_area.verticalScrollBar().maximum()+(bubble_widget.height()*20))
    
    def get_last_message(self):
        if self.message_history:
            return self.message_history[-1]  # Return last message from history list
        return ""

    

    

    def create_bubble_widget(self, message, is_sent):
        # Create a QWidget to act as the message bubble
        bubble_frame = QFrame()
        bubble_layout = QHBoxLayout(bubble_frame)
        if message.startswith("You: "): 
            is_sent= True
            self.message_history.append(message.replace("You: ",""))


        
        bubble = QLabel(message)
        bubble.setTextInteractionFlags(Qt.TextSelectableByMouse)

        bubble.setWordWrap(True)
        if not is_sent:
            bubble.setFixedWidth(int(self.scroll_area.width()*0.5))
        bubble.setStyleSheet(f"""
        background-color: {themeColor if is_sent else '#0A1E2A'};
        color: white;
        border-radius: 10px;
        padding: {"10px" if is_sent else "0px"};
        font-size:{BtnTextFont}
        """)  
  

        if is_sent:
            bubble_layout.addStretch()  # Right-align sent messages
            bubble_layout.addWidget(bubble)
        else:
            bubble_layout.addWidget(bubble)  # Left-align received messages
            bubble_layout.addStretch()

        bubble_layout.setContentsMargins(10, 5, 10, 5)
        return bubble_frame
    def delete_conversation(self):
        # Delete all widgets inside the chat_layout
        db.delete_conversation()
        while self.chat_layout.count():
            item = self.chat_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()  # Safe deletion

        # Optionally, force a UI update
        self.chat_container.update()



# NovaInterface with chat integration
class NovaInterface(QWidget):
    def __init__(self):
        global movie
        movie = QMovie("icons/mic_ani.gif")
        movie.speed = -500
        global in_custom_message_box
        self.state = QLabel("")
        self.state.setStyleSheet(f"""
                        color:{themeColor};
                        font-size: 30px;
                        font-weight: bold;
                    """)
        super().__init__()
        self.chat_window = ChatWindow()
        self.initUI()
        
        # demo(self)
        state = QLabel("Listening...")
        self.chat_window.message_input.installEventFilter(self)
        
        
        state.setStyleSheet(f"""
                        color:{themeColor};
                        font-size: 50px;
                        font-weight: bold;
                    """)
    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            if self.isMinimized() and not in_custom_message_box:
                print("Window minimized")
                self.show_popup()
            elif self.isMaximized():
                print("Window maximized")
            else:
                print("Window restored")

        if event.type() == QEvent.ActivationChange:
            if not self.isActiveWindow() and not in_custom_message_box:
                print("Window lost focus")
                self.show_popup()
            else:
                print("Window gained focus")

        super().changeEvent(event)
    def initUI(self):
        self.setWindowTitle('NOVA')
        self.setStyleSheet("background-color: #0F1C25; color: #ffffff;")
        self.popup = PopupWindow(self)
        self.setMinimumSize(1000, 1000)

        # Main layout
        self.main_layout = QVBoxLayout()

        # Top section with grid layout
        top_layout = QHBoxLayout()

        # SK logo (top-left corner)
        self.sk_label = QPushButton("U")
        self.sk_label.setStyleSheet(f"background-color: #07151E; color: {themeColor}; font-size:{BtnTextFont};  padding: 5px; border-radius: 20px; border:5px solid {themeColor};")
        self.sk_label.setFixedSize(50, 50)
        self.sk_label.clicked.connect(self.show_user_menu)

        # Create menu
        self.user_menu = QMenu(self)
        self.user_menu.setStyleSheet("""
            QMenu {
                background-color: #07151E;
                border: 2px solid #0085FF;    /* Changed border color to red */
                border-radius: 5px;
            }
            QMenu::item {
                padding: 10px 30px;      /* Reduced padding to make button smaller */
                color: white;              /* Text color red */
                font-size: 16px;         /* Slightly smaller font */
                font-weight: bold;
            }
            QMenu::item:selected {
                background-color:  #0085FF;    /* Changed hover background to red */
                color: white;
            }
            QMenu::separator {
                height: 2px;
                background-color: #0085FF;
                margin: 5px 15px;
            }
        """)

        # Add logout action
        logout_action = QAction('Logout', self)
        logout_action.triggered.connect(self.logout)
        self.user_menu.addAction(logout_action)

        separator = self.user_menu.addSeparator()
        separator.setObjectName("blueMenuSeparator")

        delete_action = QAction('Delete', self)
        delete_action.triggered.connect(self.delete_account)
        self.user_menu.addAction(delete_action)

        # NOVA label (centered)
        self.nova_icon = QLabel()
        img = QPixmap('icons/nova_no_bg.png')
        self.nova_icon.setPixmap(img)
        self.nova_icon.setStyleSheet("background-color: white; border-radius: 30px; padding: 5px;")
        nova_label = QLabel("NOVA")
        
        nova_label.setStyleSheet(f"color: {themeColor}; font-size: 30px; font-weight: bold;")

        delete_button = QPushButton()
        delete_button.setStyleSheet(f"background-color: #07151E; font-size: {BtnTextFont}; color: {themeColor}; padding: 5px; border-radius:20px; border:5px solid {themeColor}")
        delete_button.setIcon(QIcon('icons/delete.png'))
        delete_button.setIconSize(QSize(30, 30))
        delete_button.clicked.connect(self.chat_window.delete_conversation)

        # Add widgets to the top layout
        top_layout.addWidget(self.nova_icon)
        top_layout.addWidget(nova_label)
        top_layout.addStretch()
        top_layout.addStretch()
        top_layout.addWidget(delete_button)
        top_layout.addWidget(self.sk_label)  


        # Stretch settings for center and left side
        

        self.mic_button = self.create_mic_button()       
        self.mic_button.clicked.connect(self.micon)
        self.mic_button.setStyleSheet("border: none;")
        # Bottom but.bottom_layout
        self.bottom_layout = QHBoxLayout()
        
        # delete_button.setBackgroundRole(Qt.black)

        self.text_mode_button = QPushButton()
        self.text_mode_button.setStyleSheet(btnStyle)
        self.text_mode_button.setIcon(QIcon('icons/keyboard.png'))
        self.text_mode_button.setIconSize(QSize(50, 50))
        self.text_mode_button.clicked.connect(self.toggle_input_mode)
        # self.text_mode_button.setBackgroundRole(Qt.black)

        self.mute_button = QPushButton()
        self.mute_button.setStyleSheet(btnStyle)
        self.mute_button.setIcon(QIcon('icons/mute.png'))
        self.mute_button.setIconSize(QSize(50, 50))
        self.mute_button.clicked.connect(self.toggle_mute)
        # self.mute_button.setBackgroundRole(Qt.black)

        self.float_window_button = QPushButton()
        self.float_window_button.setStyleSheet(btnStyle)
        self.float_window_button.setIcon(QIcon('icons/popup_open.png'))
        self.float_window_button.setIconSize(QSize(50, 50))
        self.float_window_button.clicked.connect(self.show_popup)
        # self.float_window_button.setBackgroundRole(Qt.black)

        self.bottom_layout.addStretch()
        self.bottom_layout.addWidget(self.text_mode_button)
        self.bottom_layout.addWidget(self.mic_button)
        # self.bottom_layout.addLayout(self.chat_window.input_layout)
        self.bottom_layout.addWidget(self.mute_button)
        self.bottom_layout.addWidget(self.float_window_button)
        self.bottom_layout.addStretch()

        self.bottom = QWidget()
        self.bottom.setLayout(self.bottom_layout)
        self.bottom.setStyleSheet(f"border: 5px solid {themeColor}; border-radius: 40px; background-color: #07151E; padding: 0px;")
        self.b = QHBoxLayout()
        self.b.addStretch()
        self.b.addWidget(self.bottom)
        self.b.addStretch()

        # Add all sections to the main layout
        self.main_layout.addLayout(top_layout)
        # Add the chat window in the middle
        self.main_layout.addWidget(self.chat_window)
        self.main_layout.addLayout(self.b)
        self.main_layout.addWidget(self.state,alignment=Qt.AlignCenter)
        
        self.setLayout(self.main_layout)

        
        self.chat_window.message_input.hide()
        self.chat_window.send_button.hide()

        self.stacked_widget = QStackedWidget()
        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_layout)
        self.stacked_widget.addWidget(self.main_widget)

        self.popup_widget = QWidget()
        popup_layout = QVBoxLayout()
        self.popup_mic_button = self.create_mic_button()
        self.popup_mic_button.clicked.connect(self.micon)
        popup_layout.addWidget(self.popup_mic_button)
        self.popup_widget.setLayout(popup_layout)
        self.stacked_widget.addWidget(self.popup_widget)
        self.popup.mute_button.clicked.connect(self.toggle_mute)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stacked_widget)
        self.setLayout(main_layout)
    


    
    def logout(self):
        try:
            # Delete the user_config.txt file
            if os.path.exists('user_config.txt'):
                os.remove('user_config.txt')
            
            # Close the current window
            self.close()
            
            # Start the signup_login.py script
            python_executable = sys.executable
            os.execl(python_executable, python_executable, "signup_login.py")
        
        except Exception as e:
            print(f"Error during logout: {e}")


    def delete_account(self):
        global in_custom_message_box
        try:
            in_custom_message_box = True
            result = CustomMessageBox.show_message(text="Are you sure you want to delete your account?", B1="Yes", B2="No")
        
            if result == 1:  # User clicked Yes
                db.delete_account() 
                if os.path.exists('user_config.txt'):
                    os.remove('user_config.txt')
                
                self.close()
                python_executable = sys.executable
                os.execl(python_executable, python_executable, "signup_login.py")
        
        except Exception as e:
            print(f"Error during account deletion: {e}")
        finally:
            in_custom_message_box = False

    def show_popup(self):
        self.is_popup_mode = True
        self.stacked_widget.setCurrentWidget(self.popup_widget)
        self.setGeometry(0, 0, 300, 300)  # Adjust size for popup mode
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)
        self.show()

    def show_main_interface(self):
        self.is_popup_mode = False
        self.stacked_widget.setCurrentWidget(self.main_widget)
        self.showMaximized()  # Show in full screen
        self.setWindowFlags(Qt.Window)
        self.showMaximized()

    def toggle_input_mode(self):
        global toggleMic
        # Toggle visibility of the text field and microphone button
        if self.chat_window.message_input.isVisible():
            self.chat_window.message_input.hide()
            self.state.show()
            self.chat_window.send_button.hide()
            self.mic_button.show()
            self.text_mode_button.setIcon(QIcon('icons/keyboard.png'))
            toggleMic = True
            speak("mic mode")

        else:
            self.chat_window.message_input.show()
            self.text_mode_button.setIcon(QIcon('icons/mic.png'))
            self.chat_window.send_button.show()
            self.state.hide()
            self.mic_button.hide()
            toggleMic = False
            speak("input mode")


    def create_mic_button(self):
        global movie
        mic_size = 200
        mic_button = QPushButton(self)
        mic_button.setFixedSize(mic_size , mic_size)

        mic_label = QLabel(mic_button)
        mic_label.setGeometry(0, 0, mic_size , mic_size)

        
        mic_label.setMovie(movie)
        mic_label.setScaledContents(True)
        # movie.finished.connect(movie.start)
        movie.start()
        # movie.stop()
        return mic_button
        


    def show_popup(self):
        global toggleMic
        if not toggleMic:
            self.toggle_input_mode()
        self.hide()
        self.popup.show()
    
    def set_name(self,text):
        self.sk_label.setText(text)
        
    
    def eventFilter(self, obj, event):
        if obj == self.chat_window.message_input and event.type() == event.KeyPress:
            if event.key() == Qt.Key_Return and not event.modifiers():
                # Only send the message if it's plain "Enter" key
                if not toggleMic:
                    self.chat_window.send_message()
                return True
            elif event.key() == Qt.Key_Return and event.modifiers() == Qt.ShiftModifier:
                # Allow line breaks with Shift + Enter
                self.chat_window.message_input.insertPlainText("\n")
                return True
            elif event.key() == Qt.Key_Up:  # Handle Up Arrow Key
                # Retrieve the last message from history (assuming self.last_message stores it)
                last_message = self.chat_window.get_last_message()  # Implement this method
                if last_message:
                    self.chat_window.message_input.setPlainText(last_message)
                    self.chat_window.message_input.moveCursor(QtGui.QTextCursor.End)  # Move cursor to end
                return True  # Stop further processing of the event

        return super().eventFilter(obj, event)



    
    def state_(self,text):
        self.popup.state.setText(text)
        self.state.setText(text)

    def micon(self):
        global movie
        global thread

        if not thread:
            thread_function(self)
            thread = True
        if b.mic_off: 
            b.mic_off = False
            movie.start()

        else: 
            b.mic_off = True
            movie.stop()
            movie.jumpToFrame(0)

        

        print("b.mic_off:"+ str(b.mic_off))

    def toggle_mute(self):
        global speaking

        # Get the current mute state
        # is_muted = volume.GetMute()
        # volume.SetMute(not is_muted, None)
        speaking = not speaking

        if speaking:
            self.mute_button.setIcon(QIcon('icons/mute.png'))
            self.popup.mute_button.setIcon(QIcon('icons/mute.png'))

        else:
            self.mute_button.setIcon(QIcon('icons/unmute.png'))
            self.popup.mute_button.setIcon(QIcon('icons/unmute.png'))
            
        # Toggle the mute state
        print(f"Muted: {not speaking}")

    # Toggle mute/unmute
    def sleep_(self):
        global in_custom_message_box
        in_custom_message_box = True

        result=CustomMessageBox.show_message(self,"Are you sure you want to Sleep your pc")

        in_custom_message_box = False
        
        
        try:
            if result==1:
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
            else:
                ret= "Sleep canceled"
        except Exception as e:
            ret= f"Something Went wrong {e}"
        self.chat_window.add_message(ret)
        speak(ret)       
        
    def shutdown_(self):
        global in_custom_message_box
        in_custom_message_box = True
        
        result =  CustomMessageBox.show_message(self,"Are you sure you want to shutdown your pc")
        in_custom_message_box = False
        
        try:
            if result==1:
                os.system("shutdown /s /t 0")
            else:
                ret= "Shutdown Cancelled"
        except Exception as e:
            ret= f"Something Went wrong {e}"
        self.chat_window.add_message(ret)
        speak(ret)
        
    def restart_(self):
        global in_custom_message_box
        in_custom_message_box = True
        result=CustomMessageBox.show_message(self,"Are you sure you want to Resatart your pc")
        in_custom_message_box = False
        try:
            if result == 1:
                os.system("shutdown /r /t 0")
            else:
                ret= "Restart canceled"
        except Exception as e:
            ret= f"Something Went wrong {e}"
        self.chat_window.add_message(ret)
        speak(ret)
    def show_user_menu(self):
        # Show the menu below the SK label
        self.user_menu.exec_(self.sk_label.mapToGlobal(self.sk_label.rect().bottomLeft()))
    def send_message(self,message):
        speak("Please provide the phone number to which I should send messages.")
        number = CustomInputBox.show_input_dialog("Please provide the phone number to which I should send messages")
        while (len(number)<=9):
            number = CustomInputBox.show_input_dialog(f"The provided phone number have only {len(number)} digits Please Enter again")

        speak("This process may take a few seconds")
        now = datetime.now()
        country_code="+91"
        number=f"{country_code}{number}"
        threading.Thread(target=kit.sendwhatmsg, args=(number, message, now.hour, now.minute+1,1)).start()
        self.chat_window.add_message("Message sent to "+number+"\nwill be delivered in a minute")
        time.sleep(1)

    
#     result = CustomMessageBox.show_message(self,"Welcome to NOVA\n\nNOVA is an AI assistant which can control your desktop based on your command.")
    



class ChatThread(QThread):
    message_received = pyqtSignal(str)
    micon = pyqtSignal()
    restart = pyqtSignal()
    shutdown = pyqtSignal()
    sleep = pyqtSignal()
    state = pyqtSignal(str)
    name = pyqtSignal(str)
    send_message = pyqtSignal(str)
    

    def __init__(self,obj):
        super().__init__()
    def run(self):
     flag = True
     global prompt
     global ret
     global thread
     global speaking
     thread = True
     try:
        self.name.emit(db.get_user_initials())
        conversations = db.get_conversations()
        if conversations :
            
            for conv in conversations:
            # Get the encrypted data as a string
                encrypted_user_input = conv.to_dict().get('user_input')
                encrypted_assistant_response = conv.to_dict().get('assistant_response')
                try:
                # Decrypt the data
                    user_input = db.decrypt_data(encrypted_user_input.encode('utf-8')) if isinstance(encrypted_user_input, str) else db.decrypt_data(encrypted_user_input)
                    assistant_response = db.decrypt_data(encrypted_assistant_response.encode('utf-8')) if isinstance(encrypted_assistant_response, str) else db.decrypt_data(encrypted_assistant_response)
                    self.message_received.emit(user_input)
                    self.message_received.emit(assistant_response)
                except Exception as decryption_error:
                    print(f"Decryption error for conversation ID {conv.id}: {decryption_error}")


        # Simulate receiving a message
        wish()
        self.state.emit("How can I help you, Sir?")
        speak("How can I help you, Sir?")
    
        while True:    
            if flag:
                flag= False
            
            self.state.emit("Listening...")

            if toggleMic and not b.mic_off:
                takecmd_ = takecmd()
                self.state.emit("Recognizing...")
                query = recoginze(takecmd_).lower()
            else:
                time.sleep(0.1)
                query = prompt
                prompt = "none"
            if query=="none":
                continue 
            elif toggleMic and not b.mic_off:
                self.micon.emit()
                flag =  True
            self.state.emit("Thinking...")
            
            self.message_received.emit("You: "+query)
            result = input_from_gui(query,self).replace("*"," ")
            if result =="restart_": 
                self.restart.emit()
                result = "restarting your computer"

            if result =="shutdown_": 
                self.shutdown.emit()
                result = "shutdowning your computer"


            if result =="sleep_": 
                self.sleep.emit()
                result = "sleeping your computer"

            if result.__contains__("sending  message"): 
                self.send_message.emit(result.replace("sending  message","",1))
                



                         
                # result = "message send" 

            
            db.save_conversation("You: "+ query,result)
            for r in result.split("\n"):
                self.message_received.emit(r)
                time.sleep(0.05)
                
            self.state.emit("Speaking...")
            

            delimiters = r"[\n,.:!?;]"  # Regular expression for multiple delimiters

            for rt in re.split(delimiters, result):  # Split by multiple delimiters
                rt = rt.strip()  # Remove leading/trailing spaces
                if rt:  # Ignore empty strings from splitting
                    if (not b.mic_off ) or not speaking:
                        self.micon.emit()
                        print("mic off")
                        break
                    speak(rt)

            

            prompt ="none"
            if result.__contains__("Goodbye! "): 
                self.state.emit("")
                thread = False
                break
 
            
            if toggleMic:
                self.micon.emit()
            time.sleep(1)
            if toggleMic:
                speak("Sir, Do you have any other work")
          
     except Exception as e:
            print(e)
        

    
def thread_function(obj):
    chat_thread.start()          

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)    
        ex = NovaInterface()
        ex.showMaximized()
        chat_thread = ChatThread(ex)
        chat_thread.message_received.connect(ex.chat_window.add_message)    
        chat_thread.micon.connect(ex.micon)
        chat_thread.restart.connect(ex.restart_)
        chat_thread.shutdown.connect(ex.shutdown_)
        chat_thread.sleep.connect(ex.sleep_)
        chat_thread.state.connect(ex.state_)
        chat_thread.name.connect(ex.set_name)
        chat_thread.send_message.connect(ex.send_message)
        chat_thread.start()
        sys.exit(app.exec_())
    except Exception as e:
        print(e)