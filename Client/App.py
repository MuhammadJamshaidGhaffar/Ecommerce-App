


from login_page import *
from signup_page import *
from MainPage import *
import functools
import sys





####    My Resources  ###########
sys.path.append("../Shared_Resources/")
from utility_classes import *
class Window:
    def __init__(self):


        self.loginWindow = LoginWindow(self.on_login_success , self.on_login_error)
        self.signupWindow = SignUpWindow()
        self.mainWindow = None
        # current active window
        self.window = self.loginWindow
        self.window.show()

        # connecting login btn in signup page with login window
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
        print(error_tuple)




app = QApplication([])

window = Window()
#window = QMainWindow()
#window.show()

app.exec()


