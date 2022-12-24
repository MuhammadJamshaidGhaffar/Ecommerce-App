from PyQt6.QtWidgets import *
from PyQt6 import uic
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import sys
import requests

from Worker import Worker

from product_page import *

####    My Resources  ###########
sys.path.append("../Shared_Resources/")
from SHARED_GLOBAL_VARIABLES import *

from global_vars import *


class ProductWidget(QWidget):
    def __init__(self , product ):
        print("[productUi.py] step 1")
        super().__init__()
        uic.loadUi('./ui/product.ui', self)
        self.setFixedSize(QSize(426, 324))
        self.product = product
        self.image = None
        self.name_label.setText(product["name"])
        #self.descrip_label.setText(product.description)
        self.price_label.setText("RS." + str(product["price"]))
        self.prod_image_label.setText("Product Image here")

        self.viewprod_btn.clicked.connect(self.openProductPage)

        print("[productUi.py] step 2")
        try:
            print(product)
            url = f"{HOST}:{SV_PORT}/image?id={product['image_url']}"
            if("http" in product['image_url']):
                url = product["image_url"]
            worker = Worker(self.fetchImage , url=url)
            #worker.signals.finished.connect(self.on_login_success)
            print("[productUi.py] step 3")
            worker.signals.image.connect(self.on_image_fetch_success)
            worker.signals.error.connect(self.on_image_fetch_error)
            worker.threadPool.start(worker)
        except Exception as error:
            print(error)


    def fetchImage(self ,url):
        print("sending request to get image to url : \n" , url)
        response = requests.get(url)
        if(response.status_code >= 400):
            raise Exception("Failed to load Image")
        responseData = response.content
        #print("Inside : " , responseData  , type(responseData))
        return responseData

    def on_image_fetch_error(self , error):
        print(error)
    def on_image_fetch_success(self , binData):
        self.image = binData
        pixmap = QPixmap()
        #print(binData)
        pixmap.loadFromData(binData)
        self.prod_image_label.setPixmap(pixmap)
        self.prod_image_label.setScaledContents(True)

    def openProductPage(self):
        print("opening product page")
        try:
            window = ProductPage(self.product , self.image )
            window.show()
            globalVars["windows"]["productWindows"].append(window)
        except Exception as error:
            print(error)






