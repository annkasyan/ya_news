import pytest

from http import HTTPStatus

from django.urls import reverse
from pytest_django.asserts import assertFormError

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


@pytest.mark.django_db
def test_user_can_create_comment(author_client, author, new, form_data):
    url = reverse('news:detail', args=(new.id,))
    author_client.post(url, data=form_data)
    assert Comment.objects.count() == 1
    new_comment = Comment.objects.get()
    assert new_comment.news == form_data['news']
    assert new_comment.author == author
    assert new_comment.text == form_data['text']


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(client, new, form_data):
    url = reverse('news:detail', args=(new.id,))
    client.post(url, data=form_data)
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_user_cant_use_bad_words(author_client, new):
    url = reverse('news:detail', args=(new.id,))
    bad_words_data = {
        'news': new,
        'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'
    }
    response = author_client.post(url, data=bad_words_data)
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING,
    )
    comment_count = Comment.objects.count()
    assert comment_count == 0


@pytest.mark.django_db
def test_author_can_edit_comment(author_client, form_data, comment):
    url = reverse('news:edit', args=(comment.id,))
    author_client.post(url, data=form_data)
    comment.refresh_from_db()
    assert comment.text == form_data['text']


@pytest.mark.django_db
def test_other_user_cant_edit_comment(admin_client, form_data, comment):
    url = reverse('news:edit', args=(comment.id,))
    response = admin_client.post(url, data=form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment_from_db = Comment.objects.get(id=comment.id)
    assert comment.text == comment_from_db.text


@pytest.mark.django_db
def test_author_can_delete_comment(author_client, comment):
    url = reverse('news:delete', args=(comment.id,))
    author_client.post(url)
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_other_user_cant_delete_comment(admin_client, form_data, comment):
    url = reverse('news:delete', args=(comment.id,))
    response = admin_client.post(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1
