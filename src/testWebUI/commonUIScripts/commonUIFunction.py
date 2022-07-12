import os.path
import time

from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.reUsables.filePath import FilePath


class CommonUiFunction():
    waitingTime = 20

    def __init__(self, waitingTime=20):
        self.waitingTime = waitingTime

    def takeScreenshot(self, driver, fileName):
        filePath = FilePath()
        if filePath.getPath("screenShotPath") not in fileName:
            fileName = os.path.join(filePath.getPath("screenShotPath"), fileName)
        if ".png" not in fileName:
            fileName = fileName + ".png"
        driver.get_screenshot_as_file(fileName)

    def launchUrl(self, driver, url):
        driver.maximize_window()
        driver.get(url)

    def implicitWait(self, driver, sleep=3):
        driver.implicitly_wait(sleep)

    def waitForElementToLoad(self, driver, xpath):
        try:
            element = WebDriverWait(driver, self.waitingTime).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            return element
        except Exception as e:
            print(e)
            print("waited for {0} seconds. unable to locate the element {1} ".format(self.waitingTime, xpath))

    def waitForElementToClick(self, driver, xpath):
        try:
            element = WebDriverWait(driver, self.waitingTime).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            return element
        except Exception as e:
            print(e)
            print("waited for {0} seconds. unable to locate the element {1} ".format(self.waitingTime, xpath))

    def waitForElementToLoadBycss(self, driver, css):
        try:
            element = WebDriverWait(driver, self.waitingTime).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, css))
            )
            return element
        except Exception as e:
            print(e)
            print("waited for {0} seconds. unable to locate the element {1} ".format(self.waitingTime, css))

    def enterInTextBox(self, driver, xpath, keyword):
        if self.waitForElementToLoad(driver, xpath) is not None:
            driver.find_element_by_xpath(xpath).send_keys(keyword)
            return True
        else:
            print("error in textbox xpath " + xpath + " for the word " + keyword)
            return False

    def click(self, driver, xpath):
        if self.waitForElementToLoad(driver, xpath) is not None and self.waitForElementToClick(driver,
                                                                                               xpath) is not None:
            try:
                driver.find_element_by_xpath(xpath).click()
                return True
            except Exception as e:
                print("error in clicking xpath " + xpath)
                return False

        else:
            print("error in clicking xpath " + xpath)
            return False

    def getText(self, driver, xpath):
        if self.waitForElementToLoad(driver, xpath) is not None:
            return driver.find_element_by_xpath(xpath).text
        else:
            assert 0 == 1, "error in getting text " + xpath

    def getAttribute(self, driver, xpath, attribute):
        if self.waitForElementToLoad(driver, xpath) is not None:
            return driver.find_element(By.XPATH, xpath).get_attribute(attribute)
        else:
            assert 0 == 1, "error in getting attribute " + xpath

    def switchToWindows(self, driver):
        windows = driver.window_handles
        presentWindow = windows[len(windows) - 1]
        driver.switch_to.window(presentWindow)
        print("Switched to window " + presentWindow)
        return presentWindow

    def switchFrameBycss(self, driver, css):
        if self.waitForElementToLoadBycss(driver, css) is not None:
            driver.switch_to.frame(driver.find_element(By.CSS_SELECTOR, css))
            return True
        else:
            assert 0 == 1, "error in switching frame " + css

    def waitForPageToLoad(self, driver):
        try:
            element = WebDriverWait(driver, self.waitingTime).until(
                EC.visibility_of_all_elements_located()
            )
            return element
        except Exception as e:
            print(e)
            print("waited for page to load for{0} seconds".format(self.waitingTime))

    def scrollDown(self, driver, xpath):
        try:
            if self.waitForElementToLoad(driver, xpath) is not None:
                ele = driver.find_element(By.XPATH, xpath)
                ele.location_once_scrolled_into_view
        except Exception as e:
            print(e)
            print("Issue in Scroll page " + xpath)

    def waitAndSwitchFrame(self, driver, xpath):
        try:
            element = WebDriverWait(driver, self.waitingTime).until(
                EC.frame_to_be_available_and_switch_to_it((By.XPATH, xpath))
            )
            return element
        except Exception as e:
            print(e)
            print("waited for {0} seconds. unable to locate the Frame {1} ".format(self.waitingTime, xpath))

    def waitForFrameToLoadBycss(self, driver, css):
        try:
            element = WebDriverWait(driver, self.waitingTime).until(
                EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, css))
            )
            return element
        except Exception as e:
            print(e)
            print("waited for {0} seconds. unable to locate the element {1} ".format(self.waitingTime, css))

    def scrollDownByJS(self, driver, xpath):
        if self.waitForElementToLoad(driver, xpath):
            element = self.waitForElementToLoad(driver, xpath)
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", element)

    def clickOnceLoad(self, driver, xpath):
        if self.waitForElementToLoad(driver, xpath) is not None:
            try:
                driver.find_element_by_xpath(xpath).click()
                return True
            except Exception as e:
                print("error in clicking xpath " + xpath)
                return False

        else:
            print("error in clicking xpath " + xpath)
            return False

    def pressTab(self, driver):
        try:
            actions = ActionChains(driver)
            actions.send_keys(Keys.TAB)
            actions.perform()
            return True
        except Exception as e:
            print("error in pressing tab ")
            print(e)

    def getElements(self, driver, xpath):
        try:
            if self.waitForElementToLoad(driver, xpath):
                return driver.find_elements_by_xpath(xpath)
        except Exception as e:
            print(e)
            print("Issue in finding elements " + xpath)