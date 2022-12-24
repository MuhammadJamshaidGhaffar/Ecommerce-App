from builtins import Exception

from PyQt6.QtWidgets import *
from PyQt6 import *
from Worker import Worker
import requests
import sys
import json
import time
import functools

from Product_Ui import *
from cart import *
####    My Resources  ###########
sys.path.append("../Shared_Resources/")
from SHARED_GLOBAL_VARIABLES import *
from utility_classes import *

from global_vars import *

class MainWindow(QWidget):
    def __init__(self  ):
        super().__init__()
        uic.loadUi('./ui/MainPage.ui', self)

        self.startWorkerToFetchAllProducts()

        # search button connect
        self.search_btn.clicked.connect(self.searchProduct)

        # cart btn connect
        self.cart_btn.clicked.connect(self.openCartPage)






    def startWorkerToFetchAllProducts(self , filters={}):
        worker = Worker(self.fetchAllProducts, filters=filters)
        worker.signals.finished.connect(self.on_product_fetch_success)
        worker.signals.error.connect(self.on_product_fetch_error)
        worker.threadPool.start(worker)

    def fetchAllProducts(self , filters = {} ):
        print("On serach click  , " , self.searchbar.text())
        print("Filters are : " , filters)
        data = {"filters" : filters}
        headers = {"content-type":"application/json"}
        response = requests.post(f"{HOST}:{SV_PORT}/get_product" , data=json.dumps(data) , headers=headers)
        responseDict = json.loads(response.json())

        if(response.status_code >= 400):
            raise Exception(responseDict["msg"])
        print("All products Fetched Response = " , responseDict)
        return responseDict

    def searchProduct(self):
        textToSearch = self.searchbar.text().split()
        NumToSearch  = []
        for word in textToSearch:
            if(word.isdigit()):
                NumToSearch.append(int(word))
        filters = None
        if(len(textToSearch) == 0):
            filters={}
            self.addPriceFilter(filters)
        else:
            filters = {
                "$or": [{"name": ["$substring/i", textToSearch]}, {"description": ["$substring/i", textToSearch]}, {"price":["$eq",NumToSearch]}]
            }
            self.addPriceFilter(filters)

        self.startWorkerToFetchAllProducts(filters=filters)

    def addPriceFilter(self , filters):
        min_price = None
        max_price = None
        try:
            min_price = int(self.min_price_edit.text())
            filters["$and"] = [{"price": ["$gte", [min_price]]}]
        except Exception as error:
            print(error)
        try:
            max_price = int(self.max_price_edit.text())
            if "$and" in filters:
                filters["$and"].append({"price": ["$lte", [max_price]]})
            else:
                filters["$and"] = [{"price": ["$lte", [max_price]]}]
        except Exception as error:
            print(error)

    def on_product_fetch_success(self , responseDic ):
        print("on fetching all prodcuts success")
        products = responseDic["documents"]
        remaining = responseDic["remaining"]
        self.scrollbar_inside_widget = QWidget()  # Widget that contains the collection of Vertical Box
        self.scrollbar_inside_widget_vbox = QVBoxLayout()  # The Vertical Box that contains the Horizontal Boxes of  labels and buttons
        for product in products:
            p = ProductWidget(product )
            self.scrollbar_inside_widget_vbox.addWidget(p)

        self.scrollbar_inside_widget.setLayout(self.scrollbar_inside_widget_vbox)

        # Scroll Area Properties
        self.products_scrollArea.setWidgetResizable(True)
        self.products_scrollArea.setWidget(self.scrollbar_inside_widget)

    def on_product_fetch_error(self , error):
        print(error)

    def openCartPage(self):
        print("Opening cart Page")
        try:
            window = CartPage()
            window.show()
            globalVars["windows"]["cartWindow"] = window
        except Exception as error:
            print(error)







