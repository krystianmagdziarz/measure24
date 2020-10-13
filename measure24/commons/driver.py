from selenium.webdriver.firefox.options import Options as FirefoxOptions
# from measure24.commons.settings import get_platform_driver
# from selenium import webdriver
from selenium.common.exceptions import SessionNotCreatedException
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from selenium.webdriver.common.action_chains import ActionChains


class WebDriver:

    def __init__(self, headless_mode=True, *args, **kwargs):
        self.driver = self.__createdriver(headless=headless_mode)
        self.actions = ActionChains(self.driver)

    def close(self):
        """
        Zamyka przegladarke i czysci dane
        :return: None
        """
        try:
            # self.driver.delete_all_cookies()
            if self.driver:
                self.driver.quit()
        except:
            pass

    def __createdriver(self, headless=True):
        """
        Tworzenie webdriver-a
        :param headless: Boolean
        :return: Driver object
        """
        print("Create driver")

        firefox_options = FirefoxOptions()
        try:
            if headless:
                # firefox_options.headless = True
                # firefox_options.add_argument('--headless')
                # firefox_options.add_argument('--no-sandbox')
                # firefox_options.add_argument('--disable-dev-shm-usage')

                driver = RemoteWebDriver(options=firefox_options, command_executor="http://geckodriver:4444")
            else:
                driver = RemoteWebDriver(options=firefox_options, command_executor="http://geckodriver:4444")
        except Exception as e:
            print(str(e))
            return

        # Set timeout
        # driver.set_page_load_timeout(30)

        return driver
