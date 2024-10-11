import pytest

from news.pytest_tests.conftest import ANONYMOUS, AUTHOR

pytestmark = [pytest.mark.django_db]


def test_news_count_order(client, home_url, bulk_news_creation):
    """Новости отсортированы по дате в порядке убывания."""
    response = client.get(home_url)
    object_list = list(response.context['object_list'])
    assert object_list == sorted(
        object_list, key=lambda x: x.date, reverse=True
    )


def test_comments_order(client, detail_url, news, multiple_comments):
    """Комментарии отсортированы по времени создания в порядке убывания."""
    response = client.get(detail_url)
    news = response.context['news']
    all_comments = list(news.comment_set.all())
    assert 'news' in response.context
    assert all_comments == sorted(all_comments, key=lambda x: x.created)


@pytest.mark.parametrize(
    'current_client, status',
    ((ANONYMOUS, False), (AUTHOR, True)),
)
def test_anonymous_has_no_form(
    current_client,
    detail_url,
    status,
    comment
):
    """Анонимный пользователь не видит форму для комментариев."""
    response = current_client.get(detail_url)
    assert ('form' in response.context) is status
