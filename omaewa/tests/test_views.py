import os
import pytz
from uuid import uuid4
from datetime import datetime

from django.conf import settings
from django.urls import reverse
from django.test import TestCase, Client

from omaewa.models import CustomUser
from omaewa.delete_all_user_data import delete_all


class TestViews(TestCase):
    def setUp(self):
        self.zipfile_dir = os.path.join(
            settings.OMAEWA_DIR, 'tests', 'takeout_eng_2.zip')
        assert os.path.exists(self.zipfile_dir)

        self.client = Client()
        self.credentials = {
            'username': 'DummyTestUser',
            'password': '12345678',
            'email': 'dslksdjnfiwjfiajffaqiwpdk@gmail.com'
        }
        self.test_user = CustomUser.objects.create(**self.credentials)
        self.test_user.set_password(self.credentials['password'])
        self.test_user.save()

        self.register_url = reverse('user_registration')
        self.login_url = reverse('user_login')
        self.youtube_url = reverse('youtube')
        self.confirm_random_uuid = reverse('conf_reg', args=[str(uuid4())])
        self.confirm_existing_uuid = reverse(
            'conf_reg', args=[self.test_user.random_url]
        )

    def tearDown(self):
        delete_all(self.test_user.username)

    def test_register_GET(self):
        response = self.client.get(self.register_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'omaewa/register.html')

    def test_login_GET(self):
        response = self.client.get(self.login_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'omaewa/login.html')

    def test_confirm_random_uuid_GET(self):
        response = self.client.get(self.confirm_random_uuid)

        self.assertEquals(response.status_code, 404)

    def test_confirm_existing_uuid_GET(self):
        response = self.client.get(self.confirm_existing_uuid)

        self.assertRedirects(response, reverse('user_login'))
        self.assertEquals(response.status_code, 302)

    def test_register_POST(self):
        response = self.client.post(self.register_url, self.credentials)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'omaewa/register.html')

    def test_login_authenticated(self):
        response_login = self.client.login(**self.credentials)
        response_youtube = self.client.get(self.youtube_url)

        self.assertTrue(response_login)
        self.assertEquals(response_youtube.status_code, 200)

    def test_youtube_post_zipfile(self):
        custom_dt = datetime(2016, 4, 17, 17, 45, 36, 752000, tzinfo=pytz.UTC)

        response_login = self.client.login(**self.credentials)
        self.assertTrue(response_login)

        with open(self.zipfile_dir, 'rb') as file:
            response = self.client.post(self.youtube_url, {'file': file})

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))
        self.assertEquals(self.test_user.youtubetextstats.count_watched, 21481)
        self.assertEquals(self.test_user.youtubetextstats.count_searches, 3734)
        self.assertEquals(self.test_user.youtubetextstats.count_liked, 422)
        self.assertEquals(self.test_user.youtubetextstats.first_liked,
                          'Maddyson играет в Battlefield 3: Close Quarters')
        self.assertEquals(self.test_user.youtubetextstats.first_liked_url,
                          'https://www.youtube.com/watch?v=CpjUBsxkFcs')
        self.assertEquals(self.test_user.youtubetextstats.first_search,
                          '+100500')
        self.assertEquals(self.test_user.youtubetextstats.first_watched_title,
                          'Супергерои на Пятнице Второй выпуск')
        self.assertEquals(self.test_user.youtubetextstats.first_watched_url,
                          'https://www.youtube.com/watch?v=PcRgkXxy5yM')

        self.assertEquals(self.test_user.youtubetextstats.first_watched_dt,
                          custom_dt)
