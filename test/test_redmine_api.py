import os
import pytest
import requests


@pytest.fixture
def redmine_config():
    url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_API_KEY")
    if not url or not api_key:
        pytest.skip("REDMINE_URL or REDMINE_API_KEY not set")
    return url.rstrip("/"), api_key


def test_current_user(redmine_config):
    url, api_key = redmine_config
    endpoint = f"{url}/users/current.json"

    headers = {"X-Redmine-API-Key": api_key}

    response = requests.get(endpoint, headers=headers)

    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    data = response.json()
    assert "user" in data, "Response does not contain 'user'"
    assert "id" in data["user"], "User data missing 'id'"
