from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QVBoxLayout, QHBoxLayout, QPushButton,QLineEdit
from PyQt5 import QtCore,QtWidgets
import sys

class CustomMessageBox(QDialog):
    def __init__(self, parent=None, text="", x=400, y=400, B1="OK", B2="Cancel"):
        super().__init__(parent)
        self.setWindowTitle("Custom Message Box")
        
        # Layouts
        self.layout = QVBoxLayout()
        self.button_layout = QHBoxLayout()

        # Label
        self.label = QLabel(text)
        self.label.setWordWrap(True)
        self.label.setAlignment(QtCore.Qt.AlignCenter)  # Align text to center
        
        # Set the dialog's style
        self.setStyleSheet(
            "background-color:#0F1C25;\n"
            "color:white;\n"
            "padding:5px;\n"
            "border:2px solid #0085FF;\n"
            "font-size: 20px;"
        )
        
        # Set size and geometry of the dialog
        self.setGeometry(QtCore.QRect(500, 300, x, y))
        
        # Add the label to the layout
        self.layout.addWidget(self.label)
        
        # Buttons
        
        
        # Set button styles
        button_style = """
            QPushButton {
                font-size: 20px;
                background-color:#0F1C25;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: lightblue;
                color:#0F1C25;
            }
            QPushButton:pressed {
                background-color: #0F1C25;
                color: white;
            }
        """
        if not B1=='none':
            self.b1 = QPushButton(B1)
            self.b1.setStyleSheet(button_style)
            self.button_layout.addWidget(self.b1)
            self.b1.clicked.connect(self.accept)
        if not B2=='none':
            self.b2 = QPushButton(B2)
            self.b2.setStyleSheet(button_style)
            self.button_layout.addWidget(self.b2)
            self.b2.clicked.connect(self.reject)
        
        # Add the button layout to the main layout
        self.layout.addLayout(self.button_layout)
        
        # Set the final layout
        self.setLayout(self.layout)

    # def ok_clicked(self):
    #     self.done(1)  # Set dialog result to 1 for OK
    #     self.close()

    # def cancel_clicked(self):
    #     self.done(0)  # Set dialog result to 0 for Cancel
    #     self.close()

    @staticmethod
    def show_message(parent=None,text="", x=400, y=400, B1="OK", B2="Cancel"):
        dialog = CustomMessageBox(parent,text, x, y, B1, B2)
        result = dialog.exec_()  # Start the dialog event loop and get the result
        return result  # Return the result of the dialog
    

class CustomInputBox(QDialog):
    def __init__(self, parent=None, text="", x=200, y=200, B1="OK", B2="Cancel"):
        super().__init__(parent)
        self.setWindowTitle("Custom Input Box")
        
        # Layouts
        self.layout = QVBoxLayout()
        self.button_layout = QHBoxLayout()

        # Label
        self.label = QLabel(text)
        self.label.setAlignment(QtCore.Qt.AlignCenter)  # Align text to center
        
        # Text Input
        self.input_field = QLineEdit(self)  # Create an input field
        self.input_field.setPlaceholderText("Enter your input here...")  # Placeholder text

        # Set the dialog's style
        self.setStyleSheet(
            "background-color:#0F1C25;\n"
            "color:white;\n"
            "padding:5px;\n"
            "border:2px solid #0085FF;\n"
            "font-size: 20px;"
        )
        
        # Set size and geometry of the dialog
        self.setGeometry(QtCore.QRect(500, 300, x, y))
        
        # Add the label and input field to the layout
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.input_field)
        
        # Buttons
        self.b1 = QPushButton(B1)
        self.b2 = QPushButton(B2)
        
        # Set button styles
        button_style = """
            QPushButton {
                font-size: 20px;
                background-color:#0F1C25;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: lightblue;
                color:#0F1C25;
            }
            QPushButton:pressed {
                background-color: #0F1C25;
                color: white;
            }
        """
        self.b1.setStyleSheet(button_style)
        self.b2.setStyleSheet(button_style)
        
        # Add buttons to the button layout
        self.button_layout.addWidget(self.b1)
        self.button_layout.addWidget(self.b2)
        
        # Connect button actions to close the dialog and set the result
        self.b1.clicked.connect(self.ok_clicked)
        self.b2.clicked.connect(self.cancel_clicked)
        
        # Add the button layout to the main layout
        self.layout.addLayout(self.button_layout)
        
        # Set the final layout
        self.setLayout(self.layout)
    def ok_clicked(self):
            self.done(1)  # Set dialog result to 1 for OK
            self.close()

    def cancel_clicked(self):
            self.done(0)  # Set dialog result to 0 for Cancel
            self.close()    



    

    @staticmethod
    def show_input_dialog(message):
        dialog = CustomInputBox(None, message, 600, 300, "OK", "Cancel")
        dialog.setWindowModality(QtCore.Qt.ApplicationModal)  # Set dialog as modal
        result = dialog.exec_()  # Start the dialog event loop and get the result
        
        if result == 1:  # If OK is clicked
            return dialog.input_field.text()  # Return the input text
        return None  # If Cancel is clicked or dialog is closed



# Backend call example
if __name__ == "__main__":
    result = CustomMessageBox.show_message("Welcome to NOVA\n\nNOVA is an AI assistant which can control your desktop based on your command.")
    if result == 1:
        print("User clicked OK")
    else:
        print("User clicked Cancel")