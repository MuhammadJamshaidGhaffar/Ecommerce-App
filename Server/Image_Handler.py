import aiofiles
import falcon
import os
import uuid , json


path = "./Images/"

class Image:
    async def on_get(self,req,res):
        print(req)
        # checking if id is present in query parameters
        for key , value in req.params.items():
            print(key , value , type(value))
        if ("id" not in req.params):
            res.status = falcon.HTTP_404
            res.text = "Id Parameter is not present!"
            return
        id = req.params['id']
        # opening image file
        try:
            image = await aiofiles.open(f"{path}{id}.jpeg" , 'rb')
            res.stream = image
            res.content_type = falcon.MEDIA_JPEG
            return
        except Exception as error:
            res.status = 200
            res.text = json.dumps({"msg":str(error)})
            return

    async def on_post(self , req, res):
        # create directory if not exists
        if not os.path.exists(path):
            os.makedirs(path)

        try:
            id = uuid.uuid4()
            # reading image from req.stream
            image = await req.stream.read()
            file = await aiofiles.open(f"{path}{id}.jpeg" , 'wb')
            #writing image to a file
            await file.write(image)
            await file.close()
            return
        except Exception as error:
            res.status = 500
            res.text = json.dumps({"msg":str(error)})





