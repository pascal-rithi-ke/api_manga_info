import os
import pymongo
from bson import json_util
import json
from flask import Flask, jsonify
from flask_cors import CORS
#from mal import MangaSearch,Manga #Librairy use for add Manga data by Web scraping MyAnimeList Website data



ID = os.getenv('ID_MONGO')
PASS = os.environ.get('PASS_MONGO')

DATABASE_URL =f'mongodb+srv://{ID}:{PASS}@cluster0.sp2ay.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
#DATABASE_URL = 'mongodb://localhost:27017/'

client=pymongo.MongoClient(DATABASE_URL)
mydb = client['Manga_info']
mycol = mydb['manga_collection']
mycol2 = mydb["explain_moment"]

app = Flask(__name__)
CORS(app)

@app.route("/")
def detail():
        #List all Mangas plus some details
        output = []
        for x in mycol.find():
                output.append({'id' : x['id'],'name':x['name'],'autor':x['autor'],'img':x['url_img'],'score':x['score'],'synopsis':x['synopsis'],'genre':x['genre'],})
        #Return the data array as JSON format
        response = jsonify({'results':output})
        response.headers.add("Access-Control-Allow-Origin","*")
        return response

@app.route('/<id>')
def getSoloManga(id):
        #Search More info Manga By Id
        mydoc = mycol2.find({'id':id})
        output = []
        for x in mydoc:
                output.append(x)
        #Convert ObjectId mongodb unique Key for each data, permit to use as unique key for react-native navigation
        conv = json.loads(json_util.dumps(output))
        #Return the data array as JSON format
        response = jsonify({'results':conv})
        response.headers.add("Access-Control-Allow-Origin","*")
        return response

if __name__ == "__main__":
    app.run()


#Add Manga in database " mycol" , write information in terminal
#nb = 0
#scan = input('enter manga name :')
#def getInfo(scan):
#        search = MangaSearch(scan)
#        manga_id = search.results[nb].mal_id
#        PlusInfo = Manga(manga_id)
#        autor = PlusInfo.authors
#        resume = PlusInfo.synopsis
#        title = search.results[nb].title
#        img = search.results[nb].image_url
#        score = search.results[nb].score
#        synopsis = search.results[nb].synopsis
#        genre = input('enter genre :')
#        print(manga_id,'\n', autor, '\n', title, '\n', img, '\n', score, '\n', synopsis, '\n',genre)
#        mydict = {"id": manga_id,"name":title,"autor":autor,"url_img":img,"score":score,"synopsis":resume,"genre":genre}
#        x = mycol.insert_one(mydict)
#def new_manga():
#        continuer = True
#        while continuer :
#                choix = input("Do you want to continue ? o/n: ")
#                if choix == ('o'):
#                        new_manga = input("enter new manga :")
#                        getInfo(new_manga)
#                else:
#                        print("End Program")
#                        continuer = False
#getInfo(scan)
#new_manga()
