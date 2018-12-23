from bottle import template
import json
from os import listdir
from os.path import isfile, join

JSON_FOLDER = './data'
AVAILABE_SHOWS = ["7", "66", "73", "82", "112", "143", "175", "216", "1371", "1871","2993", "305"]

def getVersion():
    return "0.0.1"

def getJsonFromFile(showName):
    try:
        return template("{folder}/{filename}.json".format(folder=JSON_FOLDER, filename=showName))
    except:
        return "{}"

def getListDictionary():
    try:
        json_files = [f for f in listdir('./data/') if isfile(join('./data/', f))]
        shows_list = []
        for fl in json_files:
            with open('./data/' + fl, encoding="UTF-8") as f:
                data = json.load(f)
                shows_list.append(data)
        return shows_list
    except:
        return "{}"