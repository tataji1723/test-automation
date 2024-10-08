import time
import performance_Test.utilities.custom_logger as cl
from performance_Test.base.adb_class import Device
from performance_Test.base.base_class import ClassElements


class DisplayBrightness(ClassElements):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
    _searchButton = "com.android.settings:id/search_src_text"  # id
    _page_title = 'com.android.settings:id/search_src_text'  # id
    _enterSearchItem = "com.android.settings:id/search_src_text"  # id
    _verifyDisplayBrightnessText = "Display & brightness"  # text
    _clickDisplayBrightness = "Display & brightness"  # text"
    _AutoBrightnessButton = "android:id/switch_widget"  # id
    _verifyAutoRotate = '//android.widget.TextView[@resource-id="android:id/title" and @text="Auto-rotate"]'  # xpath
    _AutoRotateButton = "android:id/switch_widget"  # id
    _AppPackage = "com.android.settings"
    _AppActivity = "com.android.settings.Settings"
    _RecentApps = "com.android.launcher:id/overview_panel"  # id
    _clickClear = "com.android.launcher:id/btn_clear"  # id

    def openRecentApps(self):
        cl.allureLog("Open recent Apps")
        self.openRecentApks(self._RecentApps, "id")

    def clickCloseAll(self):
        cl.allureLog("Clicked on Clear All ")
        self.clickElement(self._clickClear, "id")

    def launchAPK(self):
        cl.allureLog("Launching APK")
        Device.launchApk(self._AppPackage, self._AppActivity)

    def clickSearchButton(self):
        self.clickElement(self._searchButton, "id")
        cl.allureLog("Clicked On search Button")

    def verifySearchPage(self):
        element = self.isDisplayed(self._page_title, "id")
        cl.allureLog("Verifying search page")
        assert element == True

    def enterSearchText(self):
        self.sendText("Display & brightness", self._enterSearchItem, "id")
        cl.allureLog("Enter Search Text")
        time.sleep(2)

    def verifyDisplayBrightness(self):
        element = self.isDisplayed(self._verifyDisplayBrightnessText, "text")
        cl.allureLog("Verifying Display & Brightness id")
        time.sleep(2)
        assert element == True

    def clickDisplayBrightness(self):
        self.clickElement(self._clickDisplayBrightness, "text")
        cl.allureLog("Clicked on Display and Brightness services")
        time.sleep(2)

    def verifyAutoBrightness(self):
        element = self.getSwitchStatus(self._AutoBrightnessButton, "id")
        cl.allureLog("verifying Auto Brightness is enabled or not")
        if element == "On":
            cl.allureLog("Auto Brightness is On...Now Disabling ")
            self.clickElement(self._AutoBrightnessButton, "id")
            self.getSwitchStatus(self._AutoBrightnessButton, "id")
            time.sleep(2)
            self.getScreenShot("Auto_brightness_status")
        else:
            cl.allureLog("Auto Brightness is Disabled")
            self.getScreenShot("Auto_brightness_latest")

    def verifyAutoRotate(self):
        cl.allureLog("verify Auto-rotate id is present or not")
        self.find_element_with_scroll(self._verifyAutoRotate, "xpath")
        # cl.allureLog("verifying Auto Rotate is enabled or not")
        self.getScreenShot("Auto_Rotate_Status")

    def verifyAutoRotateButton(self):
        element = self.getSwitchStatus(self._AutoRotateButton, "id")
        cl.allureLog("verifying Auto-Rotation is enabled or not")
        if element == "On":
            cl.allureLog("Auto-Rotation is On...Now Disabling ")
            self.clickElement(self._AutoRotateButton, "id")
            self.getSwitchStatus(self._AutoRotateButton, "id")
            time.sleep(2)
            self.getScreenShot("AutoRotate_status")
        else:
            cl.allureLog("AutoRotate is Disabled")
            self.getScreenShot("AutoRotate_status_latest")

    def closeApp(self):
        cl.allureLog("Closing Apk")
        Device.closeAndClearApp(self._AppPackage)
