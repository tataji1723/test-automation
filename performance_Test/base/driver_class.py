from appium import webdriver
from appium.options.android import UiAutomator2Options
from performance_Test.utilities.custom_logger import customLogger
import time


class Driver:
    log = customLogger()

    @staticmethod
    def getDriverMethod(deviceId, deviceVersion, deviceName):
        deviceId = str(deviceId)
        desired_cap = {
            'platformName': 'Android',
            'automationName': 'UiAutomator2',
            'platformVersion': deviceVersion,
            'deviceName': deviceName,
            'udid': deviceId
        }

        appium_options = UiAutomator2Options()
        appium_options.load_capabilities(desired_cap)

        try:
            # Attempt to create the driver
            driver = webdriver.Remote("http://127.0.0.1:4723", options=appium_options)
            time.sleep(3)  # Consider using WebDriverWait instead of sleep for better reliability
            Driver.log.info("Successfully connected to Appium server.")
        except Exception as e:
            Driver.log.error(f"Failed to connect to Appium server: {e}")
            raise  # Rethrow the exception after logging it

        return driver
