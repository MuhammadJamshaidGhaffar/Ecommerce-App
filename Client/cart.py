import functools

from PyQt6.QtWidgets import *
from PyQt6 import uic
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import sys
import requests
from Worker import Worker
import json

from product_page import *

####    My Resources  ###########
sys.path.append("../Shared_Resources/")
from SHARED_GLOBAL_VARIABLES import *
from utility_classes import *

from global_vars import  *

class CartPage(QWidget):
    def __init__(self ):
        super().__init__()
        uic.loadUi('./ui/cart.ui', self)
        self.cart = []

        self.place_order_response.setText("Fetching cart data")
        worker = Worker(self.fetchCart)
        worker.signals.finished.connect(self.onCartFetchSuccess)
        worker.signals.error.connect(self.onCartFetchError)
        worker.threadPool.start(worker)


        # form to hold cart products
        self.scrollbar_inside_widget = QWidget()  # Widget that contains the collection of Vertical Box
        # self.scrollbar_inside_widget_vBox = QFormLayout()
        self.scrollbar_inside_widget_vBox = QVBoxLayout()

        self.scrollbar_inside_widget.setLayout(self.scrollbar_inside_widget_vBox)

        # Scroll Area Properties
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.scrollbar_inside_widget)
    def clearScrollArea(self):
        # form to hold cart products
        self.scrollbar_inside_widget = QWidget()  # Widget that contains the collection of Vertical Box
        # self.scrollbar_inside_widget_vBox = QFormLayout()
        self.scrollbar_inside_widget_vBox = QVBoxLayout()

        self.scrollbar_inside_widget.setLayout(self.scrollbar_inside_widget_vBox)

        # Scroll Area Properties
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.scrollbar_inside_widget)

    def fetchCart(self ):
        data = {
            "_id": globalVars["loggedInUserInfo"]["_id"],
            "output": {
                "cart": 1
            }
        }
        headers = {"content-type": "application/json"}
        response = requests.post(f"{HOST}:{SV_PORT}/get_user", data=json.dumps(data), headers=headers)
        responseDict = response.json()

        if (response.status_code >= 400):
            raise Exception(responseDict["msg"])
        print("Cart Fetched Response = ", responseDict)
        return responseDict

    def onCartFetchSuccess(self , user):
        self.place_order_response.setText("Cart data fetched susccessfully")
        self.cart = user["cart"]
        print(self.cart)
        self.clearScrollArea()
        self.place_order_response.setText("Getting data for products in cart")
        for product_id in self.cart:
            self.startWorkertoGetProduct(product_id)

        # now bind the place order button with place order function
        self.placeOrder_btn.clicked.connect(self.placeOrder)

    def onCartFetchError(self , error):
        print(error)
        self.place_order_response.setText("Something Went Wrong! Failed to fetch cart data")

    def startWorkertoGetProduct(self , _id):
        worker = Worker(self.fetchProduct , _id = _id)
        worker.signals.finished.connect(self.onProductFetchSuccess)
        worker.signals.error.connect(self.onProductFetchError)
        worker.threadPool.start(worker)
    def fetchProduct(self , _id):
        data = {
            "_id": _id,
            "output": {
                "name":1
            }
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
        try:
            name_btn = QPushButton(product["name"])
            name_btn.clicked.connect(functools.partial(self.openProductPage , product["_id"]))

            delete_btn = QPushButton("X")
            delete_btn.setFixedSize(QSize(20,20))
            delete_btn.setObjectName("delete_btn")
            delete_btn.setStyleSheet("background-color:red")
            delete_btn.clicked.connect(functools.partial(self.startWorkerToUpdateCart ,["$remove" , [product["_id"]]]))

            hBoxLayout = QHBoxLayout()
            hBoxLayout.addWidget(name_btn )
            hBoxLayout.addWidget(delete_btn)
            self.scrollbar_inside_widget_vBox.addLayout(hBoxLayout)
        except Exception as error:
            print(error)

    def onProductFetchError(self, error):
            print(error)

    def openProductPage(self  , _id):
        print("opening product page")
        try:
            window = ProductPage(_id = _id)
            window.show()
            globalVars["windows"]["productWindows"].append(window)
        except Exception as error:
            print(error)

    def placeOrder(self):
        try:
            delivery_address = self.delivery_addr_line_edit.text()
        except Exception as error:
            print(error)
        try:
            for product_id in self.cart:
                self.startWorkerToPlaceOrder(product_id, globalVars["loggedInUserInfo"]["_id"] , delivery_address)
        except Exception as error:
            print(error)

    def startWorkerToPlaceOrder(self , product_id , user_id , delivery_address):
        self.place_order_response.setText("placing orders")
        print("starting worker")
        worker = Worker(self.fetchPlaceOrder , product_id = product_id , user_id = user_id , delivery_address = delivery_address)
        worker.signals.finished.connect(self.onPlaceOrderSuccess)
        worker.signals.error.connect(self.onPlaceOrderError)
        worker.threadPool.start(worker)

    def fetchPlaceOrder(self, product_id , user_id , delivery_address):
        print("fetching place Order")
        data = {
            "product_id": product_id,
            "user_id": user_id ,
            "delivery_address" : delivery_address
        }
        headers = {"content-type": "application/json"}
        response = requests.post(f"{HOST}:{SV_PORT}/order", data=json.dumps(data), headers=headers)
        responseDict = response.json()

        if (response.status_code >= 400):
            raise Exception(responseDict["msg"])
        print("Place Order fetched Response = ", responseDict)
        return responseDict

    def onPlaceOrderSuccess(self, order):
        print("order has been placed successfuly")
        self.place_order_response.setText("Order has been Place successfully")
        self.startWorkerToUpdateCart([])

        #  deleting cart text
        self.cart = []
        self.scrollbar_inside_widget = QWidget()  # Widget that contains the collection of Vertical Box
        self.scrollbar_inside_widget_vBox = QVBoxLayout()
        self.scrollbar_inside_widget.setLayout(self.scrollbar_inside_widget_vBox)

        # Scroll Area Properties
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.scrollbar_inside_widget)

    def onPlaceOrderError(self , error):
        print(error)
        self.place_order_response.setText("Something Went Wrong! Failed to place order")

    def startWorkerToUpdateCart(self , cartQuery = []):
        worker = Worker(self.updateCart , cartQuery = cartQuery)
        worker.signals.finished.connect(self.onCartFetchSuccess)
        worker.signals.error.connect(self.onCartFetchError)
        worker.threadPool.start(worker)

    def updateCart(self , cartQuery = []):
        print("Deleting Cart")
        data = {"_id": globalVars["loggedInUserInfo"]["_id"],
                "update": {
                    "cart": cartQuery
                }}
        print("sending request to delete cart " )
        print(json.dumps(data))
        print(type(json.dumps(data)))
        headers = {"content-type": "application/json"}
        response = requests.put(f"{HOST}:{SV_PORT}/user", data=json.dumps(data), headers=headers)
        responseDict = response.json()
        print(responseDict)
        if (response.status_code >= 400):
            raise Exception(responseDict["msg"])
        print("updated cart response = ", responseDict)
        return responseDict











