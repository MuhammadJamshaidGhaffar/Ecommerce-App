import functools

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6 import uic
from Worker import Worker
import requests
import sys
import json
import time

from orderPage import *
####    My Resources  ###########
sys.path.append("../Shared_Resources/")
from SHARED_GLOBAL_VARIABLES import *

orderWindows = []

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('./ui/adminpage.ui', self)
        self.reload_btn.clicked.connect(self.startWorkerToFetchOrders)

        try:
            self.startWorkerToFetchOrders()
        except Exception as error:
            print("Error in starting worker to fetch Orders" ,error)
        self.order_uis = []


    def startWorkerToFetchOrders(self):
        worker = Worker(self.fetchOrder)
        worker.signals.finished.connect(self.onOrderFetchSuccess)
        worker.signals.error.connect(self.onOrderFetchError)
        worker.threadPool.start(worker)
    def clearScrollArea(self):
        self.order_uis = []
        # scroll Area to hold orders
        self.scrollbar_inside_widget = QWidget()  # Widget that contains the collection of Vertical Box
        # self.scrollbar_inside_widget_vBox = QFormLayout()
        self.scrollbar_inside_widget_vBox = QVBoxLayout()

        self.scrollbar_inside_widget.setLayout(self.scrollbar_inside_widget_vBox)

        # Scroll Area Properties
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.scrollbar_inside_widget)

    def fetchOrder(self ):
        filters = {}
        if self.search_order_line_edit.text() != "":
            filters = {
                "order_status": ["$in", [self.search_order_line_edit.text().lower()]]
            }
        try:
            data = {
                "filters":filters,
                "output":{
                    "_id":1,
                    "product_id":1,
                    "order_status":1,
                    "placed_on":1
                }
            }
            headers = {"content-type": "application/json"}
            response = requests.post(f"{HOST}:{SV_PORT}/get_order", data=json.dumps(data), headers=headers)
        except Exception as error:
            print(error)
        responseDict = response.json()

        if (response.status_code >= 400):
            print("Wrong :" , responseDict["msg"])
            raise Exception(responseDict["msg"])


        responseDict = json.loads(responseDict)
        print("Printing type of date")
        print(type(responseDict["documents"][0]["placed_on"]))
        print(responseDict["documents"][0]["placed_on"])
        responseDict["documents"].sort(reverse=True, key=lambda order: order["placed_on"])
        print("Order Fetched Response = ", responseDict )
        return responseDict

    def onOrderFetchSuccess(self , orders):
        self.orders = orders["documents"]
        print("Orders has been fetched")
        print(self.orders)
        self.clearScrollArea()
        for index , order in enumerate(self.orders , start=1):
            try:
                order_ui = QWidget()
                uic.loadUi("./ui/orderui.ui" , order_ui)

                order_ui.setFixedSize(QSize(777,170))
                order_ui.order_id_label.setText(order["_id"])
                order_ui.order_serial_label.setText(str(index))
                order_ui.order_status_label.setText(order["order_status"][-1])
                # try:
                order_ui.vieworder_btn.clicked.connect(functools.partial(self.openOrder , order["_id"]))
                # except Exception as error:
                #     print(error)


                self.order_uis.append(order_ui)
                self.scrollbar_inside_widget_vBox.addWidget(self.order_uis[index-1])

                # start worker to get product Names #########
                print("TYUI" ,order["product_id"] , index-1)
                self.startWorkertoGetProduct(order["product_id"] , index-1)
            except Exception as error:
                print(error)


    def onOrderFetchError(self , error):
        print(error)

    def startWorkertoGetProduct(self , product_id , indexOfOrderUi):
        worker = Worker(self.fetchProduct , product_id = product_id , indexOfOrderUi = indexOfOrderUi)
        worker.signals.finished.connect(self.onProductFetchSuccess)
        worker.signals.error.connect(self.onProductFetchError)
        worker.threadPool.start(worker)
    def fetchProduct(self , product_id , indexOfOrderUi ):
        try:
            data = {
                "_id": product_id,
                "output": {
                    "name":1
                }
            }
            print("Feting product " , product_id , indexOfOrderUi)
            headers = {"content-type": "application/json"}
            response = requests.post(f"{HOST}:{SV_PORT}/get_product", data=json.dumps(data), headers=headers)
            responseDict = response.json()

            if (response.status_code >= 400):
                raise Exception(responseDict["msg"])
            responseDict["indexOfOrderUi"] = indexOfOrderUi
            print("Product Name Fetched Response = ", responseDict)
            return responseDict
        except Exception as error:
            print("lol", error)

    def onProductFetchSuccess(self , product):
        try:
            print(product)
            self.order_uis[product["indexOfOrderUi"]].order_name_label.setText(product["name"])
        except Exception as error:
            print(error)

    def onProductFetchError(self, error):
            print(error)

    def openOrder(self , _id):
        window = OrderPage(_id)
        orderWindows.append(window)
        window.show()






