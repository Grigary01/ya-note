# type: ignore
import pytest
from django.urls import reverse
from notes.forms import NoteForm


@pytest.mark.parametrize(
    'client_fixture, note_in_list',
    (
        ('author_client', True),
        ('not_author_client', False),
    ),
    indirect=['client_fixture']
)
def test_notes_list_for_different_users(
    note, client_fixture, note_in_list
):
    url = reverse('notes:list')
    response = client_fixture.get(url)
    object_list = response.context['object_list']
    assert (note in object_list) is note_in_list


@pytest.mark.parametrize(
    'name, args',
    (
        ('notes:add', None),
        ('notes:edit', 'slug_for_args')
    ),
    indirect=['args']
)
def test_pages_contains_form(author_client, name, args):
    url = reverse(name, args=args)
    response = author_client.get(url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], NoteForm)
