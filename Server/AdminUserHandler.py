import sys
import aiohttp , json

####################### My Shared Resources #########################
sys.path.append("../Shared_Resources/")
from utility_classes import AdminUser
from SHARED_GLOBAL_VARIABLES import  HOST , DB_PORT

################## My Resources ###############################
from GLOBAL_VARIABLES import ADMIN_USER_COLLECTION_NAME


class Admin_Login_Handler():
    async def on_post(self , req,res):
        body = await req.get_media()
        print("Request on /login_admin ---post")
        print("Body = ", body)
        for key, value in body.items():
            print(key, value, type(value))
        try:
            username = body["username"]
            password = body["password"]
        except Exception as error:
            res.status = 403
            res.text = json.dumps({"msg":"UserName and Password are required fields " })
            return
        data = {
            "collection": ADMIN_USER_COLLECTION_NAME,
            "range": [0, 1],
            "filters": {
                "$or": [{"username": username}, {
                    "email": username
                }],
                "password":password
            }
        }
        headers = {"content-type": "application/json"}

        # sends this request to database
        async with aiohttp.ClientSession() as session:
            print("Step 3")
            try:
                response = await session.post(f"{HOST}:{DB_PORT}/get_document", data=json.dumps(data), headers=headers)
                response = json.loads(await response.json())
                print(type(response))
                if len(response["documents"]) == 0:
                    res.status = 401
                    res.text = json.dumps({"msg":"Incorrect username/Email or password"})
                    return
                user = response["documents"][0]
                print("Response = ", response)
                res.status = 200
                res.text = json.dumps(user)
                return
            except Exception as error:
                print("Failed to Fetch Admin user from database")
                print(error)
                res.status = 404
                res.text = json.dumps({"msg": error})
                return

class Admin_Get_User_Handler():
    async def on_post(self , req,res):
        body = await req.get_media()
        print("Request on /get_admin_user ---post")
        print("Body = ", body)
        for key, value in body.items():
            print(key, value, type(value))
        try:
            _id = body["_id"]
            output = "*"
            if "output" in body:
                output = body["output"]
        except Exception as error:
            res.status = 403
            res.text = json.dumps({"msg":"_id is required to get user " })
            return
        data = {
            "collection": ADMIN_USER_COLLECTION_NAME,
            "range": [0, 1],
            "_id":_id,
            "output":output

        }
        # },
        # "output":output
        headers = {"content-type": "application/json"}

        # sends this request to database
        async with aiohttp.ClientSession() as session:
            print("Step 3" , data)
            try:
                response = await session.post(f"{HOST}:{DB_PORT}/get_document", data=json.dumps(data), headers=headers)
                response = await response.json()
                print(type(response))
                user = response
                print("Response = ", response)
                res.status = 200
                res.text = json.dumps(user)
                return
            except Exception as error:
                print("Failed to Fetch Admin user from database")
                print(error)
                res.status = 404
                res.text = json.dumps({"msg": error})
                return

class Admin_User_Handler:
    async def on_post(self, req, res):
        body = await req.get_media()
        print("Request on /user_admin ---post")
        print("Body = " , body)
        for key, value in body.items():
            print(key, value, type(value))
        try:
            email = body["email"]
            username = body["username"]
            password = body["password"]
            if(len(email) == 0 or len(username) == 0 or len(password) == 0):
                raise
        except Exception as error:
            res.status = 403
            res.text = json.dumps({"msg": "Email , UserName and Password are required fields "})
            return

        print("[/user_admin -- post -- ]Syntax is correct")
        # Instantitate User Object
        admin_user = AdminUser(email , username , password)
        # insert user on database
        async with aiohttp.ClientSession() as session :
            #first check if user  already exists
            data = {
                "collection" : ADMIN_USER_COLLECTION_NAME,
                "range": [0, -1],
                "filters": {
                    "$or": [{"username": username}, {
                        "email": email
                    }]
                }

            }
            headers = {"content-type": "application/json"}
            try:
                response = await session.post(f"{HOST}:{DB_PORT}/get_document", data=json.dumps(data), headers=headers)
                response = await response.json()
                response = json.loads(response)
                print("response for get_users check is =", response)
                if len(response["documents"]) > 0:
                    msg = "An already Admin Account with this UserName or email exists"
                    print(msg)
                    res.status = 404
                    res.text = json.dumps({"msg":msg})
                    return
            except Exception as error :
                print("Failed to check if Admin user alreay exists on database ", error)
                res.status = 401
                res.text = json.dumps({"msg": error})
                return

            print("Admin User doesn't exists \nNow creating the document")
            data = {
                "collection" : ADMIN_USER_COLLECTION_NAME,
                "data" : admin_user.__dict__
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
                print("Failed to create Admin user on database " , error)
                res.status = 404
                res.text = json.dumps({"msg":error})
                return
    async def on_put(self,req,res):
        body = await req.get_media()
        if "_id" not in body  or "update" not in body:
            msg = "admin user _id or update is missing"
            res.status = 401
            res.text = json.dumps({"msg":msg})
            print(msg)
            return
        print("step 1")
        #sends this request to database
        async with aiohttp.ClientSession() as session :
            data = {
                "collection": ADMIN_USER_COLLECTION_NAME,
                "_id":body["_id"],
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
        if "_id" not in body :
            msg = "admin _id is required to delete admin account"
            res.status = 401
            res.text = json.dumps({"msg":msg})
            print(msg)
            return
        print("step 1")
        #sends this request to database
        async with aiohttp.ClientSession() as session :
            data = {
                "collection": ADMIN_USER_COLLECTION_NAME,
                "_id":body["_id"],
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
                print("Failed to delete Admin user on server")
                print(error)
                res.status = 404
                res.text = json.dumps({"msg":error})
                return



