""" dfgg




@author:
date:


modig=fie
date:
line change :


"""


import os
import allure
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import (ElementNotVisibleException, ElementNotSelectableException,
                                        NoSuchElementException, TimeoutException)
from selenium.webdriver.support.wait import WebDriverWait
from performance_Test.utilities.custom_logger import customLogger
import time


class ClassElements:
    log = customLogger()

    def __init__(self, driver):
        self.driver = driver

    def waitForElement(self, locatorValue, locatorType):
        locatorType = locatorType.lower()
        element = None
        wait = WebDriverWait(self.driver, 25, poll_frequency=1,
                             ignored_exceptions=[NoSuchElementException, ElementNotSelectableException,
                                                 ElementNotVisibleException, TimeoutException])

        if locatorType == "id":
            element = wait.until(lambda x: x.find_element(AppiumBy.ID, locatorValue))
            return element
        elif locatorType == "class":
            element = wait.until(lambda x: x.find_element(AppiumBy.CLASS_NAME, locatorValue))
            return element
        elif locatorType == "index":
            element = wait.until(
                lambda x: x.find_element(AppiumBy.ANDROID_UIAUTOMATOR, "UiSelector().index(%d)" % int(locatorValue)))
            return element
        elif locatorType == "des":
            element = wait.until(
                lambda x: x.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'UiSelector().description("%s")' % locatorValue))
            return element
        elif locatorType == "text":
            element = wait.until(lambda x: x.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'text("%s")' % locatorValue))
            return element
        elif locatorType == "xpath":
            element = wait.until(lambda x: x.find_element(AppiumBy.XPATH, '%s' % locatorValue))
            return element
        else:
            self.log.info("Locator value " + locatorValue + "not found")
        return element

    def getElement(self, locatorValue, locatorType="id"):
        element = None
        # Checking element is present in device UI
        try:
            locatorType = locatorType.lower()
            element = self.waitForElement(locatorValue, locatorType)
            if element:
                self.log.info(
                    "Element Found with Locator type :" + locatorType + "and with Locator Value :" + locatorValue)
            else:
                self.log.error(
                    "Element Not Found with Locator type :" + locatorType + "and with Locator Value :" + locatorValue)

        except Exception as e:
            self.log.error(f"Exception is: {str(e)}")
            self.takeScreenshot(locatorType)  # Take screenshot on failure

        return element

    def clickElement(self, locatorValue, locatorType="id"):

        try:
            locatorType = locatorType.lower()
            element = self.waitForElement(locatorValue, locatorType)
            print(element)
            time.sleep(5)
            # Attempt to click the Element
            element.click()  # Attempt to click the element
            time.sleep(2)
            self.log.info(
                "Clicked Element with Locator-type: " + locatorType + " and with Locator-Value: " + locatorValue)


            # Optional: Check if the element is still displayed after clicking
            # if not element.is_displayed():
            #     self.log.error("Element is not displayed after clicking, failing the test.")
            #     assert False, "Element was clicked but is not displayed anymore."
            #
            # assert True, "Element clicked Successfully"

        except Exception as e:
            self.log.error(
                "Unable to click on Element with Locator-type: " + locatorType + " and with Locator-Value: " +
                locatorValue)
            self.takeScreenshot(f"Click_failure_{locatorType}_{locatorValue}")
            assert False, f"Click action failed with exception: {str(e)}"
        return element

    # Enter text in search box or chat box
    def sendText(self, text, locatorValue, locatorType="id"):
        try:
            locatorType = locatorType.lower()
            element = self.waitForElement(locatorValue, locatorType)
            # Enter text to element
            element.send_keys(text)
            self.log.info(f"sent text on Element with Locator-type :{locatorType} and with Locator-Value :{locatorValue} and text is:{text}")
        except Exception as e:
            self.log.error(
                f"Unable to send text on Element with Locator-type :{locatorType}and with Locator-Value :{locatorValue}"
                f"Exception is : {str(e)} ")
            self.takeScreenshot(f"send_text_failure_{locatorType}_{locatorValue}")
            assert False
        return element

    def isDisplayed(self, locatorValue, locatorType="id"):
        try:
            locatorType = locatorType.lower()
            element = self.waitForElement(locatorValue, locatorType)
            # Check if element is displayed
            if element.is_displayed():
                self.log.info(
                    "Element with Locator-type: " + locatorType + " and Locator-Value: " + locatorValue + " is displayed")
                return True
            else:
                self.log.info(
                    "Element with Locator-type: " + locatorType + " and Locator-Value: " + locatorValue + " is not displayed")
                self.takeScreenshot(f"isDisplayed_failure_{locatorType}_{locatorValue}")
                return False

        except Exception as e:
            self.log.error(
                "An error occurred while trying to find the element with Locator-type: " + locatorType +
                " and Locator-Value: " + locatorValue + ". Error: " + str(e))
            self.takeScreenshot(f"IsDisplayed_exception_{locatorType}_{locatorValue}")
            assert False, f"Element not displayed: {locatorValue} ({locatorType})"

    def getScreenShot(self, screenshotName):
        try:
            # Ensure the directory exists
            screenshotDirectory = "../Screenshots/"
            if not os.path.exists(screenshotDirectory):
                os.makedirs(screenshotDirectory)

            # Construct the screenshot file path
            fileName = f"{screenshotName}_{time.strftime('%d%m%y_%H%M%S')}.png"
            screenshotPath = os.path.join(screenshotDirectory, fileName)

            # Save the screenshot
            if self.driver.save_screenshot(screenshotPath):
                self.log.info(f"Successfully saved screenshot at path: {screenshotPath}")
                return screenshotPath
            else:
                self.log.error("Failed to save screenshot.")
                return None

        except Exception as e:
            self.log.error(f"Unable to take screenshot. Exception: {e}")
            return None

    def isEnabled(self, locatorValue, locatorType="id"):
        try:
            locatorType = locatorType.lower()
            element = self.waitForElement(locatorValue, locatorType)
            if element.is_enabled():
                self.log.info(
                    "Element with Locator-type : " + locatorType + " and with Locator-Value :" + locatorValue + "is Enabled")
                return True
            else:
                self.log.info(
                    "Element with Locator-type : " + locatorType + "and with Locator-Value :" + locatorValue + "is not Enabled")
                self.takeScreenshot(locatorType)
                return False
        except Exception as e:
            self.log.error(
                "An error occurred while trying to find the element with Locator-type: " + locatorType +
                " and Locator-Value: " + locatorValue + ". Error: " + str(e))
            self.takeScreenshot(locatorType)
            assert False, f"Element not Enabled: {locatorValue} ({locatorType})"

    def getSwitchStatus(self, locatorValue, locatorType="id"):
        try:
            locatorType = locatorType.lower()
            element = self.waitForElement(locatorValue, locatorType)

            # Log switch status
            switch_status = element.get_attribute("text")
            self.log.info("Switch info found with Locator-type: " + locatorType +
                          " and with Locator Value: " + locatorValue +
                          " | Switch Status: " + switch_status)
            return switch_status

        except Exception as e:
            # Log error if switch info is not found
            self.log.error("Switch info not found with Locator-type: " + locatorType +
                           " and with Locator Value: " + locatorValue + " | Exception: " + str(e))
            self.takeScreenshot(locatorType)  # Take a screenshot for debugging
            assert False, f"Switch info not found or error occurred with Locator-type: {locatorType} and Locator Value: {locatorValue}"

    def takeScreenshot(self, text):
        allure.attach(self.driver.get_screenshot_as_png(), name=text, attachment_type=allure.attachment_type.PNG)

    def scroll_up(self):
        # Scroll up by performing a swipe gesture using the size of the screen
        size = self.driver.get_window_size()
        start_y = int(size['height'] * 0.8)  # Swipe from the bottom (80% of screen height)
        end_y = int(size['height'] * 0.2)  # To the top (20% of screen height)
        start_x = int(size['width'] / 2)  # Swipe in the middle of the screen horizontally

        # Perform the swipe action
        self.driver.swipe(start_x, start_y, start_x, end_y, 1000)

    def find_element_with_scroll(self, locatorValue, locatorType="id", max_scrolls=5):
        self.log.info("Attempting to find element with scrolling.")
        scroll_attempts = 0
        locatorType = locatorType.lower()
        first_attempt = True

        while scroll_attempts < max_scrolls:
            try:
                element = self.getElement(locatorValue, locatorType)
                # self.log.info("checking")
                if element:
                    self.log.info(f"Element with {locatorType} '{locatorValue}' found!")
                    return element  # Element found, return it
                # except NoSuchElementException:
                else:
                    self.log.info(f"Element with {locatorType} '{locatorValue}' not found. Scrolling up...")
                    self.scroll_up()  # Perform the scroll action
                    scroll_attempts += 1
                    time.sleep(1)  # Optional: wait a bit before the next scroll
            except Exception as e:
                if first_attempt:
                    self.log.info("First attempt failed, skipping exception logging.")
                    first_attempt = False  # Set the flag to False after the first attempt
                else:
                    self.log.error("An error occurred while trying to find the element with Locator-type: " +
                                   locatorType + " and Locator-Value: " + locatorValue + ". Error: " + str(e))
                    self.takeScreenshot(locatorType)
                    assert False, f"Element not detected: {locatorValue} ({locatorType})"
        self.log.info(f"Element with {locatorType} '{locatorValue}' not found after {max_scrolls} scroll attempts.")
        return None  # Element not found after all attempts

    def openRecentApks(self, locatorValue, locatorType):
        self.driver.press_keycode(3)
        time.sleep(2)
        # self.driver.press_keycode(187)
        try:
            self.driver.press_keycode(187)
        except AttributeError as e:
            raise Exception(f"Failed to press keycode: {e}")

        time.sleep(4)

        try:
            # Check for an element that's part of the Recent Apps view (this might vary by device)
            recent_apps_check = self.getElement(locatorValue, locatorType)
            if recent_apps_check:
                self.log.info("Recent Apps view successfully opened.")
            else:
                self.log.error("Failed to open Recent Apps view.")

        except Exception as e:
            # Log error if Recent apps is not found
            self.log.error("Recent apps not found with Locator-type: " + locatorType +
                           " and with Locator Value: " + locatorValue + " | Exception: " + str(e))
            self.takeScreenshot(locatorType)  # Take a screenshot for debugging
            assert False, f"Recent apps not found or error occurred with Locator-type: {locatorType} and Locator Value: {locatorValue}"
