from app import app, mongo
from utils.text_analysis import get_inverted_index
from flask import request, render_template

@app.route("/")
def start_page():
    return render_template("hello.html")

@app.route('/index', methods = ['POST'])
def index():
    content = request.get_json()
    result = {
        "inverted_index" : {},
        "paragraph_dict" : {}
    }
    cursor = mongo.db.words.find({})
    for i in cursor:
        result["inverted_index"][i["word"]] = i["index"]
    cursor = mongo.db.paragraphs.find({})
    for i in cursor:
        result["paragraph_dict"][i["id"]] = i["paragraph"]
    if len(content["text"]) == 0:
        print ("erroor")
        return {
            "success" : False
        }
    result = get_inverted_index(result["inverted_index"], result["paragraph_dict"],content["text"], )["data"]
    print(result)
    mongo.db.words.remove({})
    mongo.db.paragraphs.remove({})
    for i in result['inverted_index']:
        mongo.db.words.insert_one({"word":i,"index":result["inverted_index"][i]})
    for i in result["paragraph_dict"]:
        mongo.db.paragraphs.insert_one({"id": i, "paragraph":result["paragraph_dict"][i]})
    return {
        "success": True
    }
     
@app.route("/search", methods = ["GET"])
def search():
    word = request.args.get("search", default="SOmethign", type=str)
    print (word)
    cursor = mongo.db.words.find_one({"word" : word})
    if cursor is None:
        return {"complete" : True, "body": []}
    index = cursor["index"]
    print (index)
    index = sorted(index, key = lambda x: x[1])[::-1]
    print (index)
    paragraph_list = []
    for i in range(0, min(10, len(index))):
        paragraph_list.append(mongo.db.paragraphs.find_one({"id" : index[i][0]})["paragraph"])
    print (paragraph_list)
    result = {
        "success" : True,
        "body" : paragraph_list
    }
    return result

@app.route("/clear", methods = ["DELETE"])
def clear():
    mongo.db.words.remove({})
    mongo.db.paragraphs.remove({})
    result = {
        "success": True
    }
    return result

@app.route("/getallwords", methods = ["GET"])
def get_all_words():
    cursor = mongo.db.words.find({}, { "_id": 0, "index":0})
    words = []
    for i in cursor:
        print (i)
        words.append(i["word"])
    return {
        "success" : True,
        "body" : {
            "words" : words
        }
    }