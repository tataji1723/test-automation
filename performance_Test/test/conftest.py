import time
import pytest
from performance_Test.base.driver_class import Driver
from appium.webdriver.appium_service import AppiumService
from performance_Test.base.adb_class import Device
import performance_Test.utilities.custom_logger as cl

log = cl.customLogger()


@pytest.fixture(scope='class')
def beforeClass(request):
    log.info("................Checking Android device is connection to PC..........")
    # Check android device in adb and getting serial id of device
    device = Device()
    deviceId = device.getDeviceSerialId()
    deviceVersion = device.getAndroidVersion()
    deviceName = device.getDeviceName()
    # Checking device Screen status
    device.getDeviceScreenStatus()
    # print("before class")
    # print("\nLaunching Appium Server")
    log.info("Trying to Connect Appium server")
    appium_service = AppiumService()
    appium_service.start()
    # Creating driver object and calling driver method
    driver1 = Driver()
    driver = driver1.getDriverMethod(deviceId, deviceVersion, deviceName)

    # request.cls gives us access to the class where test is executed
    if request.cls is not None:
        request.cls.driver = driver
    yield driver
    time.sleep(5)
    # driver.press_keycode(3)
    driver.quit()
    # print("after class")
    log.info("Appium server Stopped")
    appium_service.stop()


@pytest.fixture()
def beforeMethod(request):
    # print("Before Method")
    # log.info("Test started")
    test_name = request.node.name  # Get the name of the current test
    log.info(f"Starting test:{test_name}")
    yield
    # print("After Method")
    # log.info("Test Completed")
    log.info(f"Test completed:{test_name}")
