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
    # Running same again should return a different password
    hashed_password2 = utils.hash_password("hello")
    assert hashed_password2 != hashed_password


def test_verify_password():
    hashed_password = utils.hash_password("hello")
    assert utils.verify_password("hello", hashed_password)
    assert not utils.verify_password("hello2", hashed_password)


@pytest.mark.asyncio
async def test_password_tool():
    app = Datasette([], memory=True).app()
    async with httpx.AsyncClient(app=app) as client:
        response1 = await client.get("http://localhost/-/password-tool")
        csrftoken = response1.cookies["ds_csrftoken"]
        response2 = await client.post(
            "http://localhost/-/password-tool",
            data={"csrftoken": csrftoken, "password": "password!"},
        )
        html = response2.text
        assert ">pbkdf2_sha256$" in html
        password_hash = (
            "pbkdf2_sha256$" + html.split(">pbkdf2_sha256$")[1].split("<")[0]
        )
        assert utils.verify_password("password!", password_hash)
