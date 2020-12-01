"""
Functional tests for signup, login and logout (and other account functions).
"""
import time
from faker import Faker
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from users.models import User

fake = Faker()
MAX_WAIT = 5


class SignupLoginLogoutTestCase(StaticLiveServerTestCase):
    """
    Tests for account related functions like signup, login and logout.
    """

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_signup(self):
        """
        Tests that a user can sign up.
        """
        # Edith goes to the home page
        self.browser.get(self.live_server_url)
        self.assertIn("Bootcamp", self.browser.title)

        # She clicks on signup link
        self.browser.find_element_by_link_text("Signup").click()
        self.assertEqual(
            self.browser.current_url, self.live_server_url + reverse("users:signup")
        )

        # She fills in her details
        name_field = wait_for(lambda: self.browser.find_element_by_name("name"))
        email_field = wait_for(lambda: self.browser.find_element_by_name("email"))
        password_field = wait_for(lambda: self.browser.find_element_by_name("password"))

        name_field.send_keys(fake.name())
        email_field.send_keys(fake.email())
        password_field.send_keys(fake.password())

        # She clicks on signup button
        submit_button = wait_for(lambda: self.browser.find_element_by_name("submit"))
        submit_button.click()

        # She is taken to her profile page
        user = User.objects.first()
        wait_for(
            lambda: self.assertEqual(
                self.browser.current_url, self.live_server_url + user.get_absolute_url()
            )
        )
        main_content = wait_for(
            lambda: self.browser.find_element_by_tag_name("main")
        ).text
        self.assertIn(user.name, main_content)

    def test_login_logout(self):
        """
        Tests that a user can login and logout.
        """
        # Edith goes to the home page
        self.browser.get(self.live_server_url)
        self.assertIn("Bootcamp", self.browser.title)

        # She clicks on log in link
        self.browser.find_element_by_link_text("Login").click()
        self.assertEqual(
            self.browser.current_url, self.live_server_url + reverse("users:login")
        )

        # She fill in her details
        email_field = wait_for(lambda: self.browser.find_element_by_name("username"))
        password_field = wait_for(lambda: self.browser.find_element_by_name("password"))

        user = User.objects.create_user(
            name=fake.name(), email=fake.email(), password="test@123"
        )
        email_field.send_keys(user.email)
        password_field.send_keys("test@123")

        # She clicks on login button
        submit_button = wait_for(lambda: self.browser.find_element_by_name("submit"))
        submit_button.click()

        # She is now logged in
        wait_for(
            lambda: self.assertEqual(
                self.browser.current_url, self.live_server_url + "/"
            )
        )
        header_content = wait_for(
            lambda: self.browser.find_element_by_tag_name("header")
        ).text
        self.assertNotIn("Login", header_content)
        self.assertNotIn("Signup", header_content)
        self.assertIn(user.name, header_content)
        self.assertIn("Logout", header_content)

        # She clicks on logout link
        self.browser.find_element_by_link_text("Logout").click()

        # She is now logged out
        wait_for(
            lambda: self.assertEqual(
                self.browser.current_url, self.live_server_url + "/"
            )
        )
        header_content = wait_for(
            lambda: self.browser.find_element_by_tag_name("header")
        ).text
        self.assertIn("Login", header_content)
        self.assertIn("Signup", header_content)
        self.assertNotIn(user.name, header_content)
        self.assertNotIn("Logout", header_content)


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
