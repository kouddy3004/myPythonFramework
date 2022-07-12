import os.path
from os import listdir

from deepdiff import DeepDiff
import copy
from src.reUsables.fileHandler import FileHandler
from src.reUsables.filePath import FilePath
from src.reUsables.pandaHandler import PandaHandler


class MiscScripts:
    pandaHandler = PandaHandler()

    def diffOfTwoDicts(self, expectedDict, actualDict, ignoreDecimalDiff=True):
        resDifference = DeepDiff(expectedDict, actualDict)
        removekey = []
        diffDict = {}
        if "values_changed" in resDifference.keys():
            if ignoreDecimalDiff:
                for diff in resDifference["values_changed"]:
                    if isinstance(resDifference["values_changed"][diff]["old_value"], float) or isinstance(
                            resDifference["values_changed"][diff]["old_value"], int):
                        diffe = abs(resDifference["values_changed"][diff]["new_value"]
                                    - resDifference["values_changed"][diff]["old_value"])
                        if diffe < 0.5:
                            removekey.append(diff)
                for key in removekey:
                    resDifference["values_changed"].pop(key)

            for key in resDifference["values_changed"]:
                diffDict[key] = "Expected {0} == > Actual {1}".format(
                    resDifference["values_changed"][key]["old_value"],
                    resDifference["values_changed"][key]["new_value"])

        elif "type_changes" in resDifference.keys():
            for key in resDifference["type_changes"]:
                diffDict[key] = "Expected format {0} == > Actual Format received {1}".format(
                    resDifference["type_changes"][key]["old_type"],
                    resDifference["type_changes"][key]["new_type"])
        else:
            import copy
            diffDict = copy.deepcopy(resDifference)
        return diffDict

    def archivingReportsInVM(self):
        filePath = FilePath()
        fileHandler = FileHandler()
        xlReportPath = os.path.join(filePath.getPath("reportPath"), "excelReports")
        if fileHandler.checkFileOrFolderExist(xlReportPath):
            if len(listdir(xlReportPath)) > 0:
                excelFiles = listdir(xlReportPath)
                sftpURL = 'hostName'
                sftpUser = 'userName'
                sftpPass = 'pwd'
                vmfilePath = 'linuxPath'
                import paramiko
                try:
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(sftpURL, username=sftpUser, password=sftpPass)
                    ftp = ssh.open_sftp()
                    currentPath = vmfilePath + "currentReport/"
                    archivePath = vmfilePath + "archiveReports/"
                    if "currentReport" not in ftp.listdir(vmfilePath):
                        ftp.mkdir(currentPath)
                    if "archiveReports" not in ftp.listdir(vmfilePath):
                        ftp.mkdir(archivePath)
                    vmFiles = ftp.listdir(currentPath)
                    if len(vmFiles) > 0:
                        from datetime import datetime
                        now = datetime.now()
                        folder = str(now.strftime("%d%m%y%H%M%S"))
                        archivePath += folder
                        ftp.mkdir(archivePath)
                        for file in vmFiles:
                            oldPath = currentPath + file
                            newPath = archivePath + "/" + file
                            ftp.rename(oldPath, newPath)
                        print("Reports Archived")
                    for file in excelFiles:
                        source = os.path.join(xlReportPath, file)
                        target = currentPath + file
                        ftp.put(source, target)

                    print("Reports Uploaded into VM")

                except Exception as e:
                    print("Issue in Archiving Files because of below reason : ")
                    print(str(e))
                finally:
                    ftp.close()
                    ssh.close()
            else:
                print("No reports has been genereated in Excel Reports Folder")

    def assignInputWithTestCase(self, tcDetail, inputPath, sheetName):
        inputData = self.pandaHandler.readExcelByKey(inputPath, sheetName, "Test_Case_Id", tcDetail["Test_Case_Id"],
                                                     str)
        listOfInputs = []
        for inputDatum in inputData:
            temp = copy.deepcopy(tcDetail)
            temp.update(inputData[inputDatum])
            listOfInputs.append(temp)
        return listOfInputs

    def replicateDictToList(self, dictionary, size):
        listOfInputs = []
        for i in range(size):
            listOfInputs.append(copy.deepcopy(dictionary))
        return listOfInputs


if __name__ == "__main__":
    misc = MiscScripts()
    misc.archivingReportsInVM()
