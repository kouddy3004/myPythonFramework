import os.path
import xml.etree.ElementTree as et

import pandas as pd

from src.reUsables.formatter import *


class PandaHandler:

    @staticmethod
    def getInstance():
        return PandaHandler()

    def tranform_xml(self, xmlroot, findBy):
        xmlList = []
        for xml in xmlroot.findall(findBy):
            xmlDict = {}
            for value in xml:
                xmlDict[value.tag] = value.text
            xmlList.append(xmlDict)
        return xmlList

    def readXml(self, filePath, findBy="/feeds"):
        xmlDF = pd.DataFrame(self.tranform_xml(et.parse(filePath).getroot(), findBy))
        return xmlDF

    def readCsv(self, filePath):
        return pd.read_csv(filePath, index_col=False)

    def readExcel(self, filePath, sheet=0, type=None):
        return pd.read_excel(filePath, sheet_name=sheet, dtype=type)

    def readExcelByKey(self, filePath, sheet=0, columnName=None, key=None, type=None):
        if columnName and key:
            try:
                row = self.readExcel(filePath, sheet, type)
                row = row[(row[columnName] == key)]
                row = row.fillna('').to_dict(orient="index")
                return row
            except Exception as e:
                print(e)
                return None

    def generateSummaryReport(self, filePath, fileName, results):
        filePath = os.path.join(filePath, "testSummaryReport_" + fileName + ".xlsx")
        resultDF = pd.DataFrame(results)
        rows, columns = resultDF.shape[0], resultDF.shape[1]
        resultDF = resultDF.sort_values("Test_Case_Id")
        resultDF.insert(columns - 1, 'Execution_Status', resultDF.pop('Execution_Status'))
        sheetName = "result"
        try:
            xcelWriter = pd.ExcelWriter(filePath, engine="xlsxwriter")
            resultDF.to_excel(xcelWriter, sheetName, index=False)
            xcelWriter.save()
        except Exception as e:
            print("Unable to Generate Excel report for below Reason : ")
            print(e)

    def pdToListOfDict(self, pd):
        return list(pd.fillna('').to_dict(orient="index").values())

    def getExcelSheetNames(self, filePath):
        xl = pd.ExcelFile(filePath)
        sheetNames = xl.sheet_names  # see all sheet names
        return sheetNames

    def listOfDictToDf(self, listOfDict):
        return pd.DataFrame(listOfDict)

    def writeIntoExcel(self, filePath, values):
        if not isinstance(values, pd.DataFrame):
            values = self.listOfDictToDf(values)
        values.to_excel(filePath, index=False, header=True)

    def reportFormatting(self, filePath):
        reportDF = self.readExcel(filePath)
        rows, columns = reportDF.shape[0], reportDF.shape[1]
        sheetName = "result"
        try:
            xcelWriter = pd.ExcelWriter(filePath, engine="xlsxwriter")
            reportDF.to_excel(xcelWriter, sheetName, index=False)
            workbook = xcelWriter.book
            worksheet = xcelWriter.sheets[sheetName]
            for row in range(rows):
                for col_num, value in enumerate(reportDF.columns.values):
                    worksheet.write(0, col_num, value, workbook.add_format(headerFormat()))
                    worksheet.set_column(row, col_num, len(value))
                if reportDF.loc[row, "Execution_Status"] == "PASS":
                    worksheet.write(row + 1, columns - 1, "PASS", workbook.add_format(passFormat()))
                elif reportDF.loc[row, "Execution_Status"] == "Not Executed":
                    worksheet.write(row + 1, columns - 1, "Not Executed", workbook.add_format(notExecutedFormat()))
                else:
                    worksheet.write(row + 1, columns - 1, "FAIL", workbook.add_format(failFormat()))
            xcelWriter.save()
        except Exception as e:
            print("Unable to Format Excel report for below Reason : ")
            print(e)
