import pytest

from django.urls import reverse


@pytest.mark.django_db
def test_news_count(client, news):
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    news_count = len(object_list)
    assert news_count == 10


@pytest.mark.django_db
def test_news_order(client, news):
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


@pytest.mark.django_db
def test_comments_order(client, new, comments):
    url = reverse('news:detail', args=(new.id,))
    response = client.get(url)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    assert all_comments[0].created < all_comments[1].created


@pytest.mark.django_db
def test_availability_comment_form_for_logined_user(author_client, new):
    url = reverse('news:detail', args=(new.id,))
    response = author_client.get(url)
    assert 'form' in response.context


@pytest.mark.django_db
def test_no_comment_form_for_anonymous_user(client, new):
    url = reverse('news:detail', args=(new.id,))
    response = client.get(url)
    assert 'form' not in response.context
