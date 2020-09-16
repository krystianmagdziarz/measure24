# coding: utf8

from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .driver import WebDriver
from .settings import logger

import os
import pickle
import time
import re


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

        self.driver.get("https://www.facebook.com/")

        try:
            if os.path.isfile("cookies_user_%s.pkl" % str(self.user_id)):
                cookies = pickle.load(open("cookies_user_%s.pkl" % str(self.user_id), "rb"))
                for cookie in cookies:
                    self.driver.add_cookie(cookie)

            self.driver.get("https://www.facebook.com/")
        except (IOError, OSError) as osex:
            logger.warning(str(osex))

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, ".//body")))

        # Edit
        if ("zaloguj " or "log " or "Log ") in self.driver.title or \
                "Facebook - Log In or Sign Up" in str(self.driver.title):
            try:
                with open("last_login_page_source.html", "w") as f:
                    f.write(self.driver.page_source)

                # Edit
                email_input = self.driver.find_element_by_id("email")
                pass_input = self.driver.find_element_by_id("pass")

                try:
                    login_button = self.driver.find_element_by_xpath("//*[text()='Log In']")
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
                logger.info("Zalogowano się przy użyciu zmiennych sesyjnych: login(%s)" % self.email)
        else:
            logger.info("Zalogowano się przy użyciu zmiennych sesyjnych: login(%s)" % self.email)

        pickle.dump(self.driver.get_cookies(), open("cookies_user_%s.pkl" % str(self.user_id), "wb"))

        return

    def go_to_group(self, group_url):
        """
        Go to facebook group
        :return: Object
        """
        limit_counter = 0
        limit = 3
        self.driver.get(group_url)
        post_data = []

        with open("last_group_page_source.html", "w") as f:
            f.write(self.driver.page_source)

        # Wait until this element not visible
        check_visibility_attr = 'role'
        check_visibility_value = 'banner'
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//*[contains(@" + check_visibility_attr + ", '" + check_visibility_value + "')]"))
        )
        time.sleep(2)

        try:
            post_attr = "class"
            posts_value = "du4w35lb k4urcfbm l9j0dhe7 sjgh65i0"
            posts = self.driver.find_elements_by_xpath("//*[contains(@" + post_attr + ", '" + posts_value + "')]")

            # Edit
            if posts is None:
                logger.warning("Nie wykryto class path dla postów (lvl 0) lub błędna klasa elementu.")

            for post in posts:
                try:
                    tag_attr = "class"
                    tag_value = "oi732d6d ik7dh3pa d2edcug0 hpfvmrgz qv66sw1b c1et5uql a8c37x1j keod5gw0 nxhoafnm aigsh9s9 d9wwppkn fe6kdd0r mau55g9w c8b282yb hrzyx87i jq4qci2q a3bd9o3v knj5qynh m9osqain hzawbc8m"
                    post_author = post.find_element_by_xpath(".//*[contains(@" + tag_attr + ", '" + tag_value + "')]")
                    if post_author is None:
                        logger.warning("Nie wykryto autora dla posta (lvl 0) lub błędna klasa elementu.")
                    else:
                        post_author = post_author.get_attribute("innerText")

                    tag_attr = "class"
                    tag_value = "f530mmz5 b1v8xokw o0t2es00 oo9gr5id"
                    post_message = post.find_element_by_xpath(".//*[contains(@" + tag_attr + ", '" + tag_value + "')]")
                    if post_message is None:
                        logger.warning("Nie wykryto treści wiadomości dla posta (lvl 0) lub błędna klasa elementu.")
                    else:
                        post_message = post_message.get_attribute("innerText").replace("Zobacz więcej", "")

                    tag_attr = "class"
                    tag_value = "oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 gpro0wi8 b1v8xokw"
                    post_date = post.find_element_by_xpath(".//*[contains(@"+tag_attr+", '" + tag_value + "')]")
                    if post_date is None:
                        logger.warning("Nie wykryto daty dla posta (lvl 0) lub błędna klasa elementu.")
                    else:
                        post_date = post_date.get_attribute("innerText")

                    tag_attr = "class"
                    tag_value = "oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 gpro0wi8 b1v8xokw"
                    post_permalink = post.find_element_by_xpath(".//*[contains(@"+tag_attr+", '" + tag_value + "')]")
                    if post_permalink is None:
                        logger.warning("Nie wykryto permalink dla posta (lvl 0) lub błędna klasa elementu.")
                    else:
                        post_permalink = post_permalink.get_attribute("href")

                    tag_attr = "class"
                    tag_value = "cwj9ozl2 tvmbv18p"
                    post_comments = post.find_element_by_xpath(".//*[contains(@"+tag_attr+", '" + tag_value + "')]")

                    if post_permalink:
                        match = re.search(r'/permalink/([0-9]*)/', post_permalink)
                        if match:
                            post_id = match.group(1)
                        else:
                            post_id = None
                            logger.warning("Nie wykryto id dla posta")
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
                        'post_comments': self._get_comments_lvl_0(post_comments)
                    })

                    if limit_counter > limit:
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
                    find_element_by_xpath(".//*[contains(text(), 'Zobacz więcej komentarzy')]")
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
            tag_attr = "aria-label"
            tag_value = "Komentarz"
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, ".//*[contains(@"+tag_attr+", '" + tag_value + "')]"))
            )
            post_comments_collection = comments_html_elements.\
                find_elements_by_xpath(".//*[contains(@"+tag_attr+", '" + tag_value + "') and not(contains(@aria-label, 'Komentarz do posta'))]")
        else:
            print("Post collection = 0")
            post_comments_collection = []

        for comment in post_comments_collection:
            try:
                # comment_id = str(comment.find_element_by_xpath(".//a[contains(@data-ft,'N')]")\
                #     .get_attribute("href")).rsplit("comment_id=")[1]
                # if comment_id:
                #     comment_id = comment_id.replace("&reply_", "")

                tag_attr = "class"
                tag_value = "pq6dq46d"
                try:
                    comment_author_name = comment.find_element_by_xpath(
                        ".//*[contains(@" + tag_attr + ", '" + tag_value + "')]").get_attribute("innerText")
                except:
                    comment_author_name = None
                    logger.warning("Nie wykryto Autora dla odpowiedzi (lvl 0) lub błędna klasa elementu.")

                tag_attr = "href"
                tag_value = "/user/"
                try:
                    comment_author_link_profile = comment.find_element_by_xpath(
                        ".//*[contains(@" + tag_attr + ", '" + tag_value + "')]").get_attribute("href")
                except:
                    comment_author_link_profile = None
                    logger.warning("Nie wykryto linka do profilu dla odpowiedzi (lvl 0) lub błędna klasa elementu.")

                tag_attr = "class"
                tag_value = "ecm0bbzt e5nlhep0 a8c37x1j"
                try:
                    comment_text = comment.find_element_by_xpath(
                        ".//*[contains(@" + tag_attr + ", '" + tag_value + "')]").get_attribute("innerText")
                except:
                    comment_text = None
                    logger.warning("Nie wykryto treści wiadomości dla odpowiedzi (lvl 0) lub błędna klasa elementu.")

                tag_attr = "class"
                tag_value = "tojvnm2t a6sixzi8 abs2jz4q a8s20v7p t1p8iaqh k5wvi7nf q3lfd5jv pk4s997a bipmatt0 cebpdrjk qowsmv63 owwhemhu dp1hu0rb dhp61c6y iyyx5f41"

                try:
                    comment_date = comment.find_element_by_xpath(
                        ".//*[contains(@" + tag_attr + ", '" + tag_value + "')]").get_attribute("innerText")
                except:
                    comment_date = None
                    logger.warning("Nie wykryto daty dla odpowiedzi (lvl 0) lub błędna klasa elementu.")

                # logger.info(comment_id)
                logger.info(comment_author_name)
                logger.info(comment_author_link_profile)
                logger.info(comment_date)
                logger.info(comment_text)

                post_comments_data.append({
                    # 'comment_id': comment_id,
                    'author_name': comment_author_name,
                    'author_link_profile': comment_author_link_profile,
                    'comment_date': comment_date,
                    'comment_text': comment_text,
                    'subcomments': self._get_comments_lvl_1(comment)
                })

            except NoSuchElementException as general_exception:
                logger.error("Nie pobrano danych komentarza", str(general_exception))

        return post_comments_data

    def _get_comments_lvl_1(self, comments_html_elements):
        """
        Go comments on lvl 1
        :return: List
        """
        post_comments_data = []
        post_show_more = True

        while post_show_more is not None:
            try:
                tag_attr = "class"
                tag_value = "rq0escxv l9j0dhe7 du4w35lb j83agx80 pfnyh3mw i1fnvgqd bp9cbjyn owycx6da btwxx1t3 nkwizq5d roh60bw9 scwd0bx6 hop8lmos"

                post_show_more = comments_html_elements. \
                    find_element_by_xpath(".//*[contains(@"+tag_attr+", '" + tag_value + "')]")
                self.actions.move_to_element(post_show_more)
                time.sleep(2)
                self.driver.execute_script("arguments[0].click();", post_show_more)
                # post_show_more.click()
            except NoSuchElementException:
                post_show_more = None
            except StaleElementReferenceException:
                print("Exception Stale")

        try:
            tag_attr = "class"
            tag_value = "l9j0dhe7 ecm0bbzt hv4rvrfc qt6c0cv9 scb9dxdr lzcic4wl btwxx1t3 j83agx80"

            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, ".//*[contains(@"+tag_attr+", '" + tag_value + "')]")))
            post_comments_collection = comments_html_elements.\
                find_elements_by_xpath(".//*[contains(@"+tag_attr+", '" + tag_value + "')]")
        except NoSuchElementException:
            return []

        print(len(post_comments_collection))

        for comment in post_comments_collection:
            try:
                # comment_id = str(comment.find_element_by_xpath(".//a[contains(@data-ft,'N')]")\
                #     .get_attribute("href")).rsplit("reply_comment_id=")[1]

                tag_attr = "class"
                tag_value = "nc684nl6"
                try:
                    comment_author_name = comment.find_element_by_xpath(".//*[contains(@"+tag_attr+", '" + tag_value + "')]").get_attribute("innerText")
                except:
                    comment_author_name = None
                    logger.warning("Nie wykryto Autora dla odpowiedzi (lvl 1) lub błędna klasa elementu.")

                tag_attr = "href"
                tag_value = "/user/"
                try:
                    comment_author_link_profile = comment.find_element_by_xpath(
                        ".//*[contains(@" + tag_attr + ", '" + tag_value + "')]").get_attribute("href")
                except:
                    comment_author_link_profile = None
                    logger.warning("Nie wykryto linka do profilu dla odpowiedzi (lvl 1) lub błędna klasa elementu.")

                tag_attr = "class"
                tag_value = "ecm0bbzt e5nlhep0 a8c37x1j"
                try:
                    comment_text = comment.find_element_by_xpath(
                        ".//*[contains(@" + tag_attr + ", '" + tag_value + "')]").get_attribute("innerText")
                except:
                    comment_text = None
                    logger.warning("Nie wykryto treści wiadomości dla odpowiedzi (lvl 2) lub błędna klasa elementu.")

                tag_attr = "class"
                tag_value = "tojvnm2t a6sixzi8 abs2jz4q a8s20v7p t1p8iaqh k5wvi7nf q3lfd5jv pk4s997a bipmatt0 cebpdrjk qowsmv63 owwhemhu dp1hu0rb dhp61c6y iyyx5f41"

                try:
                    comment_date = comment.find_element_by_xpath(
                        ".//*[contains(@" + tag_attr + ", '" + tag_value + "')]").get_attribute("innerText")
                except:
                    comment_date = None
                    logger.warning("Nie wykryto daty dla odpowiedzi (lvl 2) lub błędna klasa elementu.")

                # logger.info(comment_id)
                logger.info(comment_author_name)
                logger.info(comment_author_link_profile)
                logger.info(comment_date)
                logger.info(comment_text)

                post_comments_data.append({
                    # 'comment_id': comment_id,
                    'author_name': comment_author_name,
                    'author_link_profile': comment_author_link_profile,
                    'comment_date': comment_date,
                    'comment_text': comment_text,
                })

            except NoSuchElementException as general_exception:
                logger.error("Nie pobrano danych komentarza lvl1")

        return post_comments_data
