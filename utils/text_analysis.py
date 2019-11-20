from nltk.tokenize import RegexpTokenizer
from collections import Counter
from .generate_random import random_string_digits

def get_random_string(paragraph_keys):
    s = random_string_digits(15)
    while True:
        if s in paragraph_keys:
            s = random_string_digits(15)
        else:
            break
    return s

def tokenize_paragraph(indexed_paragraph,s=None):
    result = {
        'status' : False
    }
    if(s is not None):
        data_list = s.split("\n\n")
        paragraph_dict = {}
        for i in range(0,len(data_list)):
            if len(data_list[i].strip()) is not 0:
                paragraph_index = get_random_string(indexed_paragraph.keys() + paragraph_dict.keys())
                paragraph_dict[paragraph_index] = data_list[i]
        if len(paragraph_dict) > 0:
            result = {
                "status" : True,
                "data" : paragraph_dict
            }
    return result

def tokenize_words(s=None):
    result = {
        "status" : False
    }
    tokenizer = RegexpTokenizer(r'\w+')
    if s is not None:
        token_list = tokenizer.tokenize(s)
        token_list = [x.lower() for x in token_list]
        counts = Counter(token_list)
        result = {
            "status": True,
            "count": counts
        }
    return result

def get_inverted_index(inverted_index, indexed_paragraph, text=None):
    result = {
        "status" : False
    }
    if text is not None:
        paragraphs_result = tokenize_paragraph( indexed_paragraph, s=text)
        if paragraphs_result['status'] is False:
            return result
        paragraphs = paragraphs_result['data']
        for i in paragraphs.keys():
            words_result = tokenize_words(s=paragraphs[i])
            if words_result["status"] is not False:
                words = words_result["count"]
                for word in words:
                    if word in inverted_index.keys():
                        inverted_index[word].append((i,words[word]))
                    else:
                        inverted_index[word] = []
                        inverted_index[word].append((i,words[word]))
        for i in inverted_index.keys():
            inverted_index[i] = sorted(inverted_index[i], key = lambda x: x[1])
        indexed_paragraph.update(paragraphs)
        result = {
            "status" : True,
            "data":{
                "inverted_index" : inverted_index,
                "paragraph_dict" : indexed_paragraph
                }
        }
    return result
