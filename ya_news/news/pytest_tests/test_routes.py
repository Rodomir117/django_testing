from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects

from .conftest import ANONYMOUS, AUTHOR, READER

pytestmark = [pytest.mark.django_db]


@pytest.mark.parametrize(
    'current_url, current_client, status', (
        (pytest.lazy_fixture('home_url'), ANONYMOUS, HTTPStatus.OK),
        (pytest.lazy_fixture('detail_url'), ANONYMOUS, HTTPStatus.OK),
        (pytest.lazy_fixture('login_url'), ANONYMOUS, HTTPStatus.OK),
        (pytest.lazy_fixture('logout_url'), ANONYMOUS, HTTPStatus.OK),
        (pytest.lazy_fixture('signup_url'), ANONYMOUS, HTTPStatus.OK),
        (pytest.lazy_fixture('delete_comment_url'), AUTHOR, HTTPStatus.OK),
        (pytest.lazy_fixture('edit_comment_url'), AUTHOR, HTTPStatus.OK),
        (pytest.lazy_fixture('delete_comment_url'), READER,
            HTTPStatus.NOT_FOUND),
        (pytest.lazy_fixture('edit_comment_url'), READER,
            HTTPStatus.NOT_FOUND),
    )
)
def test_pages_availability_for_anonymous(
    current_url, current_client, status
):
    response = current_client.get(current_url)
    assert response.status_code == status


@pytest.mark.parametrize(
    'current_url',
    (
        pytest.lazy_fixture('delete_comment_url'),
        pytest.lazy_fixture('edit_comment_url')
    ),
)
def test_redirect_for_anonymous(client, current_url, login_url, comment):
    expected_url = f'{login_url}?next={current_url}'
    response = client.get(current_url)
    assertRedirects(response, expected_url)
