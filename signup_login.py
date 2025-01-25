import subprocess
import webbrowser
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import sys,time
import database as db
from  CustomMessageBox import CustomMessageBox
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 650)
        MainWindow.setMinimumSize(QtCore.QSize(900, 650))
        MainWindow.setMaximumSize(QtCore.QSize(900, 650))
        MainWindow.setStyleSheet("background-color:#0F1C25;\n")
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # Stack of pages
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(100, 70, 681, 521))
        self.stackedWidget.setObjectName("stackedWidget")
        
        # Sign Up Page
        self.page_signup = QtWidgets.QWidget()
        self.page_signup.setObjectName("page_signup")
        self.setupSignupPage()
        self.stackedWidget.addWidget(self.page_signup)
        
        # Login Page
        self.page_login = QtWidgets.QWidget()
        self.page_login.setObjectName("page_login")
        self.setupLoginPage()
        self.stackedWidget.addWidget(self.page_login)
        
        # Initial Page
        self.stackedWidget.setCurrentWidget(self.page_signup)
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        # Event Listeners
        self.pushButton_signup.clicked.connect(self.signup)
        self.pushButton_login_page.clicked.connect(self.login)
        self.label_goto_signup.mousePressEvent = self.gotoSignupPage  # Clickable label
        self.label_goto_login.mousePressEvent = self.gotoLoginPage    # Clickable label

        # Implementing text box event handlers
        self.lineEdit_first_name.textChanged.connect(self.onTextChanged)
        self.lineEdit_last_name.textChanged.connect(self.onTextChanged)
        self.lineEdit_Email.textChanged.connect(self.onPasswordChanged)
        self.lineEdit_password.textChanged.connect(self.onPasswordChanged)
        self.lineEdit_confirm_password.textChanged.connect(self.onPasswordChanged)
        self.lineEdit_login_Email.textChanged.connect(self.onLoginChanged)
        
        # Implementing radio button event handlers
        self.radioButton_male.toggled.connect(self.onGenderSelected)
        self.radioButton_female.toggled.connect(self.onGenderSelected)

    def setupSignupPage(self):
        self.frame_signup = QtWidgets.QFrame(self.page_signup)
        self.frame_signup.setGeometry(QtCore.QRect(0, 0, 681, 521))
        self.frame_signup.setStyleSheet("border: 5px solid #0085FF;\n"
                                        "border-radius:10px;\n"
                                        "color: white;")
        self.frame_signup.setObjectName("frame_signup")
        
        self.lineEdit_first_name = QtWidgets.QLineEdit(self.frame_signup)
        self.lineEdit_first_name.setGeometry(QtCore.QRect(60, 80, 261, 41))
        self.lineEdit_first_name.setStyleSheet("border:no;\n"
                                               "border-bottom: 3px solid #0085FF;\n"
                                               " font-size: 20px;")
        self.lineEdit_first_name.setObjectName("lineEdit_first_name")
        
        self.lineEdit_last_name = QtWidgets.QLineEdit(self.frame_signup)
        self.lineEdit_last_name.setGeometry(QtCore.QRect(360, 80, 271, 41))
        self.lineEdit_last_name.setStyleSheet("border:no;\n"
                                              "border-bottom: 3px solid #0085FF;\n"
                                              " font-size: 20px;")
        self.lineEdit_last_name.setObjectName("lineEdit_last_name")
        
        self.lineEdit_Email = QtWidgets.QLineEdit(self.frame_signup)
        self.lineEdit_Email.setGeometry(QtCore.QRect(60, 170, 531, 41))
        self.lineEdit_Email.setStyleSheet("border:no;\n"
                                          "border-bottom: 3px solid #0085FF;\n"
                                          " font-size: 20px;")
        self.lineEdit_Email.setObjectName("lineEdit_Email")
        
        self.lineEdit_password = QtWidgets.QLineEdit(self.frame_signup)
        self.lineEdit_password.setGeometry(QtCore.QRect(60, 260, 531, 41))
        self.lineEdit_password.setStyleSheet("border:no;\n"
                                             "border-bottom: 3px solid #0085FF;\n"
                                             " font-size: 20px;")
        self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_password.setObjectName("lineEdit_password")

        self.label_warning = QtWidgets.QLabel(self.frame_signup)
        self.label_warning.setGeometry(QtCore.QRect(60, 390, 400, 20))
        self.label_warning.setStyleSheet("border:no;\n"
                                             "color:red;\n"
                                             " font-size: 15px;")
        
        
        self.lineEdit_confirm_password = QtWidgets.QLineEdit(self.frame_signup)
        self.lineEdit_confirm_password.setGeometry(QtCore.QRect(60, 340, 531, 41))
        self.lineEdit_confirm_password.setStyleSheet("border:no;\n"
                                                     "border-bottom: 3px solid #0085FF;\n"
                                                     " font-size: 20px;")
        self.lineEdit_confirm_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_confirm_password.setObjectName("lineEdit_confirm_password")
        
        self.radioButton_male = QtWidgets.QRadioButton(self.frame_signup)
        self.radioButton_male.setGeometry(QtCore.QRect(190, 410, 95, 20))
        self.radioButton_male.setStyleSheet("border:no;\n"
                                            "color:#0085FF;\n"
                                            " font-size: 20px;")
        self.radioButton_male.setChecked(True)
        self.radioButton_male.setObjectName("radioButton_male")
        
        self.radioButton_female = QtWidgets.QRadioButton(self.frame_signup)
        self.radioButton_female.setGeometry(QtCore.QRect(310, 410, 95, 20))
        self.radioButton_female.setStyleSheet("border:no;\n"
                                              "color:#0085FF;\n"
                                              " font-size: 20px;")
        self.radioButton_female.setObjectName("radioButton_female")
        
        self.pushButton_signup = QtWidgets.QPushButton(self.frame_signup)
        self.pushButton_signup.setGeometry(QtCore.QRect(230, 450, 171, 51))
        self.pushButton_signup.setStyleSheet("QPushButton#pushButton_signup{\n"
                                             " font-size: 20px;\n"
                                             "background-color:#0085FF;\n"
                                             "border-radius:20px;\n"
                                             "}\n"
                                             "\n"
                                             "QPushButton#pushButton_signup:hover{\n"
                                             "background-color:lightblue;\n"
                                             "color:#0085FF;\n"
                                             "}\n"
                                             "\n"
                                             "QPushButton#pushButton_signup:pressed{\n"
                                             "background-color:#0085FF;\n"
                                             "color:white;\n"
                                             "\n"
                                             "}")
        self.pushButton_signup.setObjectName("pushButton_signup")
        
        # "Already have an account?" Label
        self.label_goto_login = QtWidgets.QLabel(self.frame_signup)
        self.label_goto_login.setGeometry(QtCore.QRect(480, 450, 171, 51))
        self.label_goto_login.setStyleSheet("color: #0085FF;\n"
                                            "font-size: 16px;\n"
                                            "border: none;\n"
                                            "text-decoration: underline;")
        self.label_goto_login.setObjectName("label_goto_login")
    
    def setupLoginPage(self):
        self.frame_login = QtWidgets.QFrame(self.page_login)
        self.frame_login.setGeometry(QtCore.QRect(0, 0, 681, 521))
        self.frame_login.setStyleSheet("border: 5px solid #0085FF;\n"
                                       "border-radius:10px;\n"
                                       "color: white;")
        self.frame_login.setObjectName("frame_login")
        
        self.lineEdit_login_Email = QtWidgets.QLineEdit(self.frame_login)
        self.lineEdit_login_Email.setGeometry(QtCore.QRect(60, 140, 531, 41))
        self.lineEdit_login_Email.setStyleSheet("border:no;\n"
                                                "border-bottom: 3px solid #0085FF;\n"
                                                " font-size: 20px;")
        self.lineEdit_login_Email.setObjectName("lineEdit_login_Email")
        
        self.lineEdit_login_password = QtWidgets.QLineEdit(self.frame_login)
        self.lineEdit_login_password.setGeometry(QtCore.QRect(60, 230, 531, 41))
        self.lineEdit_login_password.setStyleSheet("border:no;\n"
                                                   "border-bottom: 3px solid #0085FF;\n"
                                                   " font-size: 20px;")
        self.lineEdit_login_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_login_password.setObjectName("lineEdit_login_password")
        
        self.label_warning_login = QtWidgets.QLabel(self.frame_login)
        self.label_warning_login.setGeometry(QtCore.QRect(60, 290, 400, 20))
        self.label_warning_login.setStyleSheet("border:no;\n"
                                             "color:red;\n"
                                             " font-size: 15px;")
        
        self.pushButton_login_page = QtWidgets.QPushButton(self.frame_login)
        self.pushButton_login_page.setGeometry(QtCore.QRect(230, 340, 171, 51))
        self.pushButton_login_page.setStyleSheet("QPushButton#pushButton_login_page{\n"
                                                 " font-size: 20px;\n"
                                                 "background-color:#0085FF;\n"
                                                 "border-radius:20px;\n"
                                                 "}\n"
                                                 "\n"
                                                 "QPushButton#pushButton_login_page:hover{\n"
                                                 "background-color:lightblue;\n"
                                                 "color:#0085FF;\n"
                                                 "}\n"
                                                 "\n"
                                                 "QPushButton#pushButton_login_page:pressed{\n"
                                                 "background-color:#0085FF;\n"
                                                 "color:white;\n"
                                                 "\n"
                                                 "}")
        self.pushButton_login_page.setObjectName("pushButton_login_page")
        
        # "Don't have an account?" Label
        self.label_goto_signup = QtWidgets.QLabel(self.frame_login)
        self.label_goto_signup.setGeometry(QtCore.QRect(480, 340, 171, 51))
        self.label_goto_signup.setStyleSheet("color: #0085FF;\n"
                                             "font-size: 16px;\n"
                                             "border: none;\n"
                                             "text-decoration: underline;")
        self.label_goto_signup.setObjectName("label_goto_signup")

    def onPasswordChanged(self):
        email = self.lineEdit_Email.text()
        password = self.lineEdit_password.text()
        confirm_password = self.lineEdit_confirm_password.text()

        if "@" not in email or ".com" not in email:
            self.label_warning.setText("Invalid email format. Please include '@' and '.com'.")
        elif password != confirm_password:
            self.label_warning.setText("Passwords do not match.")
        else:
            self.label_warning.clear()
            return email,confirm_password

    def onTextChanged(self):
        first_name = self.lineEdit_first_name.text()
        last_name = self.lineEdit_last_name.text()

        if not first_name or not last_name:
            self.label_warning.setText("First name and last name cannot be empty.")
        else:
            self.label_warning.clear()
            return first_name,last_name
        
        
            
        

    def onLoginChanged(self):
        login_email = self.lineEdit_login_Email.text()
        password = self.lineEdit_login_password.text()

        if "@" not in login_email or ".com" not in login_email:
            self.label_warning_login.setText("Invalid email format. Please include '@' and '.com'.")
        else:
            self.label_warning_login.clear()
            return login_email,password

    def onGenderSelected(self):
        if self.radioButton_male.isChecked():
            return "Male"
        elif self.radioButton_female.isChecked():
            return "Female"
        
    def signup(self):
        email,confirm_password=self.onPasswordChanged()
        first_name,last_name=self.onTextChanged()
        gender=self.onGenderSelected()
        
        result=db.sign_up(email,confirm_password,first_name,last_name,gender)
        
        if result==0:

            r= ( CustomMessageBox.show_message(text="""Welcome to NOVA 

NOVA is your intelligent desktop assistant, designed to seamlessly control your system based on your voice and text commands. Get ready to elevate your productivity and simplify your workflow with cutting-edge AI at your fingertips.

Let NOVA handle the details, so you can focus on what matters!
""",B1="learn More",B2="Launch Nova"))
            if r :
                print("User clicked learn more")
                webbrowser.open("https://github.com/Siddiq2772/NOVA--aixpalin-.git")
                QtWidgets.QApplication.quit()                 
                subprocess.Popen(["python", "maingui.py"]) 
            else:
                # os.system("python maingui.py")
                print("User clicked lauch nova")
                QtWidgets.QApplication.quit()                 
                subprocess.Popen(["python", "maingui.py"])  

        else:
            CustomMessageBox.show_message(text=result,B1='Try Again',B2='none')
            # QMessageBox.information(self.centralwidget, "Something Wrong", f"{result}")
            # print(result)

    def login(self):
        global launch_main
        login_email,password=self.onLoginChanged()
        result=db.log_in(login_email,password)
        
        
        if result==0:            
            r= ( CustomMessageBox.show_message(text="""✅ Login Successful! 

Hello, [Username]! You're now connected to NOVA. Let's get things done effortlessly.

""",B1="LAUNCH NOVA",B2='none'))
            if r :
                print("User clicked OK")
                QtWidgets.QApplication.quit()                 
                subprocess.Popen(["python", "maingui.py"])         
           
        else:
            CustomMessageBox.show_message(text=result,B1='Try Again',B2='none')
            # QMessageBox.information(self.centralwidget, "Something Wrong", f"{result}")

    def gotoSignupPage(self, event):
        self.stackedWidget.setCurrentWidget(self.page_signup)

    def gotoLoginPage(self, event):
        self.stackedWidget.setCurrentWidget(self.page_login)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        
        # Sign Up Page
        self.lineEdit_first_name.setPlaceholderText(_translate("MainWindow", "First Name"))
        self.lineEdit_last_name.setPlaceholderText(_translate("MainWindow", "Last Name"))
        self.lineEdit_Email.setPlaceholderText(_translate("MainWindow", "Email"))
        self.lineEdit_password.setPlaceholderText(_translate("MainWindow", "Password"))
        self.lineEdit_confirm_password.setPlaceholderText(_translate("MainWindow", "Confirm Password"))
        self.pushButton_signup.setText(_translate("MainWindow", "SIGN UP"))
        self.radioButton_male.setText(_translate("MainWindow", "Male"))
        self.radioButton_female.setText(_translate("MainWindow", "Female"))
        self.label_goto_login.setText(_translate("MainWindow", "Already have an account?"))
        
        # Login Page
        self.lineEdit_login_Email.setPlaceholderText(_translate("MainWindow", "Email"))
        self.lineEdit_login_password.setPlaceholderText(_translate("MainWindow", "Password"))
        self.pushButton_login_page.setText(_translate("MainWindow", "LOGIN"))
        self.label_goto_signup.setText(_translate("MainWindow", "Don't have an account?"))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())