import os

from jproperties import Properties

from src.reUsables.filePath import FilePath


class PropertyHandler:
    config = None
    projectPath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    def __init__(self, propertyName):
        self.config = Properties()
        filePath = FilePath()
        propertyPath = filePath.getPath("propertiesPath")
        if ".properties" not in propertyName:
            propertyName = propertyName + ".properties"
        with open(os.path.join(propertyPath, propertyName),
                  'rb') as readProps:
            self.config.load(readProps)

    def readProperties(self):
        properties = {}
        for item in self.config.items():
            properties[item[0]] = item[1].data
        return properties

    def readProperty(self, fileKey):
        return self.config.get(fileKey).data
