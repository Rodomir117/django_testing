from http import HTTPStatus

from django.contrib.auth import get_user_model
from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note
from notes.tests.base_test import BaseTest

User = get_user_model()


class TestLogic(BaseTest):
    """Тесты логики работы заметок."""

    def test_user_can_create_note(self):
        """Пользователь может создать заметку."""
        response = self.author_client.post(
            self.url_add_note, data=self.form_data
        )
        self.assertRedirects(response, self.url_add_success)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 2)
        self.assertEqual(self.note.text, self.TEXT)
        self.assertEqual(self.note.author, self.author)

    def test_anonymous_cant_create_note(self):
        """Анонимный пользователь не может создать заметку."""
        response = self.client.post(self.url_add_note, self.form_data)
        expected_url = f'{self.url_login}?next={self.url_add_note}'
        self.assertRedirects(response, expected_url)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)

    def test_unique_slug(self):
        """Уникальность slug для заметки."""
        note_count = Note.objects.count()
        self.form_data['slug'] = self.SLUG
        response = self.author_client.post(
            self.url_add_note, data=self.form_data)
        self.assertFormError(
            response, 'form', 'slug', errors=f'{self.SLUG}{WARNING}'
        )
        self.assertEqual(Note.objects.count(), note_count)

    def test_empty_slug(self):
        """Автоматическая генерация slug, если он не задан."""
        Note.objects.all().delete()
        self.form_data.pop('slug')
        response = self.author_client.post(
            self.url_add_note, data=self.form_data
        )
        self.assertRedirects(response, self.url_add_success)
        self.assertEqual(Note.objects.count(), 1)
        new_note = Note.objects.get(title=self.form_data['title'])
        self.assertEqual(new_note.slug, slugify(self.form_data['title']))
        self.assertEqual(new_note.title, self.form_data['title'])

    def test_author_can_edit_note(self):
        """Автор может редактировать заметку."""
        response = self.author_client.post(
            self.url_edit_note, data=self.form_data
        )
        self.assertRedirects(response, self.url_add_success)
        self.note.refresh_from_db()
        self.assertEqual(self.note.text, self.form_data['text'])

    def test_author_can_delete_note(self):
        """Автор может удалить заметку."""
        response = self.author_client.post(self.url_delete_note)
        self.assertRedirects(response, self.url_add_success)
        self.assertEqual(Note.objects.count(), 0)

    def test_not_author_cant_edit_note(self):
        """Не автор не может редактировать чужую заметку."""
        response = self.reader_client.post(
            self.url_edit_note, data=self.form_data
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.note.refresh_from_db()
        self.assertNotEqual(self.note.text, self.form_data['text'])

    def test_not_author_cant_delete_note(self):
        """Не автор не может удалить чужую заметку."""
        response = self.reader_client.post(self.url_delete_note)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(Note.objects.count(), 1)
