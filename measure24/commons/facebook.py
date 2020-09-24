# coding: utf8
import re

from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .driver import WebDriver
from .settings import logger
from .sentry import Sentry
from configuration.models import Configuration

import os
import pickle
import time


class Facebook(WebDriver):

    def __init__(self, email, password, user_id, headless_mode=True, *args, **kwargs):
        super().__init__(headless_mode, *args, **kwargs)
        self.email = email
        self.password = password
        self.user_id = user_id

    def login(self):
        """
        Login into portal
        :return:
        """

        self.driver.get("https://m.facebook.com/")

        try:
            if os.path.isfile("cookies_user_%s.pkl" % str(self.user_id)):
                cookies = pickle.load(open("cookies_user_%s.pkl" % str(self.user_id), "rb"))
                for cookie in cookies:
                    self.driver.add_cookie(cookie)

            self.driver.get("https://m.facebook.com/")
        except (IOError, OSError) as osex:
            logger.warning(str(osex))

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, ".//body")))

        # Edit
        print(self.driver.title, "Facebook - Log In or Sign Up" == str(self.driver.title))
        if ("zaloguj " or "log " or "Log ") in str(self.driver.title) or \
                "Facebook - Log In or Sign Up" == str(self.driver.title) or \
                "Log into Facebook | Facebook" == str(self.driver.title):
            try:
                with open("last_login_page_source.html", "w") as f:
                    f.write(self.driver.page_source)

                # Edit
                email_input = self.driver.find_element_by_name("email")
                pass_input = self.driver.find_element_by_name("pass")

                try:
                    login_button = self.driver.find_element_by_name("login")
                except NoSuchElementException:
                    login_button = None
                    print("Nie znaleziono przycisku zaloguj")
                except KeyError:
                    login_button = None
                    print("Nie znaleziono przycisku zaloguj")

                if email_input and pass_input and login_button:
                    email_input.send_keys(self.email)
                    pass_input.send_keys(self.password)
                    login_button.click()

                logger.warning("Zaszła potrzeba zalogowania się na konto: login(%s)" % self.email)
            except NoSuchElementException as e:
                logger.info("Błąd podczas logowania: %s" % e)
        else:
            logger.info("Zalogowano się przy użyciu zmiennych sesyjnych: login(%s)" % self.email)

        pickle.dump(self.driver.get_cookies(), open("cookies_user_%s.pkl" % str(self.user_id), "wb"))

        return

    def go_to_group(self, group_url):
        """
        Go to facebook group
        :return: Object
        """
        config = Configuration.get_solo()
        limit_counter = 0
        limit = config.max_entry
        group_url = str(group_url).replace("www.facebook.com", "m.facebook.com")
        print("Go to group %s" % str(group_url))
        self.driver.get(group_url)
        post_data = []

        try:
            with open("last_group_page_source.html", "w") as f:
                f.write(self.driver.page_source)
        except Exception as e:
            pass

        # Go up
        # self.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)

        try:
            post_attr = "class"
            posts_value = ""
            post_method = "tag"

            if post_method == "tag":
                posts = self.driver.find_elements_by_tag_name("article")
            else:
                posts = self.driver.find_elements_by_xpath("//*[contains(@" + post_attr + ", '" + posts_value + "')]")

            # Edit
            if posts is None:
                logger.warning("Nie wykryto class path dla postów (lvl 0) lub błędna klasa elementu.")

            for post in posts:

                try:
                    """
                    Post author
                    """
                    tag_attr = "class"
                    tag_value = "bt dk dl dm"
                    try:
                        post_author = post.find_element_by_xpath(".//*[contains(@" + tag_attr + ", '" + tag_value + "')]//a")
                        post_author = post_author.get_attribute("innerText")
                    except NoSuchElementException:
                        post_author = None
                        logger.warning("Nie wykryto autora dla posta (lvl 0) lub błędna klasa elementu.")

                    """
                    Post message
                    """
                    tag_attr = "class"
                    tag_value = "dn"
                    try:
                        post_message = post.find_element_by_xpath(".//*[contains(@" + tag_attr + ", '" + tag_value + "')]")
                        post_message = post_message.get_attribute("innerText").replace("Zobacz więcej", "")
                    except NoSuchElementException:
                        post_message = None
                        logger.warning("Nie wykryto treści wiadomości dla posta (lvl 0) lub błędna klasa elementu.")

                    """
                    Post date
                    """
                    tag_attr = "class"
                    tag_value = "cq cr"
                    tag_method = "tag"
                    try:
                        if tag_method == "tag":
                            post_date = post.find_element_by_tag_name("abbr")
                        else:
                            post_date = post.find_element_by_xpath(".//*[contains(@" + tag_attr + ", '" + tag_value + "')]")
                        self.actions.move_to_element(post_date)
                        post_date = post_date.get_attribute("innerText")
                    except NoSuchElementException:
                        post_date = None
                        logger.warning("Nie wykryto daty dla posta (lvl 0) lub błędna klasa elementu.")

                    """
                    Post permalink
                    """
                    tag_attr = "href"
                    tag_value = "permalink"
                    try:
                        post_permalink = post.find_element_by_xpath(".//*[contains(@"+tag_attr+", '" + tag_value + "')]")
                        post_permalink = post_permalink.get_attribute("href")
                    except NoSuchElementException:
                        post_permalink = None
                        logger.warning("Nie wykryto permalink dla posta (lvl 0) lub błędna klasa elementu.")


                    # tag_attr = "class"
                    # tag_value = "cwj9ozl2 tvmbv18p"
                    # post_comments = post.find_element_by_xpath(".//*[contains(@"+tag_attr+", '" + tag_value + "')]")

                    if post_permalink:
                        match = re.search(r'permalink&id=([0-9]*)&', post_permalink)
                        if match:
                            post_id = match.group(1)
                        else:
                            post_id = None
                            logger.warning("Nie wykryto id dla posta")

                        match = re.search(r'(.*)&refid', post_permalink)
                        if match:
                            post_permalink = match.group(1)
                    else:
                        post_id = None

                    logger.info(post_id)
                    logger.info(post_author)
                    logger.info(post_message)
                    logger.info(post_date)
                    logger.info(post_permalink)

                    post_data.append({
                        'post_id': post_id,
                        'post_author': post_author,
                        'post_message': post_message,
                        'post_date': post_date,
                        'post_permalink': post_permalink,
                        'post_comments': []
                        # 'post_comments': self._get_comments_lvl_0(post_comments)
                    })

                    limit_counter += 1
                    if limit_counter >= limit:
                        break


                except NoSuchElementException:
                    warning = "Nie wykryto message dla posta: %s" % post.get_attribute("id")
                    logger.warning(warning)

            return post_data

        except NoSuchElementException as general_exception:
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
                    find_element_by_xpath(".//a[contains(@data-ft, '{\"tn\":\"Q\"}')]")
                self.actions.move_to_element(post_show_more)
                time.sleep(2)
                logger.info("Click into more button")
                self.driver.execute_script("arguments[0].click();", post_show_more)
                # post_show_more.click()
            except NoSuchElementException:
                post_show_more = None
            except StaleElementReferenceException:
                pass

        time.sleep(2)

        if comments_html_elements.size != 0:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, ".//ul//li//div//div[@role='article']")))
            post_comments_collection = comments_html_elements.\
                find_elements_by_xpath(".//ul//li//div//div[@role='article']")
        else:
            print("Post collection = 0")
            post_comments_collection = []

        for comment in post_comments_collection:
            try:
                comment_id = str(comment.find_element_by_xpath(".//a[contains(@data-ft,'N')]")\
                    .get_attribute("href")).rsplit("comment_id=")[1]
                if comment_id:
                    comment_id = comment_id.replace("&reply_", "")
                comment_author = comment.find_element_by_xpath(".//img")
                comment_author_name = comment_author.get_attribute("alt")
                comment_author_link_profile = comment.find_element_by_xpath(".//a[contains(@data-hovercard,'user.php')]")\
                    .get_attribute("href")
                comment_text = comment.find_element_by_xpath(".//span[@dir='ltr']").get_attribute("innerText")
                comment_date = comment.find_element_by_xpath(".//abbr")\
                    .get_attribute("data-utime")

                logger.info(comment_id)
                logger.info(comment_author_name)
                logger.info(comment_author_link_profile)
                logger.info(comment_date)
                logger.info(comment_text)

                post_comments_data.append({
                    'comment_id': comment_id,
                    'author_name': comment_author_name,
                    'author_link_profile': comment_author_link_profile,
                    'comment_date': comment_date,
                    'comment_text': comment_text,
                    'subcomments': self._get_comments_lvl_1(comment)
                })

            except NoSuchElementException as general_exception:
                logger.error("Nie pobrano danych komentarza")
                Sentry.capture_event(general_exception)

        return post_comments_data

    def _get_comments_lvl_1(self, comments_html_elements):
        """
        Go comments on lvl 1
        :return: List
        """
        post_comments_data = []
        # post_show_more = True
        #
        # while post_show_more is not None:
        #     try:
        #         post_show_more = comments_html_elements. \
        #             find_element_by_xpath(".//a[@role='button' and contains(text(), 'odpowiedzi')]")
        #         self.actions.move_to_element(post_show_more)
        #         time.sleep(2)
        #         self.driver.execute_script("arguments[0].click();", post_show_more)
        #         # post_show_more.click()
        #     except NoSuchElementException:
        #         post_show_more = None
        #     except StaleElementReferenceException:
        #         print("Exception Stale")

        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, ".//ul//li//div//div[contains(@data-ft,'R')]")))
            post_comments_collection = comments_html_elements.\
                find_elements_by_xpath(".//ul//li//div//div[contains(@data-ft,'R')]")
        except NoSuchElementException:
            return []

        for comment in post_comments_collection:
            try:
                comment_id = str(comment.find_element_by_xpath(".//a[contains(@data-ft,'N')]")\
                    .get_attribute("href")).rsplit("reply_comment_id=")[1]
                if comment_id:
                    comment_id = comment_id.replace("&reply_", "")
                comment_author = comment.find_element_by_xpath(".//img")
                comment_author_name = comment_author.get_attribute("alt")
                comment_author_link_profile = comment.find_element_by_xpath(".//a[contains(@data-hovercard,'user.php')]")\
                    .get_attribute("href")
                comment_date = comment.find_element_by_xpath(".//abbr")\
                    .get_attribute("data-utime")
                comment_text = comment.find_element_by_xpath(".//span[@dir='ltr']").get_attribute("innerText")

                logger.info(comment_id)
                logger.info(comment_author_name)
                logger.info(comment_author_link_profile)
                logger.info(comment_date)
                logger.info(comment_text)

                post_comments_data.append({
                    'comment_id': comment_id,
                    'author_name': comment_author_name,
                    'author_link_profile': comment_author_link_profile,
                    'comment_date': comment_date,
                    'comment_text': comment_text,
                })

            except NoSuchElementException as general_exception:
                logger.error("Nie pobrano danych komentarza lvl1")
                Sentry.capture_event(general_exception)

        return post_comments_data
