# Importing necessary imports
import optparse
import os
import subprocess
import sys

# Set Project and Module Path and Opt Parsing
projectPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(projectPath)
from src.reUsables.fileHandler import FileHandler
from src.reUsables.pandaHandler import PandaHandler
from src.reUsables.miscScripts import MiscScripts

file = FileHandler()
parser = optparse.OptionParser()
parser.add_option("-a", "--app", dest="app",
                  help="assigning which app to run")
parser.add_option("-f", "--pyTestFile", dest="pyTestFile",
                  help="Name of the pytest file. For running all the pyTest files, please leave empty")
parser.add_option("-t", "--tags", dest="tags",
                  help="Assign 'unit' for Unit Test or 'regression' for Regression Test. By default unit case used to run")
parser.add_option("--b", dest="browser",
                  help="Setting browser by adding: 'chrome' for Google Chrome, 'firefox' for Mozilla Firefox ")
parser.add_option("--h", dest="headLess",
                  help="assign 'Y' to run tests in headless mode")
parser.add_option("-p", "--parallel", dest="parallel",
                  help="Assign number of threats to run test parallel")

(opts, args) = parser.parse_args()
app = ''
pyFile = ''
tags = 'unit'
browser = ''
headless = ''
parallel = 4

if opts.pyTestFile is not None:
    pyFile = opts.pyTestFile
if opts.tags is not None:
    tags = opts.tags
if opts.app is not None:
    app = opts.app
if opts.browser is not None:
    browser = opts.browser
if opts.headLess is not None:
    headless = opts.headLess
if opts.parallel is not None:
    parallel = opts.parallel

pyFilePath = os.path.join(projectPath, "test", "test_steps", app, pyFile)
reportFilePath = os.path.join(projectPath, "reports")
allureLogFilePath = os.path.join(reportFilePath, "allureLogs")
allureReportFilePath = os.path.join(reportFilePath, "allure-report")
logPath = os.path.join(reportFilePath, "logs")
pytestHtmlReport = os.path.join(reportFilePath, "pyHtmlReport.html")

# Running Feature file
cmd = 'pytest -v -s -n {3} -m {0} --b={1} --h={2} --disable-warnings --alluredir={4} {5} --html={6} --self-contained-html --clean-alluredir' \
    .format(tags, browser, headless, parallel, allureLogFilePath, pyFilePath, pytestHtmlReport)

subprocess.run(cmd, shell=True)


def generateSummaryReport(fileName, summaryResult):
    from src.baseScripts.masterDriver import MasterDriver
    master = MasterDriver()
    master.generateSummaryReport(fileName, summaryResult)


def alignFeatureReport():
    tempPath = os.path.join(projectPath, "reports", "temp")
    jsonFileNames = os.listdir(tempPath)
    summaryResult = []
    featureFileNames = []
    for fileName in jsonFileNames:
        with open(os.path.join(tempPath, fileName), "r") as file:
            import json
            summaryResult.append(json.load(file))
        for result in summaryResult:
            if isinstance(result, dict):
                featureFileNames.append(result["Services"])
            if isinstance(result, list):
                for reps in result:
                    featureFileNames.append(reps["Services"])
    featureFileNames = set(featureFileNames)
    print(featureFileNames)
    for fileName in featureFileNames:
        testCases = []
        for result in summaryResult:
            print(result)
            if isinstance(result, dict):
                if result["Services"] in fileName:
                    testCases.append(result)
            if isinstance(result, list):
                for reps in result:
                    if reps["Services"] in fileName:
                        testCases.append(reps)
        generateSummaryReport(fileName, testCases)
        print(fileName + " ==> " + str(len(testCases)))


# Generating Allure Report
cmd = 'allure generate {0}  --clean -o {1}'.format(allureLogFilePath, allureReportFilePath)
print(cmd)
# subprocess.run(cmd, shell=True)

cmd = 'allure open {0} -h localhost'.format(allureReportFilePath)
print(cmd)
# subprocess.run(cmd, shell=True)
#
alignFeatureReport()
#file.removeFileOrFolder(os.path.join(projectPath, "reports", "temp"))
xcelReports = os.path.join(projectPath, "reports", "excelReports")
xlFileNames = os.listdir(xcelReports)
ph = PandaHandler()
for xlFIle in xlFileNames:
    ph.reportFormatting(os.path.join(xcelReports, xlFIle))

misc = MiscScripts()
# misc.archivingReportsInVM()
