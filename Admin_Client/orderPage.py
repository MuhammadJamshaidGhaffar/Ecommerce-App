from builtins import Exception

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

width = 601
height = 550

class OrderPage(QWidget):
    def __init__(self , _id):
        super().__init__()

        self.order_id = _id
        self.size = QSize(width , height)

        uic.loadUi('./ui/order_page_1.ui', self)
        self.groupBox.setFixedSize(self.size)
        self.order = None
        self.product = None
        self.image = None
        self.startWorkerToFetchOrder()


        ####### Adding Layout in order tracker widget  #############
        self.order_tracker_layout = QVBoxLayout()
        self.order_tracker_layout.setSpacing(10)
        self.order_tracker_widget.setLayout(self.order_tracker_layout)

        #### connecting update order status btn with function #######
        self.update_order_status_btn.clicked.connect(self.startWorkerToUpdateOrderStatus)

    def initializeOrderPage(self ):
        try:
            if self.image != None:
                self.setImage()
            if self.order != None:
                self.setOrderDetails()
            if self.product != None:
                self.setProductDetails()

        except Exception as error:
            print(error)

    def startWorkerToFetchOrder(self):
        worker = Worker(self.fetchOrder)
        worker.signals.finished.connect(self.onOrderFetchSuccess)
        worker.signals.error.connect(self.onOrderFetchError)
        worker.threadPool.start(worker)

    def fetchOrder(self):
        data = {
            "_id" : self.order_id
        }
        headers = {"content-type": "application/json"}
        response = requests.post(f"{HOST}:{SV_PORT}/get_order", data=json.dumps(data), headers=headers)
        responseDict = response.json()
        if (response.status_code >= 400):
            print("Wrong :", responseDict["msg"])
            raise Exception(responseDict["msg"])
        print("Order Fetched Response = ", responseDict)
        return responseDict

    def onOrderFetchSuccess(self, order):
        self.order = order
        self.initializeOrderPage()
        self.startWorkerToFetchProduct()

    def onOrderFetchError(self, error):
        print(error)

    def startWorkerToFetchProduct(self):
        worker = Worker(self.fetchProduct)
        worker.signals.finished.connect(self.onProductFetchSuccess)
        worker.signals.error.connect(self.onProductFetchError)
        worker.threadPool.start(worker)

    def fetchProduct(self ):
        data = {
            "_id": self.order["product_id"],
        }
        headers = {"content-type": "application/json"}
        response = requests.post(f"{HOST}:{SV_PORT}/get_product", data=json.dumps(data), headers=headers)
        responseDict = response.json()
        if (response.status_code >= 400):
            raise Exception(responseDict["msg"])
        print("Product Name Fetched Response = ", responseDict)
        return responseDict

    def onProductFetchSuccess(self , product):
        self.product = product
        self.setProductDetails()
        # now fetch the image
        worker = Worker(self.fetchImage, image_url = self.product["image_url"])
        worker.signals.image.connect(self.on_image_fetch_success)
        worker.signals.error.connect(self.on_image_fetch_error)
        worker.threadPool.start(worker)

    def onProductFetchError(self, error):
            print(error)

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
        self.image = binData
        try:
            self.setImage()
        except Exception as error:
            print(error)

    def setOrderDetails(self):
        print("setting order details")

        self.order_id_label.setText(self.order["_id"])
        self.order_status_label.setText(self.order["order_status"][-1])
        self.delivery_address_label.setText(self.order["delivery_address"])

        #### clearing the order layout
        self.order_tracker_layout.setSpacing(15)

        # setting order tracker
        for index ,order_past_status in enumerate(self.order["order_status"] , start=1):
            index_label = QLabel(str(index))
            index_label.setFixedSize(QSize(20,20))
            index_label.setStyleSheet("background-color:rgb(255, 255, 0);"
                                      "padding-left:2px")

            order_status_label = QLabel(order_past_status)
            order_status_label.setStyleSheet("background-color:white;"
                                             "border-radius:10px;"
                                             "padding-left:10px;")
            order_status_label.setFixedHeight(21)

            hBoxLayout = QHBoxLayout()
            hBoxLayout.addWidget(index_label)
            hBoxLayout.addWidget(order_status_label)
            hBoxLayout.setSpacing(10)

            # widget = QWidget()
            # widget.setFixedHeight(31)
            # widget.setLayout(hBoxLayout)
            # self.self.order_tracker_layout.addWidget(widget)
            self.order_tracker_layout.addLayout(hBoxLayout)


        increasedHeight = 21 + self.order_tracker_layout.spacing()
        increasedHeight = len(self.order["order_status"]) * (increasedHeight)
        self.order_tracker_widget.setFixedHeight(increasedHeight)
        self.groupBox.setFixedSize(QSize(width , height+ increasedHeight))



    def setProductDetails(self):
        try:
            self.product_name_label.setText(self.product["name"])
        except Exception as error:
            print(error)

    def setImage(self ):
        print("setting Image")
        pixmap = QPixmap()
        pixmap.loadFromData(self.image)
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)

    def startWorkerToUpdateOrderStatus(self):
        if(self.update_status_lineedit.text() == ""):
            return
        worker = Worker(self.updateOrderStatus)
        worker.signals.finished.connect(self.onOrderUpdateSuccess)
        worker.signals.error.connect(self.onOrderUpdateError)
        worker.threadPool.start(worker)
    def updateOrderStatus(self):
        data = {"_id":self.order_id,
                "update":{
                    "order_status":["$push" , [self.update_status_lineedit.text().lower()]]
                }
            }
        print("sending request to update Order")
        headers = {"content-type":"application/json"}
        response = requests.put(f"{HOST}:{SV_PORT}/order" , data=json.dumps(data) , headers=headers)
        responseDict = response.json()
        if(response.status_code >= 400):
            raise Exception(responseDict["msg"])
        print("updated Order = " , responseDict)
        return responseDict

    def onOrderUpdateSuccess(self , order):
        self.order = order

        try:
            index_label = QLabel(str(len(self.order["order_status"])))
            index_label.setFixedSize(QSize(20, 20))
            index_label.setStyleSheet("background-color:rgb(255, 255, 0);"
                                      "padding-left:2px")

            order_status_label = QLabel(self.order["order_status"][-1])
            order_status_label.setStyleSheet("background-color:white;"
                                             "border-radius:10px;"
                                             "padding-left:10px;")
            order_status_label.setFixedHeight(21)

            hBoxLayout = QHBoxLayout()
            hBoxLayout.addWidget(index_label)
            hBoxLayout.addWidget(order_status_label)
            hBoxLayout.setSpacing(10)
            self.order_tracker_layout.addLayout(hBoxLayout)

            increasedHeight = 21 + self.order_tracker_layout.spacing()
            increasedHeight = len(self.order["order_status"]) * (increasedHeight)
            self.order_tracker_widget.setFixedHeight(increasedHeight)
            print("here")
            self.groupBox.setFixedSize(QSize(width, height + increasedHeight))
        except Exception as error:
            print(error)

    def onOrderUpdateError(self , error):
        print(error)







