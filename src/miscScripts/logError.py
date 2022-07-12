from src.baseScripts.masterDriver import MasterDriver
from src.reUsables.fileHandler import FileHandler
import os

file = FileHandler()
masterDriver = MasterDriver()


def loggingTheError(loggedError, errorMsg):
    ap = "w"
    nl=""
    errlogPath = os.path.join(masterDriver.getfilePathProperties("reportPath"), "errorLog.log")
    if isinstance(loggedError, dict):
        tcId = loggedError["Test_Case_Id"]
        scenario = loggedError["Scenario"]
        tcName = loggedError["Test_Case_Name"]
    if isinstance(loggedError, list):
        tcId = loggedError[0]["Test_Case_Id"]
        scenario = loggedError[0]["Scenario"]
        tcName = loggedError[0]["Test_Case_Name"]

    if file.checkFileOrFolderExist(errlogPath):
        ap = "a"
    with open(errlogPath, ap) as file1:
        if ap == "a":
            nl = "\n\n"
        loggedError = "{3}{0} --> {1} --> {2}\n     =======================\n".format(tcId, scenario, tcName, nl) \
                      + str(errorMsg)
        file1.writelines(loggedError)
