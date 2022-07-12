import os

import pytest
from pytest_bdd import scenarios, scenario, then

from src.baseScripts.masterDriver import MasterDriver
from src.reUsables.allureHandler import AllureHandler

masterDriver = MasterDriver()
demoFeature = os.path.join(masterDriver.getfilePathProperties("featurePath"), "demoApp1", "demoApp1UI.feature")
scenarioName = ""

if scenarioName:
    @scenario(demoFeature, scenarioName)
    def test_MyScenario():
        pass
else:
    scenarios(demoFeature)

allureHandler = AllureHandler()


@then("For Demo App1 UI")
def demoApp2UI():
    print("For Demo App1 Web UI")
    if '01' in pytest.scenarioResult["Test_Case_Id"]:
        pytest.scenarioResult["Execution_Status"] = "PASS"
    else:
        pytest.scenarioResult["Execution_Status"] = "FAIL"
