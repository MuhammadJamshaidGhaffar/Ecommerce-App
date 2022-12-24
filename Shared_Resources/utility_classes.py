from datetime import datetime

class Product:
    def __init__(self , name , description ,price ,image_url ):
        print("creating product")
        self.name = name
        self.description = description
        self.price = price
        self.image_url = image_url


class User:
    def __init__(self , email ,username , password , balance=0 , no_of_products_bought=0 , bought_products=[] , cart = []):
        self.email = email
        self.username = username
        self.password = password
        self.balance = balance
        self.no_of_products_bought = no_of_products_bought
        self.bought_products = bought_products
        self.cart = cart

class Order:
    def __init__(self , product_id  ,user_id , delivery_address ,isOrderCompleted = False , placed_on = datetime.timestamp(datetime.now()) , is_cash_payed = False , order_status = ["placed successfully"]) :
        self.product_id = product_id
        self.user_id = user_id
        self.delivery_address = delivery_address
        self.placed_on = placed_on
        self.is_cash_payed = is_cash_payed
        self.order_status = order_status
        self.isOrderCompleted = isOrderCompleted

class AdminUser:
    def __init__(self , email ,username , password ):
        self.email = email
        self.username = username
        self.password = password
