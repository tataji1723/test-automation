import logging
import inspect
import os
import allure


def customLogger():
    # Get the class/method name from where the custom logger method is called
    logName = inspect.stack()[1][3]

    # Create the logging object and pass the log name in it
    logger = logging.getLogger(logName)

    # Create log level
    logger.setLevel(logging.DEBUG)

    # Define the directory for the log file
    log_directory = "../Reports"

    # Check if the directory exists, if not, create it
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    # Create a file handler to save the logs in the file
    log_file = os.path.join(log_directory, "Test.log")  # Specify the log file name
    fileHandler = logging.FileHandler(log_file, mode='a')

    # Set the log level to file handler
    fileHandler.setLevel(logging.DEBUG)

    # Create the formatter in which way you want to save the log
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                  datefmt='%d:%m:%y %H:%M:%S %p %A')

    # Set the formatter to file handler
    fileHandler.setFormatter(formatter)

    # Add file handler to logging
    logger.addHandler(fileHandler)

    # Return logger
    return logger


def allureLog(text):
    with allure.step(text):
        pass
