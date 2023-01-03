
from login_page import *
from signup_page import *
from MainPage import *
import functools
import sys

import global_vars

####    My Resources  ###########
sys.path.append("../Shared_Resources/")
from utility_classes import *
class Window:
    def __init__(self):


        self.loginWindow = LoginWindow(self.on_login_success , self.on_login_error)
        self.signupWindow = SignUpWindow(self.onSignUpSuccess)
        self.mainWindow = None
        # current active window
        self.window = self.loginWindow
        self.window.show()

        # connecting signup tbn in login window with signup window
        self.loginWindow.signup_btn.clicked.connect(functools.partial(self.setWindow , self.signupWindow))



    def setWindow(self , window):
        print("Changing window")
        self.window.close()
        self.window = window
        self.window.show()

    def on_login_success(self , user_data):
        globalVars["loggedInUserInfo"] = user_data
        self.mainWindow = MainWindow()
        self.setWindow(self.mainWindow)

    def on_login_error(self , error_tuple):
        print(error_tuple[0])
        print(type(error_tuple[0]))
        try:
            self.loginWindow.error_label.setText(error_tuple[0])
        except Exception as error:
            print(error)

    def onSignUpSuccess(self , data):
        print("signup succesfull")
        self.setWindow(self.loginWindow)




app = QApplication([])

window = Window()
#window = QMainWindow()
#window.show()

app.exec()


