from django.contrib.auth import get_user_model

from .base_test import BaseTest

User = get_user_model()


class TestRoutes(BaseTest):

    def test_notes_list_for_different_users(self):
        users_statuses = (
            (self.author_client, True),
            (self.reader_client, False),
        )
        for user, value in users_statuses:
            with self.subTest():
                response = user.get(self.url_list)
                object_list = response.context['object_list']
                self.assertIs((self.note in object_list), value)

    def test_pages_contains_form(self):
        urls = (self.url_add_note, self.url_edit_note)
        for url in urls:
            with self.subTest():
                response = self.author_client.get(url)
                self.assertIn('form', response.context)
