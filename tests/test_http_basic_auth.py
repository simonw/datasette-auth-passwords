from datasette.app import Datasette
from datasette_auth_passwords import utils
import pytest
import httpx

# "password!"
PASSWORD_HASH = "pbkdf2_sha256$260000$a9bb87a3e9d968847a36c50cf1a4ac3d$UO1DUqulWhRLj8UZrnViiu6KaKn0C5M9IZKWB4R9JX4="

TEST_METADATA = {
    "plugins": {
        "datasette-auth-passwords": {
            "actors": {"user1": {"id": "userone", "name": "User 1"}},
            "user1_password_hash": PASSWORD_HASH,
            "user2_password_hash": PASSWORD_HASH,
            "http_basic_auth": True,
        }
    }
}


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "username,password,should_login",
    [
        ("user1", "password!", True),
        ("user1", "password", False),
        ("user2", "", False),
        ("user2", "password!", True),
        ("user3", "password!", False),
    ],
)
@pytest.mark.parametrize("path", ("/", "/-/404"))
async def test_basic_auth_login(path, username, password, should_login):
    ds = Datasette([], memory=True, metadata=TEST_METADATA)
    # Anonymous should 401
    anon_response = await ds.client.get(path)
    assert anon_response.status_code == 401
    # Try again with authorization header
    auth_response = await ds.client.get(path, auth=(username, password))
    if should_login:
        assert auth_response.status_code in (200, 404)
    else:
        assert auth_response.status_code == 401
