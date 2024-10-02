from datetime import date

import pytest
from django.conf import settings
from django.utils import timezone

from .conftest import ANONYMOUS, AUTHOR

pytestmark = [pytest.mark.django_db]


def test_news_count_order(client, home_url, bulk_news_creation):
    response = client.get(home_url)
    object_list = list(response.context['object_list'])
    assert len(object_list) == settings.NEWS_COUNT_ON_HOME_PAGE
    assert isinstance(object_list[0].date, date)
    assert object_list == sorted(
        object_list, key=lambda x: x.date, reverse=True
    )


def test_comments_order(client, detail_url, news, list_comments):
    response = client.get(detail_url)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = list(news.comment_set.all())
    assert isinstance(all_comments[0].created, timezone.datetime)
    assert all_comments == sorted(all_comments, key=lambda x: x.created)


@pytest.mark.parametrize(
    'current_client, status',
    ((ANONYMOUS, False), (AUTHOR, True)),
)
def test_anonymous_hasnt_form(
    current_client,
    detail_url,
    status,
    comment
):
    response = current_client.get(detail_url)
    assert ('form' in response.context) is status
