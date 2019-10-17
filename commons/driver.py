from selenium.webdriver.firefox.options import Options as FirefoxOptions
from settings import get_platform_driver
from selenium import webdriver
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
            self.driver.quit()
        except:
            pass

    def __createdriver(self, headless=True):
        """
        Tworzenie webdriver-a
        :param headless: Boolean
        :return: Driver object
        """
        firefox_options = FirefoxOptions()
        if headless:
            firefox_options.headless = True
            firefox_options.add_argument('--headless')
            firefox_options.add_argument('--no-sandbox')
            firefox_options.add_argument('--disable-dev-shm-usage')

            driver = webdriver.Firefox(options=firefox_options, executable_path=get_platform_driver())
        else:
            driver = webdriver.Firefox(options=firefox_options, executable_path=get_platform_driver())

        return driver
