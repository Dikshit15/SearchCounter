from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
app.config["MONGO_URI"] = "mongodb+srv://tapsearch:lhgZh0HJ0xqbTY6w@cluster0-i7yjg.mongodb.net/test?retryWrites=true&w=majority"
mongo = PyMongo(app)
from . import routes
