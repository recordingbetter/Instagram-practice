from django.test import TestCase
from django.urls import reverse, resolve

from member import views


class LoginViewTest(TestCase):
    VIEW_URL = '/member/login/'
    VIEW_URL_NAME = 'member:login'

    def test_url_equal_reverse_url_name(self):
        self.assertEqual(self.VIEW_URL, reverse(self.VIEW_URL_NAME))

    def test_url_resolve_to_login_view(self):
        found = resolve(self.VIEW_URL)
        # print(found)
        # print(found.func)
        # print(views.login)
        self.assertEqual(found.func, views.login)

    def test_uses_login_template(self):
        url = reverse('member:login')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'member/login.html')
