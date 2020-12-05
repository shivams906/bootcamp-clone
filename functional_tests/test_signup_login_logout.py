"""
Functional tests for signup, login and logout (and other account functions).
"""
from django.urls import reverse
from users.models import User
from .base import fake, FunctionalTest, wait_for


class SignupLoginLogoutTestCase(FunctionalTest):
    """
    Tests for account related functions like signup, login and logout.
    """

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

        # She is taken to the login page
        wait_for(
            lambda: self.assertEqual(
                self.browser.current_url, self.live_server_url + reverse("users:login")
            )
        )

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
