from click.testing import CliRunner
from datasette.cli import cli
from datasette_auth_passwords.utils import verify_password


def test_hash_password_interactive():
    runner = CliRunner()
    result = runner.invoke(cli, ["hash-password"], input="hello\nhello\n")
    lines = result.output.split("\n")
    assert lines[0] == "Password: "
    assert lines[1] == "Repeat for confirmation: "
    hashed = lines[2]
    assert hashed.startswith("pbkdf2_sha256$")
    assert verify_password("hello", hashed)


def test_hash_password_no_confirm():
    runner = CliRunner()
    result = runner.invoke(cli, ["hash-password", "--no-confirm"], input="hello2")
    lines = result.output.split("\n")
    hashed = lines[0]
    assert hashed.startswith("pbkdf2_sha256$")
    assert verify_password("hello2", hashed)
