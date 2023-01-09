from datasette.app import Datasette
from datasette_auth_passwords import utils
import pytest

# "password!"
PASSWORD_HASH = "pbkdf2_sha256$260000$a9bb87a3e9d968847a36c50cf1a4ac3d$UO1DUqulWhRLj8UZrnViiu6KaKn0C5M9IZKWB4R9JX4="

TEST_METADATA = {
    "plugins": {
        "datasette-auth-passwords": {
            "actors": {"user1": {"id": "userone", "name": "User 1"}},
            "user1_password_hash": PASSWORD_HASH,
            "user2_password_hash": PASSWORD_HASH,
        }
    }
}


@pytest.mark.asyncio
async def test_plugin_is_installed():
    ds = Datasette(memory=True)
    response = await ds.client.get("/-/plugins.json")
    assert response.status_code == 200
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
    # Should pass if there is trailing whitespace
    assert utils.verify_password("hello", hashed_password + "\n")
    assert not utils.verify_password("hello2", hashed_password)
    # Should fail if hashed_password is invalid:
    assert not utils.verify_password("hello3", None)
    assert not utils.verify_password("hello3", "Only$two$dollars")


@pytest.mark.asyncio
async def test_password_tool():
    ds = Datasette(memory=True)
    response1 = await ds.client.get("/-/password-tool")
    csrftoken = response1.cookies["ds_csrftoken"]
    response2 = await ds.client.post(
        "/-/password-tool",
        data={"csrftoken": csrftoken, "password": "password!"},
    )
    html = response2.text
    assert ">pbkdf2_sha256$" in html
    password_hash = "pbkdf2_sha256$" + html.split(">pbkdf2_sha256$")[1].split("<")[0]
    assert utils.verify_password("password!", password_hash)


@pytest.mark.asyncio
async def test_login_warning_no_accounts():
    ds = Datasette(memory=True)
    message = "This instance does not have any configured accounts"
    response = await ds.client.get("/-/login")
    assert message in response.text
    ds2 = Datasette(memory=True, metadata=TEST_METADATA)
    response2 = await ds2.client.get("/-/login")
    assert message not in response2.text


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "username,password,should_login,expected_username",
    [
        ("user1", "password!", True, "userone"),
        ("user1", "password", False, None),
        ("user2", "", False, None),
        ("user2", "password!", True, "user2"),
        ("user3", "password!", False, None),
    ],
)
async def test_login(username, password, should_login, expected_username):
    ds = Datasette(memory=True, metadata=TEST_METADATA)
    # Menu should show 'Log in' option
    html = (await ds.client.get("/")).text
    LOG_IN = '<li><a href="/-/login">Log in</a></li>'
    LOG_OUT = '<form action="/-/logout" method="post">'
    assert LOG_IN in html
    assert LOG_OUT not in html
    # Get csrftoken
    csrftoken = (await ds.client.get("/-/login")).cookies["ds_csrftoken"]
    response = await ds.client.post(
        "/-/login",
        data={"csrftoken": csrftoken, "username": username, "password": password},
    )
    if should_login:
        assert response.status_code == 302
        ds_actor_cookie = response.cookies["ds_actor"]
        ds_actor = ds.unsign(ds_actor_cookie, "actor")["a"]
        assert ds_actor["id"] == expected_username
        # Now that user is logged in, menu should show 'Log out' option
        html = (await ds.client.get("/", cookies={"ds_actor": ds_actor_cookie})).text
        assert LOG_IN not in html
        assert LOG_OUT in html
    else:
        assert response.status_code == 200
        assert "Invalid username or password" in response.text
