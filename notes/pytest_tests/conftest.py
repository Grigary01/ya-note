# type:ignore
import pytest
from django.test.client import Client
from notes.models import Note


@pytest.fixture
def client_fixture(request):
    """Фикстура, возвращающая клиента based on параметра"""
    client_name = request.param
    return request.getfixturevalue(client_name)


@pytest.fixture
def args(request):
    """Фикстура, возвращающая аргументы based on параметра"""
    args_value = request.param
    if args_value == 'slug_for_args':

        note = request.getfixturevalue('note')
        return [note.slug]
    return args_value


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def note(author):
    note = Note.objects.create(
        title='Заголовок',
        text='Текст заметки',
        slug='note-slug',
        author=author,
    )
    return note


@pytest.fixture
def form_data():
    return {
        'title': 'Новый заголовок',
        'text': 'Новый текст',
        'slug': 'new-slug'
    }


@pytest.fixture
def slug_for_page(note):
    return (note.slug,)


@pytest.fixture
def no_args():
    return None
