from flask_pymongo import PyMongo
from flask_cors import CORS
import os
import random
import string
import time
from flask import Flask, request, render_template, redirect, url_for
import json
from nltk.tokenize import RegexpTokenizer
from collections import Counter
app = Flask(__name__)
CORS(app)
app.config["MONGO_URI"] = "mongodb://Dikshit:tapchief@cluster0-shard-00-00-avmxv.mongodb.net:27017,cluster0-shard-00-01-avmxv.mongodb.net:27017,cluster0-shard-00-02-avmxv.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority"
mongo = PyMongo(app)


def token_p(indexed_para,s=None):
    response = {
        'status' : False
    }
    if(s is not None):
        data_list = s.split("\n\n")
        para_dict = {}
        p = len(data_list)
        for i in range(0,p):
            if len(data_list[i].strip()) is not 0:
                para_index = get_rand_str(list(indexed_para.keys()) + list(para_dict.keys()))
                para_dict[para_index] = data_list[i]
        if len(para_dict) > 0:
            response = {
                "status" : True,
                "data" : para_dict
            }
    return response

def tokenize_words(s=None):
    response = {
        "status" : False
    }
    tokenizer = RegexpTokenizer(r'\w+')
    if s is not None:
        t_list = tokenizer.tokenize(s)
        t_list = [x.lower() for x in t_list]
        counts = Counter(t_list)
         response = {
            "status": True,
            "count": counts
        }
    return response

def get_index(invert_index, indexed_para, text=None):
    response = {
        "status" : False
    }
    if text is not None:
        paras_response = token_p( indexed_para, s=text)
        if paras_response['status'] is False: return response
        paras = paras_response['data']
        for i in paras.keys():
            words_response = tokenize_words(s=paras[i])
            if words_response["status"] is not False: words = words_response["count"]
                for word in words:
                    if word in invert_index.keys():
                        invert_index[word].append((i,words[word]))
                    else:
                        invert_index[word] = []
                        invert_index[word].append((i,words[word]))
        for i in invert_index.keys():
            invert_index[i] = sorted(invert_index[i], key = lambda x: x[1])
        indexed_para.update(paras)
        response = {
            "status" : True,
            "data":{
                "invert_index" : invert_index,
                "para_dict" : indexed_para
                }
        }
    return response

def random_dig(string_length=12):
    al_list = string.ascii_letters + string.digits
    return ''.join(random.choice(al_list) for i in range(string_length))

def get_rand_str(para_keys):
    s = random_dig(15)
    while True:
        if s in para_keys:
            s = random_dig(15)
        else:
            break
    return s


@app.route('/indexData', methods = ['POST'])
def indexData():
    content = request.get_json()
    response = {
        "invert_index" : {},
        "dictionary_paragraph" : {}
    }
    pointer_to_data = mongo.db.words.find({}) #find from amongst all the data we have
    for i in pointer_to_data:
        response["invert_index"][i["word"]] = i["index"]
    pointer_to_data = mongo.db.paragraphs.find({})
    for i in pointer_to_data:
        response["dictionary_paragraph"][i["id"]] = i["paragraph"]
    mongo.db.words.remove({})
    mongo.db.paragraphs.remove({})
    if len(content["text"]) == 0:
        return {
            "success" : False
        }

    response = get_index(response["invert_index"], response["dictionary_paragraph"],content["text"], )["data"]

    for i in response['invert_index']:
        mongo.db.words.insert_one({"word":i,"index":response["invert_index"][i]})
    for i in response["dictionary_paragraph"]:
        mongo.db.paragraphs.insert_one({"id": i, "paragraph":response["dictionary_paragraph"][i]})
    return {
        "success": True
    }

@app.route("/search", methods = ["GET"])
def searchData():
    plist = []
    word = request.args.get("search", type=str)
    pointer_to_data = mongo.db.words.find_one({"word" : word})
    if pointer_to_data is None:
        return {"complete" : True, "body": []}
    else:
        index = pointer_to_data["index"]


    index = sorted(index, key = lambda x: x[1])[::-1]

    len_index = len(index)
    for i in range(0, min(10, len_index)):
        plist.append(mongo.db.paragraphs.find_one({"id" : index[i][0]})["paragraph"])
    return {
        "success" : True,
        "body" : plist
    }

@app.route("/clear", methods = ["DELETE"])
def clear():
    mongo.db.words.remove({})
    mongo.db.paragraphs.remove({})
    return {
        "success": True
    }

@app.route("/getWords", methods = ["GET"])
def getWords():
    words = []
    pointer_to_data = mongo.db.words.find({}, { "_id": 0, "index":0})
    for i in pointer_to_data:
        words.append(i["word"])
    return {
        "success" : True,
        "body" : {
            "words" : words
        }
    }
