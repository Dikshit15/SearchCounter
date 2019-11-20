from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
# app.config["MONGO_URI"] = "mongodb://localhost:27017/tapsearch"
app.config["MONGO_URI"] = "mongodb://Dikshit:tapchief@cluster0-shard-00-00-avmxv.mongodb.net:27017,cluster0-shard-00-01-avmxv.mongodb.net:27017,cluster0-shard-00-02-avmxv.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority"
mongo = PyMongo(app)
from . import routes
