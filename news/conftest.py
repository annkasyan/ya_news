import pytest

from django.conf import settings
from django.utils import timezone

from news.models import Comment, News

from datetime import datetime, timedelta 


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def author_client(author, client):
    client.force_login(author)
    return client


@pytest.fixture
def new():
    new = News.objects.create(
        title='Заголовок новости',
        text='Текст новости',
    )
    return new


@pytest.fixture
def comment(author, new):
    comment = Comment.objects.create(
        news=new,
        author=author,
        text='Текст коммента',
    )
    return comment


@pytest.fixture
def news():
    today = datetime.today()
    news = News.objects.bulk_create(
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )
    return news


@pytest.fixture
def comments(author, new):
    now = timezone.now()
    for index in range(2):
        comment = Comment.objects.create(
            news=new,
            author=author,
            text=f'Tекст {index}',
        )
        comment.created = now + timedelta(days=index)
        comment.save()
    return comments


@pytest.fixture
def form_data(new, author):
    return {
        'news': new,
        'author': author,
        'text': 'New comment text',
    }
