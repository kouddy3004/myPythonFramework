import os

import pytest
from pytest_bdd import given, then, parsers

from src.baseScripts.masterDriver import MasterDriver
from src.reUsables.allureHandler import AllureHandler
from src.testWebUI.commonUIScripts.commonUIFunction import CommonUiFunction

masterDriver = MasterDriver()
allureHandler = AllureHandler()

commonUiFunction = CommonUiFunction()


@given(u'Conftest For Common Function')
def commonFunction(env):
    print("Write For Common Function like login Page")
