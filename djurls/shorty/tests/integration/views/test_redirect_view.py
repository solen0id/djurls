from datetime import datetime

import pytest
from django.urls import reverse_lazy
from django.utils import timezone

from djurls.shorty.models import ShortURL


@pytest.fixture
def redirect_url():
    def _redirect_url(short_key=None):
        return reverse_lazy("redirect", kwargs={"short_key": short_key})

    return _redirect_url


@pytest.mark.django_db
def test_redirect_model_lookup_failure_results_in_error(api_client, redirect_url):
    response = api_client.get(redirect_url(short_key="x"))

    assert response.status_code == 404


@pytest.mark.django_db
def test_redirect_user_can_redirect(api_client, redirect_url, default_url):
    short_url = ShortURL.objects.create(url=default_url)
    response = api_client.get(redirect_url(short_key=short_url.short_key))

    assert response.status_code == 302
    assert response.url == default_url


@pytest.mark.django_db
def test_redirect_unauthenticated_user_can_redirect_to_url_created_by_authenticated(
    alice_user, api_client, redirect_url, default_url
):
    short_url = ShortURL.objects.create(url=default_url, author=alice_user)
    response = api_client.get(redirect_url(short_key=short_url.short_key))

    assert response.status_code == 302
    assert response.url == default_url


@pytest.mark.django_db
def test_redirect_authenticated_user_can_redirect(
    alice_user, api_client_authenticated, redirect_url, default_url
):
    short_url = ShortURL.objects.create(url=default_url, author=alice_user)
    response = api_client_authenticated.get(redirect_url(short_key=short_url.short_key))

    assert response.status_code == 302
    assert response.url == default_url


@pytest.mark.django_db
def test_redirect_authenticated_user_can_redirect_to_url_created_by_authenticated(
    alice_user, api_client_authenticated, redirect_url, default_url
):
    short_url = ShortURL.objects.create(url=default_url, author=alice_user)
    response = api_client_authenticated.get(redirect_url(short_key=short_url.short_key))

    assert response.status_code == 302
    assert response.url == default_url


@pytest.mark.django_db
def test_redirect_preserves_query_params(api_client, redirect_url, default_url):
    short_url = ShortURL.objects.create(url=default_url)

    redirect_url = redirect_url(short_key=short_url.short_key)
    query_params = "?search=true&q=test"
    redirect_url_with_params = f"{redirect_url}?{query_params}"

    response = api_client.get(redirect_url_with_params)

    assert response.status_code == 302
    assert response.url == f"{default_url}?{query_params}"
