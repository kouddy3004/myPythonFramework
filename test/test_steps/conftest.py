import copy

import pytest
from pytest_bdd import given, then, parsers

from src.baseScripts.ifrs17_Base import Ifrs17_Base
from src.miscScripts.logError import *
from src.reUsables.allureHandler import AllureHandler
from src.reUsables.dbHandler import DbHandler
from src.reUsables.fileHandler import FileHandler
from src.testWebUI.commonUIScripts.commonUIFunction import CommonUiFunction

masterDriver = MasterDriver()
allureHandler = AllureHandler()
file = FileHandler()


def pytest_bdd_before_scenario(request, feature, scenario):
    print("\nBefore Scenario")
    pytest.remoteSession = None
    pytest.scenarioResult = None
    pytest.serviceSession = None
    pytest.driver = None
    pytest.featureFileName = feature.filename
    pytest.errorLog = None
    setProxy = False
    setNoProxy = False
    try:
        if "setProxy" in scenario.tags:
            setProxy = True
        if "webService" in scenario.tags:
            pytest.serviceSession = masterDriver.setSessionWebServices(setProxy)
            print("Web Services Session Created")
        if "webUi" in scenario.tags:
            pytest.screenshotPath = masterDriver.makeSpaceForScreenShots()
            headless = False
            if headLess:
                headless = True
            if browser:
                pytest.driver = masterDriver.setWebDriver(browser, headless)
            else:
                if "chrome" in scenario.tags:
                    pytest.driver = masterDriver.setWebDriver("chrome", headless, setProxy)
                elif "firefox" in scenario.tags:
                    pytest.driver = masterDriver.setWebDriver("firefox", headless, setProxy)
            pytest.driver.delete_all_cookies()
            print("Web Driver has been initialized")
    except Exception as e:
        print(e)
        assert False


def pytest_bdd_after_scenario(request, feature, scenario):
    print("\nAfter Scenario")
    service = ""
    if pytest.scenarioResult:
        import random
        import json
        if "webService" in scenario.tags:
            service = "_webService"
        elif "webUi" in scenario.tags:
            service = "_webUi"
        with open(os.path.join(masterDriver.getfilePathProperties("reportPath"), "temp",
                               "temp" + "_" + str(random.randint(1, 1000))
                               + ".json"), "w") as file1:
            if isinstance(pytest.scenarioResult, dict):
                pytest.scenarioResult["Services"] += service
                json.dump(pytest.scenarioResult, file1)
            elif isinstance(pytest.scenarioResult, list):
                for reps in pytest.scenarioResult:
                    reps["Services"] += service
                    if len(reps["Execution_Status"]) == 0:
                        reps["Execution_Status"] = "Not Executed"
                json.dump(pytest.scenarioResult, file1)
            if pytest.errorLog:
                loggingTheError(pytest.scenarioResult, pytest.errorLog)
    if pytest.remoteSession is not None:
        pytest.remoteSession.close()
        print("Remote Session Closed")
    if pytest.serviceSession is not None:
        pytest.serviceSession.close()
        print("Session Closed")
    if pytest.driver is not None:
        pytest.driver.quit()
        print("Driver closed")


def pytest_configure(config):
    import sys
    if sys.platform == "win32":
        dbHandler = DbHandler()
        dbHandler.setInstantClient(masterDriver.getfilePathProperties("instantClient"))
    reportFilePath = masterDriver.getfilePathProperties("reportPath")
    allureLogFilePath = os.path.join(reportFilePath, "allureLogs")
    file.removeFileOrFolder(reportFilePath)
    file.makeFileOrDirectory(allureLogFilePath)
    file.makeFileOrDirectory(os.path.join(reportFilePath, "temp"))
    file.makeFileOrDirectory(os.path.join(reportFilePath, "excelReports"))


def pytest_addoption(parser):
    parser.addoption("--b")
    parser.addoption("--h")


@pytest.fixture(scope="function", autouse=True)
def cmdOpts(pytestconfig):
    global browser
    global headLess
    browser = pytestconfig.getoption("b")
    headLess = pytestconfig.getoption("h")


@pytest.fixture(scope="module", autouse=True)
def featureSetup():
    pytest.featureResult = []
    pytest.featureFileName = None
    pytest.screenshotPath = None
    pytest.dbConn = None
    yield
    print('\nAfter Feature')
    reportFileName = os.path.split(pytest.featureFileName)
    reportFileName = reportFileName[-1].split(".feature")[0]
    if pytest.dbConn is not None:
        pytest.dbConn.dispose()
        print("DB connection closed")
    if pytest.driver is not None:
        pytest.driver.quit()
        print("Driver closed")
    allureHandler.allureLogs("All the drivers and DB configurations has been closed for the featue {0}.feature"
                             .format(reportFileName))


@given(parsers.parse("Get {app} {webDetails} Env Details"), target_fixture="env")
def getEnvDetails(app, webDetails):
    if webDetails.upper() == "WEBSERVICES":
        env = masterDriver.getWebServiceEnvProperties(app)
    elif webDetails.upper() == "WEBUI":
        env = masterDriver.getWebUIEnvProperties(app)
    if "JdbcUrl" in env:
        pytest.dbConn = masterDriver.setDatabase(env)
    allureHandler.allureLogs("Given : Got env details for " + app)

    return env


@given(parsers.parse('Assign Test Cases {tc} from  {sheetName} sheet in {fileName}'),
       target_fixture="testCase")
def assignTestCases(fileName, tc, sheetName):
    if "." not in fileName:
        fileName = fileName + ".xlsx"
    testCase = masterDriver.assignTestCases(fileName, sheetName, tc)
    if testCase is None:
        assert False, "Unable to fetch test case details for " + tc
    if "IFRS17".upper() in fileName.upper():
        ifrs17Base = Ifrs17_Base()
        if "LC_TestCase" in testCase.keys():
            testCase = ifrs17Base.assignFUllFLowTestCases(fileName, testCase)
    pytest.scenarioResult = copy.deepcopy(testCase)
    print(pytest.scenarioResult)
    allureHandler.allureLogs("Given : Test Cases assigned for " + tc)
    return testCase


@then(parsers.parse('Take screenshot and naming it as {fileName}'))
def takeScreenshot(fileName):
    screenshot = os.path.join(pytest.screenshotPath, fileName + ".png")
    print(screenshot)
    pytest.driver.get_screenshot_as_file(screenshot)


@given("Launch url")
def launchUrl(env):
    print("Url : " + env["URL"])
    commonUiFunction = CommonUiFunction()
    commonUiFunction.launchUrl(pytest.driver, env["URL"])


@given("Establish Remote Connection")
def makeRemoteConnection(env):
    if "remoteName" in env.keys():
        hostName = env["remoteName"].split("@")[0]
        userName = env["remoteName"].split("@")[1].split("/")[0]
        password = env["remoteName"].split("@")[1].split("/")[1]
        import paramiko
        try:
            pytest.remoteSession = paramiko.SSHClient()
            pytest.remoteSession.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            pytest.remoteSession.connect(hostName, username=userName, password=password)

        except Exception as e:
            print("UNable to create Remote Session because of below reason : ")
            print(e)
    else:
        print("Unable to establish Connection. Please add remoteName in Environment properties in "
              "the format hostName@userName/Password")
