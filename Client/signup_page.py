from PyQt6.QtWidgets import *
from PyQt6 import uic
from Worker import Worker
import requests
import sys
import json
####    My Resources  ###########
sys.path.append("../Shared_Resources/")
from SHARED_GLOBAL_VARIABLES import *

class SignUpWindow(QWidget):
    def __init__(self , onSignupSuccess):
        super().__init__()
        uic.loadUi('./ui/signuppage.ui', self)
        self.signup_btn.clicked.connect(self.signup_btn_on_click)
        self.onSignupSuccess = onSignupSuccess
        self.login_btn.clicked.connect(self.onSignupSuccess)

    def signup_btn_on_click(self):
        print("Signup button is clicked")
        print(self.newpassword_lineedit.text() , self.confirmpassword_lineedit.text())
        if(self.newpassword_lineedit.text() != self.confirmpassword_lineedit.text()):
            print("Password does not match with confirm password")
            self.error_label.setText("Password does not match with confirm password")
            return
        def fetch(email , username , password):
            print("Inside fetch" , email , username , password)
            data = {"email" : email , "username":username , "password":password}
            headers = {"content-type":"application/json"}
            response = requests.post(f"{HOST}:{SV_PORT}/user" , data=json.dumps(data) , headers=headers)
            responseDict = response.json()
            print("Username Fetched Response = " , responseDict)
            if (response.status_code >= 400):
                raise Exception(responseDict["msg"])
            return responseDict

        self.error_label.setText("Creating new Account")
        worker = Worker(fetch , email=self.email_lineedit.text() ,username=self.newusername_lineedit.text(), password=self.newpassword_lineedit.text())
        worker.signals.finished.connect(self.onSignupSuccess)
        worker.signals.error.connect(self.onSignupError)
        worker.threadPool.start(worker)

    def onSignupError(self, error):
        print(error)
        print(type(error))
        self.error_label.setText(error[0])






