from performance_Test.deviceFunctions.display_brightness import DisplayBrightness
import unittest
import pytest


@pytest.mark.usefixtures("beforeClass", "beforeMethod")
class DeviceDisplayBrightness(unittest.TestCase):
    # driver = None

    @pytest.fixture(autouse=True)
    def classObjects(self):
        self.driver =None
        self.Db = DisplayBrightness(self.driver)


    # @pytest.mark.run(order=1)
    @pytest.mark.order(1)
    def test_clearRecentApps(self):
        print(" staring method ")
        self.Db.openRecentApps()
        print(" Middle method ")
        self.Db.clickCloseAll()
        print(" ending method ")

    @pytest.mark.order(2)
    def test_launchAPK(self):
        self.Db.launchAPK()
        print(" Starting_1 method ")
        # cl.allureLog(f"App Launched")

    # @pytest.mark.order(3)
    # def test_preConditions(self):
    #     print(" ending_1 method ")
    #     self.Db.clickSearchButton()
    #     print(" ending_2 method ")
    #     self.Db.verifySearchPage()
    #     self.Db.enterSearchText()
    #     self.Db.verifyDisplayBrightness()
    #     self.Db.clickDisplayBrightness()
    #     self.Db.verifyDisplayBrightness()
    #
    # @pytest.mark.order(4)
    # def test_AutoBrightnessStatus(self):
    #     self.Db.verifyAutoBrightness()
    #
    # @pytest.mark.order(5)
    # def test_AutoRotateStatus(self):
    #     self.Db.verifyAutoRotate()
    #     self.Db.verifyAutoRotateButton()
    #
    # @pytest.mark.order(6)
    # def test_closeApp(self):
    #     self.Db.closeApp()
