import falcon.asgi
import sys
####################### My Resources #########################
sys.path.append("../Shared_Resources/")
from utility_classes import User , Order , Product
###################### My Modules ##########################
from  Image_Handler import *
from User_Handler import *
from Product_Handler import *
from Order_Handler import *

app = falcon.asgi.App()


app.add_route("/image" , Image())

app.add_route("/user" , User_Handler())
app.add_route("/login" , Get_User_Handler())

app.add_route("/get_product" , Get_Product_Handler())
app.add_route("/product" , Product_Handler())

app.add_route("/get_order" , Get_Order_Handler())
app.add_route("/order" , Order_Handler())





