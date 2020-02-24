from uuid import uuid4
from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve
from omaewa.urls import urlpatterns
from omaewa.views import (
    index,
    user_registration,
    user_login,
    user_logout,
    conf_reg,
    category_page,
    post_page,
    youtube,
)


class TestUrls(SimpleTestCase):

    def test_all_urls_are_resolved(self):
        views_tuple = (
            index,
            user_registration,
            user_login,
            user_logout,
            conf_reg,
            category_page,
            post_page,
            youtube,
        )

        arguments = [None] * len(views_tuple)
        # Customise url arguments below
        arguments[views_tuple.index(conf_reg)] = (str(uuid4()),)

        for i, url_path in enumerate(urlpatterns):
            url = reverse(url_path.name, args=arguments[i])
            self.assertEquals(resolve(url).func, views_tuple[i])
