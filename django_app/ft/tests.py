# ft = function test

from django.test import LiveServerTestCase
from django.urls import reverse
from selenium import webdriver

from member.models import User


class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(1)

    def tearDown(self):
        self.browser.quit()

    def test_root_url_redirect_to_post_list(self):
        self.browser.get(self.live_server_url)

        post_list_url = reverse('post:post_list')

        self.assertEqual(
            self.live_server_url + post_list_url,
            self.browser.current_url
            )

    def test_not_authenticated_user_redirect_to_login_view(self):
        urls = [
            '/member/profile',
            '/member/profile_edit/',
            '/post/create/',
            ]
        for url in urls:
            self.browser.get(self.live_server_url + url)
            self.assertIn(
                self.live_server_url + '/member/login',
                self.browser.current_url
                )

    def test_not_authenticated_user_can_view_login_form(self):
        test_username = 'username'
        test_password = 'password'
        User.objects.create_user(
            username=test_username,
            password=test_password,
            )
        # 로그인하지 않은 유저가 로그인폼을 이용해서 로그인할 수 있는지 테스트
        self.browser.get(self.live_server_url)
        form_login = self.browser.find_element_by_class_name('form-inline-login')
        input_username = form_login.find_element_by_id('id_username')
        input_password = form_login.find_element_by_id('id_password')
        button_submit = form_login.find_element_by_tag_name('button')
        # 폼에 값을 입력하고 로그인버튼 클릭
        input_username.send_keys(test_username)
        input_password.send_keys(test_password)
        button_submit.click()

        top_header = self.browser.find_element_by_class_name('top-header')

