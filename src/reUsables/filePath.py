import os


class FilePath:
    projectPath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    def getPath(self, fileName=None):
        filePaths = {
            "xmlFiles": os.path.join(self.projectPath, "resources", "xmlFiles"),
            "csvFiles": os.path.join(self.projectPath, "resources", "csvFiles"),
            "testCasePath": os.path.join(self.projectPath, "resources", "testCases"),
            "tcInputData": os.path.join(self.projectPath, "resources", "inputData"),
            "mail": os.path.join(self.projectPath, "resources", "properties"),
            "testDataPath": os.path.join(self.projectPath, "resources", "expectedOutput", "testData"),
            "mail": os.path.join(self.projectPath, "resources", "properties"),
            "driver": os.path.join(self.projectPath, "utils", "webUiResources", "webDrivers"),
            "webServiceEnv": os.path.join(self.projectPath, "utils", "webServicesResources"),
            "webUiEnv": os.path.join(self.projectPath, "utils", "webUiResources"),
            "instantClient": os.path.join(self.projectPath, "utils", "instant_client"),
            "shellScripts": os.path.join(self.projectPath, "utils", "shellScripts"),
            "batchExecution": os.path.join(self.projectPath, "utils", "batchExecution"),
            "sqlPath": os.path.join(self.projectPath, "utils", "sql"),
            "cookiePath": os.path.join(self.projectPath, "utils", "webServicesResources", "cookies"),
            "inpRequestPath": os.path.join(self.projectPath, "utils", "webServicesResources", "input"),
            "expResponsePath": os.path.join(self.projectPath, "utils", "webServicesResources", "expectedRes"),
            "batchListPath": os.path.join(self.projectPath, "utils", "batchExecution"),
            "reportPath": os.path.join(self.projectPath, "reports"),
            "screenShotPath": os.path.join(self.projectPath, "reports", "screenShots"),
            "logPath": os.path.join(self.projectPath, "reports", "logs"),
            "featurePath": os.path.join(self.projectPath, "test", "feature"),
            "propertiesPath": os.path.join(self.projectPath, "resources", "properties"),
            "expectedOutput": os.path.join(self.projectPath, "resources", "expectedOutput")
        }
        if fileName in filePaths.keys():
            return filePaths.get(fileName)
        else:
            return None
