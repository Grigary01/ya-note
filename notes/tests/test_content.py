# type: ignore
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase
from notes.models import Note
from notes.forms import NoteForm
from django.conf import settings

User = get_user_model()


class TestHomePage(TestCase):
    HOME_URL = reverse('notes:list')

    @classmethod
    def setUpTestData(cls):
        all_notes = []
        cls.author = User.objects.create(username='Автор')
        for index in range(1, settings.NOTE_COUNT_ON_HOME_PAGE + 1):
            note = Note(
                title=f'Заметка {index}',
                text='Текс',
                slug=f'note-{index}',
                author=cls.author
            )
            all_notes.append(note)
        Note.objects.bulk_create(all_notes)

    def test_note_count(self):
        self.client.force_login(self.author)
        response = self.client.get(self.HOME_URL)
        self.assertIsNotNone(response.context)
        object_list = response.context['object_list']
        print(object_list)
        new_count = object_list.count()
        self.assertEqual(new_count, settings.NOTE_COUNT_ON_HOME_PAGE)


class TestDetailPage(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            slug='address-for-page-with-note',
            author=cls.author
        )
        cls.add_url = reverse('notes:add')
