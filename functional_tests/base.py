"""
Contains base class for functional tests and some helper methods.
"""
import time
from faker import Faker
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

fake = Faker()
MAX_WAIT = 5


class FunctionalTest(StaticLiveServerTestCase):
    """
    Base class for functional tests.
    """

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()


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
