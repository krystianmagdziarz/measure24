import os
import logging
import sentry_sdk

from sys import platform, exit

# Sentry logger
sentry_sdk.init("https://23ac1c5dc1ad4233a5176af52bdc3aaa@sentry.io/2035970")

# Create a custom logger
logger = logging.getLogger(__name__)

# Create handler
i_handler = logging.StreamHandler()
f_handler = logging.FileHandler('file.log')
f_handler.setLevel(logging.WARNING)
f_handler.setLevel(logging.ERROR)
i_handler.setLevel(logging.INFO)

# Create formatters and add it to handler
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
i_format = logging.Formatter('%(asctime)s - %(message)s')
f_handler.setFormatter(f_format)
i_handler.setFormatter(i_format)

# Add handlers to the logger
logger.addHandler(f_handler)
logger.addHandler(i_handler)
logger.setLevel(logging.INFO)


def get_platform_driver():
    """
    Sprawdzam jaki system operacyjny jest uzywany przez uzytkownika
    """
    if platform == "linux" or platform == "linux2":
        detected_platform = "linux"
    elif platform == "darwin":
        detected_platform = None
        exit("Nie obslugiwany system operacyjny")
    else:
        detected_platform = "windows"

    path = os.getcwd() + '/assets/'

    if detected_platform == "linux":
        return path + "geckodriver"
    elif detected_platform == "windows":
        return os.getcwd() + r"\assets\geckodriver.exe"
    else:
        return None
