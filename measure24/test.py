from facebook_test.test_facebook import Facebook

import os

TEST_USER = "anitaferency@wp.pl"
TEST_USER_ID = 2
TEST_PASSWORD = "anit66"

GROUP_URL = "https://www.facebook.com/groups/136460731063321/"


def remove_files():
    files = [
        "last_group_page_source.html",
        "last_login_page_source.html",
        "geckodriver.log",
        "file.log",
        "cookies_user_1.pkl",
        # "cookies_user_2.pkl",
    ]

    for file in files:
        if os.path.exists(file):
            os.remove(file)


def test_facebook():
    facebook = Facebook(TEST_USER, TEST_PASSWORD, TEST_USER_ID, False)
    facebook.login()
    facebook.go_to_group(GROUP_URL)


if __name__ == "__main__":
    remove_files()
    test_facebook()
