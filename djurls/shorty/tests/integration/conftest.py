import pytest
from django.contrib.auth import get_user_model
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
