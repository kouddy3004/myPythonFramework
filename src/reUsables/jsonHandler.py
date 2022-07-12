import json


class JsonHandler:

    def readjson(self, path):
        with open(path) as file:
            jsonDict = json.load(file)
        return jsonDict

    def readjsonByKey(self, path, key):
        with open(path) as file:
            jsonDict = json.load(file)
        return jsonDict[key] if key in jsonDict.keys() else None
