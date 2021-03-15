"""
Contains base class for functional tests and some helper methods.
"""
import time
from faker import Faker
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.firefox.options import Options
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from users.factories import UserFactory

options = Options()
options.headless = True
fake = Faker()
MAX_WAIT = 5


class FunctionalTest(StaticLiveServerTestCase):
    """
    Base class for functional tests.
    """

    def setUp(self):
        self.browser = webdriver.Firefox(options=options)

    def tearDown(self):
        self.browser.quit()

    def login(self, name):
        """
        logs in a user.
        """
        password = fake.password()
        user = UserFactory(name=name, password=password)
        self.browser.get(self.live_server_url)
        wait_for(lambda: self.browser.find_element_by_link_text("Login")).click()
        wait_for(lambda: self.browser.find_element_by_name("username")).send_keys(
            user.email
        )
        wait_for(lambda: self.browser.find_element_by_name("password")).send_keys(
            password
        )
        wait_for(
            lambda: self.browser.find_element_by_css_selector("input[type='submit']")
        ).click()


def wait_for(function):
    """
    Helper method for the tests. Provides an explicit wait.
    """
    start_time = time.time()
    while True:
        try:
            return function()
        except WebDriverException as exception:
            if time.time() - start_time > MAX_WAIT:
                raise exception
            time.sleep(0.5)
