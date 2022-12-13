from PyQt6.QtWidgets import *
from PyQt6 import uic
from Worker import Worker
import requests
import sys
import json
####    My Resources  ###########
sys.path.append("../Shared_Resources/")
from SHARED_GLOBAL_VARIABLES import *

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('./ui/login_page.ui', self)
        self.login_btn.clicked.connect(self.login_btn_on_click)

    def login_btn_on_click(self):
        def fetch(username , password):
            print("Inside fetch" , username , password)
            data = {"username":username , "password":password}
            headers = {"content-type":"application/json"}
            try:
                response = requests.post(f"{HOST}:{SV_PORT}/login" , data=json.dumps(data) , headers=headers)
                response = response.json()
                print("Username Fetched Response = " , response)
            except Exception as error:
                print("Error " , error)

        worker = Worker(fetch , username=self.username_lineedit.text(), password=self.password_lineedit.text())
        worker.threadPool.start(worker)





