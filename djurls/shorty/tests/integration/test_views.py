from datetime import datetime

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.utils import timezone
from rest_framework.test import APIClient

from djurls.shorty.models import ShortURL


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture()
def api_client_authenticated(alice_user, default_password):
    client = APIClient()
    client.login(username=alice_user.username, password=default_password)

    return client


@pytest.fixture()
def alice_user(db, default_password):
    User = get_user_model()
    user = User.objects.create(username="Alice - Test User", email="alice@test.de")
    user.set_password(default_password)
    user.save()

    return user


@pytest.fixture()
def bob_user(db, default_password):
    User = get_user_model()
    user = User.objects.create(username="Bob - Test User", email="bob@test.de")
    user.set_password(default_password)
    user.save()

    return user


@pytest.fixture(scope="module")
def default_password():
    return "testpassword"


@pytest.fixture()
def default_shorturl(db, default_url):
    return ShortURL.objects.create(url=default_url)


@pytest.fixture()
def default_shorturl_with_author(db, alice_user, default_url):
    return ShortURL.objects.create(author=alice_user, url=default_url)


@pytest.fixture()
def default_url():
    return "http://www.mytesturl.com"


@pytest.fixture()
def url_list_create():
    return reverse_lazy("url_list_create")


def timestamp_to_tz_aware_object(timestamp: str) -> datetime:
    timestamp = timestamp[:-1] if timestamp[-1].lower() == "z" else timestamp
    return timezone.make_aware(datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f"))


def test_unauthorized_user_can_view_empty_short_url_list(api_client, url_list_create):
    response = api_client.get(url_list_create)

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.django_db
def test_unauthorized_user_cannot_view_existing_urls_with_no_author(
    api_client, url_list_create, default_shorturl
):
    response = api_client.get(url_list_create)

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.django_db
def test_unauthorized_user_cannot_view_existing_urls_with_author(
    api_client, url_list_create, default_shorturl_with_author
):
    response = api_client.get(url_list_create)

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.django_db
def test_unauthorized_user_can_create_new_short_url(api_client, url_list_create):
    url_to_create = "https://www.mytesturl.com"
    response = api_client.post(
        url_list_create, data={"url": url_to_create}, format="json"
    )

    assert response.status_code == 201


@pytest.mark.django_db
def test_create_new_short_url_construction(api_client, url_list_create, default_url):
    before_create = timezone.now()
    data = {"url": default_url}

    response_json = api_client.post(url_list_create, data=data, format="json").json()

    assert response_json.get("url") == default_url
    assert response_json.get("times_accessed") == 0
    assert response_json.get("accessed_at") is None
    assert response_json.get("author") is None
    assert timestamp_to_tz_aware_object(response_json.get("created_at")) > before_create


@pytest.mark.django_db
def test_authorized_user_can_view_empty_short_url_list(
    api_client_authenticated, url_list_create
):
    response = api_client_authenticated.get(url_list_create)

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.django_db
def test_authorized_user_can_create_new_short_url(
    api_client_authenticated, url_list_create
):
    url_to_create = "https://www.mytesturl.com"
    response = api_client_authenticated.post(
        url_list_create, data={"url": url_to_create}, format="json"
    )

    assert response.status_code == 201


@pytest.mark.django_db
def test_authorized_user_cannot_view_existing_urls_with_no_author(
    api_client_authenticated, url_list_create, default_shorturl
):
    response = api_client_authenticated.get(url_list_create)

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.django_db
def test_authorized_user_can_view_existing_urls_he_created_himself(
    api_client_authenticated, url_list_create, default_shorturl_with_author, alice_user
):
    response = api_client_authenticated.get(url_list_create)
    response_json = response.json()

    assert response.status_code == 200
    assert len(response_json) == 1
    assert response_json[0]["author"] == alice_user.username


@pytest.mark.django_db
def test_authorized_user_cannot_view_existing_urls_other_authorized_users_created(
    api_client_authenticated, url_list_create, bob_user, default_url
):
    ShortURL.objects.create(author=bob_user, url=default_url)
    response = api_client_authenticated.get(url_list_create)

    assert response.status_code == 200
    assert response.json() == []
