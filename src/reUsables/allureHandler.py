import allure
from allure_commons.types import AttachmentType


class AllureHandler:

    def takeAndAttachScreenshot(self, driver):
        allure.attach(driver.get_screenshot_as_png(), name="screenshot", attachment_type=AttachmentType.PNG)

    def allureLogs(self, log):
        with allure.step(log):
            pass

    def attachExcelFiles(self, filePath):
        allure.attach.file(filePath, name="attachedExcel.xlsx", extension="xlsx")
