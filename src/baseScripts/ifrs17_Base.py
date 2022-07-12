from src.baseScripts.masterDriver import MasterDriver


class Ifrs17_Base:

    def assignFUllFLowTestCases(self, fileName, testCase):
        if testCase["LC_TestCase"]:
            masterDriver = MasterDriver()
            tcId = testCase["Test_Case_Id"]
            loaName = testCase["LOA_Name"]
            le_hier = testCase["LE_Hierarchy"]
            le_member = testCase["LE_Member"]
            lob_hier = testCase["Lob_Hierarchy"]
            lob_member = testCase["Lob_Member"]
            run_type = testCase["RunType"]
            testCase.update(masterDriver.assignTestCases(fileName, "LC", testCase["LC_TestCase"]))
            testCase["Test_Case_Id"] = tcId
            testCase["LE_Hierarchy"] = le_hier
            testCase["LE_Member"] = le_member
            testCase["Lob_Hierarchy"] = lob_hier
            testCase["Lob_Member"] = lob_member
            testCase["RunType"] = run_type
            testCase["LOA_Name"] = loaName
        return testCase
