from datasette.app import Datasette
from datasette_auth_passwords import utils
import pytest
import httpx


@pytest.mark.asyncio
async def test_plugin_is_installed():
    app = Datasette([], memory=True).app()
    async with httpx.AsyncClient(app=app) as client:
        response = await client.get("http://localhost/-/plugins.json")
        assert 200 == response.status_code
        installed_plugins = {p["name"] for p in response.json()}
        assert "datasette-auth-passwords" in installed_plugins


def test_utils_hash_password():
    hashed_password = utils.hash_password("hello")
    assert hashed_password.count("$") == 3
    assert hashed_password.startswith("pbkdf2_sha256$")
    # Running same agains should return a different password
    hashed_password2 = utils.hash_password("hello")
    assert hashed_password2 != hashed_password


def test_verify_password():
    hashed_password = utils.hash_password("hello")
    assert utils.verify_password("hello", hashed_password)
    assert not utils.verify_password("hello2", hashed_password)
