from PyQt6.QtWidgets import *
from PyQt6 import uic
from Worker import Worker
import requests
import sys
import json
import time
####    My Resources  ###########
sys.path.append("../Shared_Resources/")
from SHARED_GLOBAL_VARIABLES import *

class LoginWindow(QWidget):
    def __init__(self , on_login_success , on_login_error):
        super().__init__()
        uic.loadUi('./ui/loginpage.ui', self)
        self.on_login_success = on_login_success
        self.on_login_error = on_login_error
        self.login_btn.clicked.connect(self.login_btn_on_click)

    def login_btn_on_click(self):
        print("button is clicked")
        def fetch(username , password):
            print("Inside fetch" , username , password)
            data = {"username":username , "password":password}
            headers = {"content-type":"application/json"}
            response = requests.post(f"{HOST}:{SV_PORT}/login" , data=json.dumps(data) , headers=headers)
            responseDict = response.json()
            if(response.status_code >= 400):
                raise Exception(responseDict["msg"])
            print("Username Fetched Response = " , responseDict)
            return responseDict

        self.error_label.setText("Checking credentials")
        worker = Worker(fetch , username=self.username_lineedit.text(), password=self.password_lineedit.text())
        worker.signals.finished.connect(self.on_login_success)
        worker.signals.error.connect(self.on_login_error)
        worker.threadPool.start(worker)





