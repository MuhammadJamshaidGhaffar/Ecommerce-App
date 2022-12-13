from PyQt6.QtWidgets import *
from login_page import *



app = QApplication([])
window = QMainWindow()

loginWindow = LoginWindow()
window = loginWindow

window.show()
app.exec()
