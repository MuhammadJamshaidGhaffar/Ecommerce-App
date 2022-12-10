import sys
import aiohttp , json

####################### My Shared Resources #########################
sys.path.append("../Shared_Resources/")
from utility_classes import User
from SHARED_GLOBAL_VARIABLES import  HOST , DB_PORT

################## My Resources ###############################
from GLOBAL_VARIABLES import USER_COLLECTION_NAME


class Get_User_Handler():
    async def on_post(self , req,res):
        body = await req.get_media()
        print("step 1")
        # sends this request to database
        async with aiohttp.ClientSession() as session:
            body["collection"] = USER_COLLECTION_NAME
            print("step 2")
            headers = {"content-type": "application/json"}
            print("Step 3")
            try:
                response = await session.post(f"{HOST}:{DB_PORT}/get_document", data=json.dumps(body), headers=headers)
                response = await response.json()
                print("Response = ", response)
                res.status = 200
                res.text = json.dumps(response)
                return
            except Exception as error:
                print("Failed to Fetch user from database")
                print(error)
                res.status = 404
                res.text = json.dumps({"msg": error})
                return

class User_Handler:
    async def on_post(self, req, res):
        body = await req.get_media()
        print("Request on /user ---post")
        print("Body = " , body)
        for key, value in body.items():
            print(key, value, type(value))
        try:
            username = body["username"]
            password = body["password"]
        except :
            res.status = 403
            res.rext = "UserName and Password are required fields "
            return
        print("[/user -- post -- ]Syntax is correct")
        # Instantitate User Object
        user = User(username , password)
        # insert user on database
        async with aiohttp.ClientSession() as session :
            #first check if user  already exists
            data = {
                "collection" : USER_COLLECTION_NAME,
                "range": [0, -1],
                "filters": {
                    "username": username,
                }
            }
            headers = {"content-type": "application/json"}
            try:
                response = await session.post(f"{HOST}:{DB_PORT}/get_document", data=json.dumps(data), headers=headers)
                response = await response.json()
                response = json.loads(response)
                print("response for get_users check is =", response)
                if len(response["documents"]) > 0:
                    msg = "UserName Already exists"
                    print(msg)
                    res.status = 404
                    res.text = json.dumps({"msg":msg})
                    return
            except Exception as error :
                print("Failed to check if user alreay exists on database ", error)
                res.status = 401
                res.text = json.dumps({"msg": error})
                return

            print("User doesn't exists \nNow creating the document")
            data = {
                "collection" : USER_COLLECTION_NAME,
                "data" : user.__dict__
            }
            headers = {"content-type":"application/json"}
            try:
                response = await session.post(f"{HOST}:{DB_PORT}/document" , data = json.dumps(data)  , headers = headers)
                response = await response.json()
                print("response =" , response)
                res.status = 200
                res.text = json.dumps(response)
                return
            except Exception as error:
                print("Failed to create user on database " , error)
                res.status = 404
                res.text = json.dumps({"msg":error})
                return
    async def on_put(self,req,res):
        body = await req.get_media()
        if "username" not in body or "password" not in body or "update" not in body:
            msg = "Username or password or update is missing"
            res.status = 401
            res.text = json.dumps({"msg":msg})
            print(msg)
            return
        print("step 1")
        #sends this request to database
        async with aiohttp.ClientSession() as session :
            data = {
                "collection": USER_COLLECTION_NAME,
                "range": [0, -1],
                "filters":{
                    "username" : body["username"],
                    "password" : body["password"]
                },
                "update": body["update"]
            }
            print("step 2")
            headers = {"content-type":"application/json"}
            print("Step 3")
            try:
                response = await session.put(f"{HOST}:{DB_PORT}/document" , data=json.dumps(data) , headers=headers)
                response = await response.json()
                print("Response = ", response)
                res.status = 200
                res.text = json.dumps(response)
                return
            except Exception as error:
                print("Failed to update user on server")
                print(error)
                res.status = 404
                res.text = json.dumps({"msg":error})
                return
    async def on_delete(self,req,res):
        body = await req.get_media()
        if "username" not in body or "password" not in body:
            msg = "Username or password  is missing"
            res.status = 401
            res.text = json.dumps({"msg":msg})
            print(msg)
            return
        print("step 1")
        #sends this request to database
        async with aiohttp.ClientSession() as session :
            data = {
                "collection": USER_COLLECTION_NAME,
                "range": [0, -1],
                "filters":{
                    "username" : body["username"],
                    "password" : body["password"]
                },
            }
            print("step 2")
            headers = {"content-type":"application/json"}
            print("Step 3")
            try:
                response = await session.delete(f"{HOST}:{DB_PORT}/document" , data=json.dumps(data) , headers=headers)
                response = await response.json()
                print("Response = ", response)
                res.status = 200
                res.text = json.dumps(response)
                return
            except Exception as error:
                print("Failed to delete user on server")
                print(error)
                res.status = 404
                res.text = json.dumps({"msg":error})
                return



