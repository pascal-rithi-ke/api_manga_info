import os
from bson import json_util,ObjectId
import json
import pymongo
from flask import Flask, jsonify

ID = os.getenv('ID_MONGO')
PASS = os.environ.get('PASS_MONGO')

DATABASE_URL =f'mongodb+srv://{ID}:{PASS}@cluster0.sp2ay.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'

client=pymongo.MongoClient(DATABASE_URL)
mydb = client['Manga_info']
mycol = mydb['manga_collection']
mycol2 = mydb["explain_moment"]

app = Flask(__name__)

@app.route("/home", methods = ["GET"])
def detail():
        #List all Mangas plus some details
        output = []
        for x in mycol.find():
                output.append({'id' : x['id'],'name':x['name'],'autor':x['autor'],'img':x['url_img'],'score':x['score'],'synopsis':x['synopsis'],'genre':x['genre'],})
        response = jsonify({'results':output})
        response.headers.add("Access-Control-Allow-Origin","*")
        return response

@app.route('/home/<id>', methods = ['GET'])
def getSoloManga(id):
        #Search More info Manga By Id
        mydoc = mycol2.find({'id':id})
        output = []
        for x in mydoc:
                output.append(x)
        conv = json.loads(json_util.dumps(output))
        response = jsonify({'results':conv})
        response.headers.add("Access-Control-Allow-Origin","*")
        return response

if __name__ == "__main__":
    app.run()