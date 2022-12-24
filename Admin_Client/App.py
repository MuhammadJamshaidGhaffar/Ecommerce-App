
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import functools
import sys

from global_vars import  *



########## Pages ###########
from login_page import *
from AdminPage import *
from orderPage import *



####    My Resources  ###########
sys.path.append("../Shared_Resources/")
from utility_classes import *
class Window:
    def __init__(self):


        self.loginWindow = LoginWindow(self.on_login_success )
        self.mainWindow = None
        # current active window
        self.window = self.loginWindow
        self.window.show()




    def setWindow(self , window):
        print("Changing window")
        self.window.close()
        self.window = window
        self.window.show()

    def on_login_success(self , user_data):
        globalVars["loggedInUserInfo"] = user_data
        print("User has been logged in")
        print(user_data)
        try:
            self.mainWindow = MainWindow()
            self.setWindow(self.mainWindow)
        except Exception as error:
            print(error)







app = QApplication([])

window = Window()

#window = OrderPage("2b2e51f3-c6fc-4b17-a57b-dd275f3e5f94")
#window.show()

app.exec()


