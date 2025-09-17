# type: ignore
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase
from notes.models import Note
from notes.forms import NoteForm

User = get_user_model()


class TestHomePage(TestCase):
    HOME_URL = reverse('notes:list')

    @classmethod
    def setUpTestData(cls):
        cls.reader = User.objects.create(username='Посетитель')
        cls.author = User.objects.create(username='Автор')
        cls.note = Note.objects.create(
            title='Заметка',
            text='Текст',
            slug='note',
            author=cls.author
        )

    def test_notes_list_for_author(self):
        self.client.force_login(self.author)
        url = reverse('notes:list')
        response = self.client.get(url)
        object_list = response.context['object_list']
        self.assertIn(self.note, object_list)

    def test_notes_list_for_reader(self):
        self.client.force_login(self.reader)
        url = reverse('notes:list')
        response = self.client.get(url)
        object_list = response.context['object_list']
        self.assertNotIn(self.note, object_list)

    def test_pages_contains_form(self):
        urls = (
            ('notes:add', None),
            ('notes:edit', (self.note.slug,))
        )
        self.client.force_login(self.author)
        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)

