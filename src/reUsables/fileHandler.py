import os.path
import shutil
from os import path, listdir
from os.path import isfile, join


class FileHandler:

    def removeFileOrFolder(self, filePath):
        if path.exists(filePath):
            if path.isfile(filePath):
                os.remove(filePath)
            else:
                shutil.rmtree(filePath)

    def checkFileOrFolderExist(self, filePath):
        if path.exists(filePath):
            return True
        else:
            return False

    def makeFileOrDirectory(self, filePath):
        if path.exists(filePath) is False:
            os.makedirs(filePath, exist_ok=True)
        return filePath

    def readFileAsString(self, filePath):
        with open(filePath, 'r') as f:
            line = f.read()
            return line

    def readjson(self, path):
        import json
        with open(path) as file:
            jsonDict = json.load(file)
        return jsonDict

    def fetchFileNamesinDir(self, dirPath):
        return [f for f in listdir(dirPath) if isfile(join(dirPath, f))]
