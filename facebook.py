# coding: utf8

from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.common.exceptions import TimeoutException

from selenium.common.exceptions import NoSuchElementException
from commons.driver import WebDriver
from settings import logger

import pickle


class Facebook(WebDriver):

    def __init__(self, email, password, headless_mode=True, *args, **kwargs):
        super().__init__(headless_mode, *args, **kwargs)
        self.email = email
        self.password = password

    def login(self):
        """
        Login into portal
        :return:
        """

        self.driver.get("https://www.facebook.com/")

        try:
            cookies = pickle.load(open("cookies.pkl", "rb"))
            for cookie in cookies:
                self.driver.add_cookie(cookie)

            self.driver.get("https://www.facebook.com/")
        except OSError:
            pass

        try:
            email_input = self.driver.find_element_by_name("email")
            pass_input = self.driver.find_element_by_name("pass")

            try:
                login_button = self.driver.find_element_by_id("loginbutton")
            except NoSuchElementException:
                login_button = self.driver.find_element_by_xpath("//button[@name='login']")

            if email_input and pass_input and login_button:
                email_input.send_keys(self.email)
                pass_input.send_keys(self.password)
                login_button.click()

            logger.warning("Zaszła potrzeba zalogowania się na konto: login(%s)" % self.email)
        except NoSuchElementException as e:
            logger.info("Zalogowano się przy użyciu zmiennych sesyjnych: login(%s)" % self.email)

        pickle.dump(self.driver.get_cookies(), open("cookies.pkl", "wb"))

        return

    def go_to_group(self, group_url):
        """
        Go to facebook group
        :return: Object
        """

        self.driver.get(group_url)
        post_data = []

        try:
            posts = self.driver.find_elements_by_xpath("//*[contains(@id,'mall_post_')]")

            for post in posts:
                try:
                    post_id = post.get_attribute("id")
                    post_author = post.find_element_by_xpath(".//*[@rel='dialog']").get_attribute("title")
                    post_message = str(post.find_element_by_xpath(".//*[@data-testid='post_message']")\
                        .get_attribute("textContent")).replace("Zobacz więcej", "")
                    post_date = post.find_element_by_xpath(".//*[contains(@id,'feed_subtitle_')]//abbr")\
                        .get_attribute("title")
                    post_permalink = post.find_element_by_xpath(".//*[contains(@id,'feed_subtitle_')]//abbr/..")\
                        .get_attribute("href")
                    post_comments = post.find_element_by_xpath(".//*[contains(@data-testid,'CommentsList')]")

                    post_data.append({
                        'post_id': post_id,
                        'post_author': post_author,
                        'post_message': post_message,
                        'post_date': post_date,
                        'post_permalink': post_permalink,
                        'post_comments': self._get_comments_lvl_0(post_comments)
                    })
                    break
                except NoSuchElementException as e:
                    logger.warning(e, exc_info=True)

            return post_data

        except NoSuchElementException:
            logger.error("Nie znaleziono postów na wallu %s" % group_url)

    def _get_comments_lvl_0(self, comments_html_elements):
        """
        Go comments on lvl 0
        :return: List
        """

        # @todo: Przy rozwijaniu postów pasowałoby dodać losowy czas oczekiwania, w celu zminiejszenia
        #  prawdopodobieństwa blokady konta

        post_show_more = True
        post_comments_data = []

        while post_show_more is not None:
            try:
                post_show_more = comments_html_elements. \
                    find_element_by_xpath(".//*[contains(@data-testid,'CommentsPagerRenderer')]")
                self.actions.move_to_element(post_show_more)
                post_show_more.click()
            except NoSuchElementException:
                post_show_more = None

        post_comments_collection = comments_html_elements.\
            find_elements_by_xpath(".//ul//li//*[contains(@data-testid,'body')]")

        for comment in post_comments_collection:
            try:
                comment_author = comment.find_element_by_xpath(".//a")
                comment_author_name = comment_author.get_attribute("innerHTML")
                comment_author_link_profile = comment_author.get_attribute("href")

                logger.info(comment_author)

                post_comments_data.append({
                    'author_name': comment_author_name,
                    'author_link_profile': comment_author_link_profile,
                })

            except NoSuchElementException:
                logger.error("Nie pobrano danych komentarza")

        return post_comments_data
