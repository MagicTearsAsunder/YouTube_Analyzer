import os
from uuid import uuid4
from selenium import webdriver
from urllib.parse import urljoin
from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from omaewa.views import user_login


class TestOmaewaLoginPage(StaticLiveServerTestCase):
    def setUp(self):
        chromedriver_dir = os.path.join(
            settings.OMAEWA_DIR, 'functional_tests', 'chromedriver')

        assert os.path.exists(chromedriver_dir)

        self.driver = webdriver.Chrome(chromedriver_dir)

    def tearDown(self):
        self.driver.close()

    def test_login_page_alert_displayed_if_incorrect_credentials(self):
        self.driver.get(urljoin(self.live_server_url, reverse(user_login)))

        username_field = self.driver.find_element_by_name('username')
        password_field = self.driver.find_element_by_name('password')
        button = self.driver.find_element_by_id('login_submit')

        username_field.send_keys(str(uuid4()))
        password_field.send_keys(str(uuid4()))
        button.click()

        alert = self.driver.find_element_by_class_name('alert-primary')
        self.assertEquals(alert.text, 'Incorrect username and/or password')
