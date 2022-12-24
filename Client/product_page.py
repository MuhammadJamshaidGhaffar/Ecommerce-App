from PyQt6.QtWidgets import *
from PyQt6 import uic
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import sys
import requests
from Worker import Worker
import json

from global_vars import *

####    My Resources  ###########
sys.path.append("../Shared_Resources/")
from SHARED_GLOBAL_VARIABLES import *

class ProductPage(QWidget):
    def __init__(self , product={}  , image=None , _id = None):
        super().__init__()
        uic.loadUi('./ui/productpage.ui', self)
        if product != {} and image != None :
            self.initializeProductPage(product, image)
        else:
            if product == {}:
                if _id != None:
                    worker = Worker(self.fetchProduct , _id = _id)
                    worker.signals.finished.connect(self.onProductFetchSuccess)
                    worker.signals.error.connect(self.onProductFetchError)
                    worker.threadPool.start(worker)



    def initializeProductPage(self , product , image=None):
        self.product = product
        if image != None:
            self.image = image
            self.setImage(image)
        self.name_label.setText(product["name"])
        self.descrip_label.setText(product["description"])
        self.price_label.setText("RS." + str(product["price"]))

        self.add_to_cart_btn.clicked.connect(self.startUpdateCartWorker)

    def fetchProduct(self , _id):
        data = {
            "_id": _id,
        }
        headers = {"content-type": "application/json"}
        response = requests.post(f"{HOST}:{SV_PORT}/get_product", data=json.dumps(data), headers=headers)
        responseDict = response.json()
        if (response.status_code >= 400):
            raise Exception(responseDict["msg"])
        responseDict["_id"] = _id
        print("Product Name Fetched Response = ", responseDict)
        return responseDict

    def onProductFetchSuccess(self , product):
        self.initializeProductPage(product)
        # now fetch the image
        worker = Worker(self.fetchImage, image_url = product["image_url"])
        worker.signals.image.connect(self.on_image_fetch_success)
        worker.signals.error.connect(self.on_image_fetch_error)
        worker.threadPool.start(worker)

    def onProductFetchError(self, error):
            print(error)

    def setImage(self , image):
        print("setting Image")
        pixmap = QPixmap()
        pixmap.loadFromData(image)
        self.prod_image_label.setPixmap(pixmap)
        self.prod_image_label.setScaledContents(True)

    def fetchImage(self ,image_url):
        url = f"{HOST}:{SV_PORT}/image?id={image_url}"
        if "http" in image_url:
            url = image_url
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
        print("Image Fetched Succesflly")
        self.setImage(binData)
    ######## CART #############
    def startUpdateCartWorker(self):
        print("worker staerted")
        addToCartWorker = Worker(self.updateCart)
        addToCartWorker.threadPool.start(addToCartWorker)
    def updateCart(self ):
        print("[updateCart] step 1")
        print(globalVars["loggedInUserInfo"]["username"])
        print(globalVars["loggedInUserInfo"]["password"])
        print(self.product)
        data = {"_id":globalVars["loggedInUserInfo"]["_id"],
                "update":{
                    "cart":["$push" , [self.product["_id"]]]
                }}
        print("sending request to update cart")
        headers = {"content-type":"application/json"}
        response = requests.put(f"{HOST}:{SV_PORT}/user" , data=json.dumps(data) , headers=headers)
        responseDict = json.loads(response.json())
        print(responseDict)
        if(response.status_code >= 400):
            raise Exception(responseDict["msg"])
        print("updated user = " , responseDict)
        return responseDict







