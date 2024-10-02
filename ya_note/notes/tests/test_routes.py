from http import HTTPStatus

from django.contrib.auth import get_user_model

from notes.tests.base_test import BaseTest

User = get_user_model()


class TestRoutes(BaseTest):

    def test_pages_availability(self):
        urls = (
            (self.url_home, self.client, HTTPStatus.OK, self.ANONYMOUS),
            (self.url_login, self.client, HTTPStatus.OK, self.ANONYMOUS),
            (self.url_logout, self.client, HTTPStatus.OK, self.ANONYMOUS),
            (self.url_signup, self.client, HTTPStatus.OK, self.ANONYMOUS),
            (self.url_detail, self.author_client, HTTPStatus.OK, self.AUTHOR),
            (self.url_edit_note, self.author_client, HTTPStatus.OK,
             self.AUTHOR),
            (self.url_delete_note, self.author_client, HTTPStatus.OK,
             self.AUTHOR),
            (self.url_add_note, self.reader_client, HTTPStatus.OK,
             self.READER),
            (self.url_add_success, self.reader_client, HTTPStatus.OK,
             self.READER),
            (self.url_list, self.reader_client, HTTPStatus.OK, self.READER),
            (self.url_detail, self.reader_client, HTTPStatus.NOT_FOUND,
             self.READER),
            (self.url_edit_note, self.reader_client, HTTPStatus.NOT_FOUND,
             self.READER),
            (self.url_delete_note, self.reader_client, HTTPStatus.NOT_FOUND,
             self.READER),
        )
        for current_url, current_client, status, user in urls:
            with self.subTest():
                self.assertEqual(
                    current_client.get(current_url).status_code,
                    status)

    def test_redirects(self):
        urls = (
            self.url_add_note,
            self.url_add_success,
            self.url_detail,
            self.url_edit_note,
            self.url_delete_note,
            self.url_list,
        )
        for url in urls:
            with self.subTest():
                redirect_url = f'{self.url_login}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
