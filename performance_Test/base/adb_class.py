from performance_Test.utilities.custom_logger import customLogger, allureLog
import subprocess
import time


class Device:
    log = customLogger()

    def __init__(self):
        self.output = None
        self.log.info("Checking Android Device Information")
        try:
            result = subprocess.run(['adb', 'devices'], capture_output=True, text=True, check=True)
            output = result.stdout.strip()  # Strip any extra whitespace
            self.log.info("Test Device information:\n{0}".format(output))

        except subprocess.CalledProcessError as e:
            self.log.critical(f"Error occurred while checking Device Information: {e}")

    def getDeviceSerialId(self):
        # This method is to get device serial id_s
        self.log.info("checking device serial-id")
        try:
            result = subprocess.run(['adb', 'devices'], capture_output=True, text=True, check=True)
            output = result.stdout
            # split the output by lines and skip the first line (header)
            lines = output.strip().split('\n')[1:]
            # print(lines)
            # Extra serial ID's
            serial_ids = [line.split('\t')[0] for line in lines if line.strip()]
            self.log.info("Device serial-id:{0}".format(serial_ids[0]))
            return serial_ids[0]

        except subprocess.CalledProcessError as e:
            self.log.error(f"Error occurred while getting devices serial-id: {e}")
            return f"Error: {e}"

    # This method checks display status and Enabling screen on and unlocked
    def getDeviceScreenStatus(self):
        def check_Status():
            cmd = "adb shell dumpsys nfc | grep 'mScreenState='"
            output = subprocess.run(cmd, capture_output=True, text=True, check=True)
            if "mScreenState=ON_UNLOCKED" in output.stdout:
                self.log.info("Device screen is ON and UnLocked")
            if "mScreenState=ON_LOCKED" in output.stdout:
                self.log.info("Device screen is ON and Locked")
                screen_Unlock()
                check_Status()
            if "mScreenState=OFF" in output.stdout:
                self.log.info("Device Screen is OFF ")
                screen_On()
                check_Status()

        def screen_On():
            subprocess.run(['adb', 'shell', 'input', 'keyevent', '26'], capture_output=True, text=True, check=True)
            time.sleep(2)
            # check_Status()

        def screen_Unlock():
            subprocess.run(['adb', 'shell', 'input', 'swipe', '500', '1000', '300', '300'], capture_output=True,
                           text=True,
                           check=True)
            time.sleep(2)
            # check_Status()

        try:
            self.log.info("checking device Screen Status")
            check_Status()
        except TypeError as e:
            self.log.error(f"NFC error occurred: {e}")
        except Exception as ex:
            self.log.error(f"Now checking another way to handle this Error:{ex}")

            def check_Status_1():
                cmd1 = "adb shell dumpsys display | grep 'mScreenState'"
                output1 = subprocess.run(cmd1, capture_output=True, text=True, check=True)
                cmd2 = "adb shell dumpsys window | grep 'mDreamingLockscreen'"
                output2 = subprocess.run(cmd2, capture_output=True, text=True, check=True)
                if "mScreenState=ON" in str(output1) and "mShowingDream=false mDreamingLockscreen=false" in str(
                        output2):
                    self.log.info("Device screen is ON and UnLocked")
                if "mScreenState=ON" in str(output1) and "mShowingDream=false mDreamingLockscreen=true" in str(output2):
                    self.log.info("Device screen is ON and Locked")
                    screen_Unlock()
                    check_Status_1()
                if "mScreenState=OFF" in str(output1):
                    screen_On()
                    check_Status_1()

            check_Status_1()

    def getAndroidVersion(self):
        # This method is to get device serial id_s
        self.log.info("checking device Android Version")
        try:
            result = subprocess.run(['adb', 'shell', 'getprop', 'ro.build.version.release'], capture_output=True, text=True, check=True)
            output = result.stdout
            self.log.info(f"Android Version :{output}")
            return output

        except subprocess.CalledProcessError as e:
            self.log.error(f"Error occurred while getting devices serial-id: {e}")
            return f"Error: {e}"

    def getDeviceName(self):
        # This method is to get device serial id_s
        cmd = "adb shell getprop ro.product.model"
        self.log.info("checking device Name")
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            output = result.stdout
            self.log.info(f"Device Name :{output}")
            return output

        except subprocess.CalledProcessError as e:
            self.log.error(f"Error occurred while getting devices serial-id: {e}")
            return f"Error: {e}"

    @staticmethod
    def launchApk(appPackage, appActivity):
        # allureLog("Launching Apk")
        launch_cmd = f"adb shell am start -n {appPackage}/{appActivity}"

        try:
            # Launch the APK
            result = subprocess.run(launch_cmd, capture_output=True, text=True, check=True)
            time.sleep(2)
            # output = result.stdout
            Device.log.info(f"Launch command output: {result.stdout}")

            # Give some time for the app to start
            time.sleep(3)  # Wait for 3 seconds before checking if the app is running
            check_cmd = f"adb shell \"ps | grep {appPackage}\""

            result = subprocess.run(check_cmd, capture_output=True, text=True, shell=True)
            # print(result)
            if appPackage in result.stdout:
                Device.log.info(f"App '{appPackage}' is running.")
                allureLog(f"{appPackage} Launched Successfully")
            else:
                Device.log.error(f"App '{appPackage}' is not running.")
                allureLog(f"{appPackage} launching failed")

        except subprocess.CalledProcessError as e:
            Device.log.error(f"Error occurred: {e}")

    @staticmethod
    def closeAndClearApp(appPackage):
        allureLog("Close and Clear from background ")
        # Command to force stop the app
        force_stop_cmd = f"adb shell am force-stop {appPackage}"
        clear_data_cmd = f"adb shell pm clear {appPackage}"

        try:
            # Run the command to force-stop the app
            subprocess.run(force_stop_cmd, shell=True, check=True)
            Device.log.info(f"App '{appPackage}' has been closed.")

            # Run the command to clear app data
            subprocess.run(clear_data_cmd, shell=True, check=True)
            Device.log.info(f"App '{appPackage}' data has been cleared.")
            allureLog(f"{appPackage} is successfully closed and cleared from background")

        except subprocess.CalledProcessError as e:
            Device.log.error(f"Error while closing/clearing app: {e}")

    def clearBackgroundApks(self):
        pass
