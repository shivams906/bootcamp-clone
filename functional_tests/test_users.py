"""
Functional tests for signup, login and logout (and other account functions).
"""
from django.urls import reverse
from users.factories import UserFactory
from users.models import User
from .base import fake, FunctionalTest, wait_for, webdriver


class UserTest(FunctionalTest):
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
            lambda: self.assertNotIn(reverse("users:login"), self.browser.current_url)
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
        header_content = wait_for(
            lambda: self.browser.find_element_by_tag_name("header")
        ).text
        self.assertIn("Login", header_content)
        self.assertIn("Signup", header_content)
        self.assertNotIn(user.name, header_content)
        self.assertNotIn("Logout", header_content)

    def test_follow_unfollow(self):
        """
        Tests that user can follow and unfollow other users.
        """
        self.login("Meredith")
        meredith_browser = self.browser
        self.browser = webdriver.Firefox()

        # Edith logs in and goes to Meredith's profile page.
        self.login("Edith")
        meredith = User.objects.get(name="Meredith")
        self.browser.get(
            self.live_server_url + reverse("users:profile", args=[meredith.pk])
        )

        # She sees a follow link.
        follow_link = wait_for(lambda: self.browser.find_element_by_link_text("follow"))

        # She clicks on it.
        follow_link.click()

        # The page reloads and follow link's text changes to unfollow.
        wait_for(lambda: self.browser.find_element_by_link_text("unfollow"))

        # She goes to the network page.
        self.browser.get(self.live_server_url + reverse("users:network", args=["all"]))

        # She clicks on followees' link.
        wait_for(lambda: self.browser.find_element_by_link_text("Followees")).click()

        # She sees meredith's name in the users' list
        wait_for(
            lambda: self.assertEqual(
                self.browser.current_url,
                self.live_server_url + reverse("users:network", args=["followees"]),
            )
        )
        user_list = wait_for(lambda: self.browser.find_element_by_id("user_list"))
        self.assertIn("Meredith", user_list.text)

        # Meredith goes to network page in her browser.
        edith_browser = self.browser
        self.browser = meredith_browser
        self.browser.get(self.live_server_url + reverse("users:network", args=["all"]))

        # She clicks on followers' link.
        wait_for(lambda: self.browser.find_element_by_link_text("Followers")).click()

        # She sees Edith's name in users' list
        wait_for(
            lambda: self.assertEqual(
                self.browser.current_url,
                self.live_server_url + reverse("users:network", args=["followers"]),
            )
        )
        user_list = wait_for(lambda: self.browser.find_element_by_id("user_list"))
        self.assertIn("Edith", user_list.text)

        # Edith goes to Meredith's profile page.
        meredith_browser = self.browser
        self.browser = edith_browser
        self.browser.get(
            self.live_server_url + reverse("users:profile", args=[meredith.pk])
        )

        # She clicks on the unfollow link.
        unfollow_link = wait_for(
            lambda: self.browser.find_element_by_link_text("unfollow")
        )
        unfollow_link.click()

        # The page reloads and unfollow link's text changes to follow.
        wait_for(lambda: self.browser.find_element_by_link_text("follow"))

        # She goes to the network page.
        self.browser.get(self.live_server_url + reverse("users:network", args=["all"]))

        # She clicks on followees' link.
        wait_for(lambda: self.browser.find_element_by_link_text("Followees")).click()

        # She does not see meredith's name in the users' list
        wait_for(
            lambda: self.assertEqual(
                self.browser.current_url,
                self.live_server_url + reverse("users:network", args=["followees"]),
            )
        )
        user_list = wait_for(lambda: self.browser.find_element_by_id("user_list"))
        self.assertNotIn("Meredith", user_list.text)

        # Meredith goes to network page in her browser.
        edith_browser = self.browser
        self.browser = meredith_browser
        self.browser.get(self.live_server_url + reverse("users:network", args=["all"]))

        # She clicks on followers' link.
        wait_for(lambda: self.browser.find_element_by_link_text("Followers")).click()

        # She does not see Edith's name in users' list
        wait_for(
            lambda: self.assertEqual(
                self.browser.current_url,
                self.live_server_url + reverse("users:network", args=["followers"]),
            )
        )
        user_list = wait_for(lambda: self.browser.find_element_by_id("user_list"))
        self.assertNotIn("Edith", user_list.text)

        edith_browser.quit()