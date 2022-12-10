from datetime import datetime

class Product:
    def __init__(self , name , description ,price ,image_url ):
        print("creating product")
        self.name = name
        self.description = description
        self.price = price
        self.image_url = image_url
        self._id = -1


class User:
    def __init__(self , username , password , balance=0 , no_of_products_bought=0 , bought_products=[]):
        self.username = username
        self.password = password
        self.balance = balance
        self.no_of_products_bought = no_of_products_bought
        self.bought_products = bought_products

class Order:
    def __init__(self , product_id , payment_method  ,user_id , placed_on = datetime.timestamp(datetime.now()) , is_cash_payed = False , order_status = "Placed Successfully") :
        self.product_id = product_id
        self.payment_method = payment_method
        self.user_id = user_id
        self.placed_on = placed_on
        self.is_cash_payed = is_cash_payed
        self.order_status = order_status

