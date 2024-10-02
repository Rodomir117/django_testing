from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class BaseTest(TestCase):

    AUTHOR = 'Кайл Брафловски'
    READER = 'Эрик Картман'
    ANONYMOUS = 'anonymous'
    SLUG = 'short_text-3'
    TITLE = 'Заголовок'
    TEXT = 'Какой-то текст'
    NEW_SLUG = 'short_text-5'
    NEW_TITLE = 'Какой-то новый заголовок'
    NEW_TEXT = 'Какой-то новый текст'

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username=cls.AUTHOR)
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader = User.objects.create(username=cls.READER)
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
        cls.note = Note.objects.create(
            author=cls.author,
            slug=cls.SLUG,
            title=cls.TITLE,
            text=cls.TEXT,
        )
        cls.form_data = {
            'title': cls.NEW_TITLE,
            'text': cls.NEW_TEXT,
            'slug': cls.NEW_SLUG
        }
        cls.url_home = reverse('notes:home')
        cls.url_add_note = reverse('notes:add')
        cls.url_add_success = reverse('notes:success')
        cls.url_detail = reverse('notes:detail', args=(cls.SLUG,))
        cls.url_edit_note = reverse('notes:edit', args=(cls.SLUG,))
        cls.url_delete_note = reverse('notes:delete', args=(cls.SLUG,))
        cls.url_list = reverse('notes:list')
        cls.url_login = reverse('users:login')
        cls.url_logout = reverse('users:logout')
        cls.url_signup = reverse('users:signup')
