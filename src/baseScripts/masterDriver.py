import os

import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from src.reUsables.dbHandler import DbHandler
from src.reUsables.fileHandler import FileHandler
from src.reUsables.filePath import FilePath
from src.reUsables.pandaHandler import PandaHandler
from src.reUsables.propertyHandler import PropertyHandler


class MasterDriver:
    fileHandler = FileHandler()

    def getProperties(self, propertyName, key):
        proHandler = PropertyHandler(propertyName)
        return proHandler.readProperty(key)

    def getfilePathProperties(self, key):
        filePath = FilePath()
        return filePath.getPath(key)

    def setWebDriver(self, browser, headless=False, setProxy=False):
        driverPath = self.getfilePathProperties("driver")
        driver = None
        if browser == "chrome":
            options = webdriver.ChromeOptions()
        elif browser == "firefox":
            options = webdriver.FirefoxOptions()
        options.add_argument("--disable-xss-auditor")
        options.add_argument("--disable-web-security")
        options.add_argument("--allow-running-insecure-content")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-setuid-sandbox")
        options.add_argument("--disable-webgl")
        options.add_argument("--disable-popup-blocking")
        options.add_argument('ignore-certificate-errors')

        if headless:
            options.add_argument("--headless")

        if setProxy:
            proxy = {
                'http': 'http://www-proxy-hqdc.us.oracle.com:80',
                'https': 'http://www-proxy.us.oracle.com:80',
            }
            os.environ["HTTP_PROXY"] = proxy["http"]
            os.environ["HTTPS_PROXY"] = proxy["https"]

        if browser == "chrome":
            driverPath = ChromeDriverManager(path=driverPath).install()
            os.environ["HTTP_PROXY"] = ""
            os.environ["HTTPS_PROXY"] = ""
            driver = webdriver.Chrome(executable_path=driverPath, options=options)
        elif browser == "firefox":
            driverPath = GeckoDriverManager(path=driverPath).install()
            os.environ["HTTP_PROXY"] = ""
            os.environ["HTTPS_PROXY"] = ""
            driver = webdriver.Firefox(executable_path=driverPath, options=options)

        return driver

    def getWebServiceEnvProperties(self, propertyFile):
        envPropsPath = self.getfilePathProperties("webServiceEnv")
        print(os.path.join(envPropsPath, propertyFile))
        proHandler = PropertyHandler(os.path.join(envPropsPath, propertyFile))
        return proHandler.readProperties()

    def getWebUIEnvProperties(self, propertyFile):
        envPropsPath = self.getfilePathProperties("webUiEnv")
        proHandler = PropertyHandler(os.path.join(envPropsPath, propertyFile))
        return proHandler.readProperties()

    def setSessionWebServices(self, setProxy=False):
        se = requests.session()
        if setProxy:
            proxy = {
                'http': 'http://www-proxy-hqdc.us.oracle.com:80',
                'https': 'http://www-proxy.us.oracle.com:80',
            }
            se.proxies = proxy
        return se

    def assignTestCases(self, fileName, sheet, tcId):
        tcPath = os.path.join(self.getfilePathProperties("testCasePath"), fileName)
        pandaHandler = PandaHandler()
        try:
            testCase = pandaHandler.readExcelByKey(tcPath, sheet, "Test_Case_Id", tcId, str)
            return testCase[list(testCase.keys())[0]]

        except Exception as e:
            print(e)

    def generateSummaryReport(self, fileName, result):
        pandaHandler = PandaHandler()
        reportPath = os.path.join(self.getfilePathProperties("reportPath"), "excelReports")
        return pandaHandler.generateSummaryReport(reportPath, fileName, result)

    def logError(self, fileName, logs):
        logPath = os.path.join(self.getfilePathProperties("reportPath"), fileName + "_errLog.log")
        with open(logPath, "w") as fileLog:
            for log in logs:
                fileLog.write(str(log))
        return logPath

    def makeSpaceForScreenShots(self):
        return self.fileHandler.makeFileOrDirectory(self.getfilePathProperties("screenShotPath"))

    def setDatabase(self, envDetails):
        dbDetails = self.getDbDetails(envDetails)
        hostName = dbDetails["jdBC"].split(":")[0]
        port = dbDetails["jdBC"].split(":")[1]
        serviceName = dbDetails["jdBC"].split(":")[2]
        dbHandler = DbHandler()
        dbConn = dbHandler.connectIntoOracle(dbDetails['dbUserName'], dbDetails['dbPassword'], hostName, port,
                                             serviceName)

        return dbConn

    def getDbDetails(self, envDetails):
        return {
            "dbUserName": envDetails["dbSchema"].split("/")[0],
            "dbPassword": envDetails["dbSchema"].split("/")[-1],
            "jdBC": envDetails["JdbcUrl"].split("@")[-1]
        }

    def removeFileOrFolder(self, filePath):
        self.fileHandler.removeFileOrFolder(filePath)
