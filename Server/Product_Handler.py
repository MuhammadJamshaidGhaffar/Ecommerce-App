import json

import falcon , sys , uuid , aiohttp
############ MY Resources #################
sys.path.append("../Shared_Resources/")
from utility_classes import Product
from GLOBAL_VARIABLES import *
from SHARED_GLOBAL_VARIABLES import  HOST , DB_PORT


class Get_Product_Handler():
    async def on_post(self , req, res):
        body = await req.get_media()
        body["collection"] = PRODUCT_COLLECTION_NAME
        headers = {"content-type": "application/json"}
        try:
            async with aiohttp.ClientSession() as session:
                response = await session.post(f"{HOST}:{DB_PORT}/get_document" , data=json.dumps(body) ,  headers = headers)
                response = await response.json()
                print("Query : " , body)
                print(("Response form db = " , response))
                res.status = 200
                res.text = json.dumps(response)
                return
        except Exception as error:
            print("Error : " , str(error))
            res.status = 404
            res.text = str(error)
            return

class Product_Handler():
    async def on_post(self,req,res):
        #convert body into json
        body = await req.get_media()
        #check if body contains all the required properties of prouct class
        try:
            name = body["name"]
            description = body["description"]
            price = body["price"]
            image_url = body["image_url"]
        except Exception as error:
            res.status = 404
            res.text = json.dumps({"msg":"Missing required properties of product class" + str(error)})
            return
        print("/product --post -- all fields are present")
        # instantiate product object
        try:
            product = Product(name , description ,price , image_url )
        except Exception as error:
            print(str(error))
        print("product instantiated")
        # sends request to database
        async with aiohttp.ClientSession() as session:
            data = {
                "collection" :PRODUCT_COLLECTION_NAME,
                "data" : product.__dict__
            }
            headers = {"content-type":"application/json"}
            try:
                response = await session.post(f"{HOST}:{DB_PORT}/document", data=json.dumps(data), headers=headers)
                response = await response.json()
                print("response =", response)
                res.status = 200
                res.text = json.dumps(response)
                return
            except Exception as error:
                print("Failed to create Product on database ", str(error))
                res.status = 404
                res.text = json.dumps({"msg": str(error)})
                return
    async def on_put(self,req,res):
        body = await req.get_media()
        body["collection"] = PRODUCT_COLLECTION_NAME
        headers = {"content-type": "application/json"}
        #sends this request to database
        async with aiohttp.ClientSession() as session :
            try:
                response = await session.put(f"{HOST}:{DB_PORT}/document" , data=json.dumps(body) , headers=headers)
                response = await response.json()
                print("Response = ", response)
                res.status = 200
                res.text = json.dumps(response)
                return
            except Exception as error:
                print("Failed to update Product on server")
                print(str(error))
                res.status = 404
                res.text = json.dumps({"msg":str(error)})
                return
    async def on_delete(self,req,res):
        body = await req.get_media()
        body["collection"] = PRODUCT_COLLECTION_NAME
        headers = {"content-type": "application/json"}
        # sends this request to database
        async with aiohttp.ClientSession() as session:
            try:
                response = await session.delete(f"{HOST}:{DB_PORT}/document", data=json.dumps(body), headers=headers)
                response = await response.json()
                print("Response = ", response)
                res.status = 200
                res.text = json.dumps(response)
                return
            except Exception as error:
                print("Failed to delete Product on server")
                print(str(error))
                res.status = 404
                res.text = json.dumps({"msg": str(error)})
                return

