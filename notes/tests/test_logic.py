from http import HTTPStatus
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from notes.models import Note
from django.urls import reverse

User = get_user_model()


class TestNoteCreation(TestCase):
    NOTES_TITLE = 'Заголовок записки'
    NOTES_TEXT = 'Текст записки'
    NOTES_SLUG = 'address-for-page-with-note'

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.url = reverse('notes:add')
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.author)
        cls.form_data = {'title': cls.NOTES_TITLE,
                         'text': cls.NOTES_TEXT,
                         'slug': cls.NOTES_SLUG}

    def test_anonymous_user_cant_create_note(self):
        self.client.post(self.url, data=self.form_data)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 0)

    def test_user_can_create_note(self):
        self.auth_client.post(self.url, data=self.form_data)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)
        note = Note.objects.get()
        self.assertEqual(note.title, self.NOTES_TITLE)
        self.assertEqual(note.text, self.NOTES_TEXT)
        self.assertEqual(note.slug, self.NOTES_SLUG)


class TestNoteEditDelete(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор заметки')
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            slug='address-for-page-with-note',
            author=cls.author
        )
        note_url = reverse('notes:detail', args=(cls.note.slug,))
        cls.url_to_notes = '/done/'
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader = User.objects.create(username='Читатель')
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
        cls.edit_url = reverse('notes:edit', args=(cls.note.slug,))
        cls.delete_url = reverse('notes:delete', args=(cls.note.slug,))

    def test_author_can_delete_note(self):
        response = self.author_client.delete(self.delete_url)
        self.assertRedirects(response, self.url_to_notes)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 0)

    def test_user_cant_delete_comment_of_another_user(self):
        response = self.reader_client.delete(self.delete_url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        comments_count = Note.objects.count()
        self.assertEqual(comments_count, 1)
