import base64
import hashlib
import secrets

ALGORITHM = "pbkdf2_sha256"


def hash_password(password, salt=None, iterations=260000):
    if salt is None:
        salt = secrets.token_hex(16)
    assert salt and isinstance(salt, str) and "$" not in salt
    assert isinstance(password, str)
    pw_hash = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt.encode("utf-8"), iterations
    )
    b64_hash = base64.b64encode(pw_hash).decode("ascii").strip()
    return "{}${}${}${}".format(ALGORITHM, iterations, salt, b64_hash)


def verify_password(password, password_hash):
    if (password_hash or "").count("$") != 3:
        return False
    algorithm, iterations, salt, b64_hash = password_hash.split("$", 3)
    iterations = int(iterations)
    assert algorithm == ALGORITHM
    compare_hash = hash_password(password, salt, iterations)
    return secrets.compare_digest(password_hash, compare_hash)


def scope_has_valid_authorization(scope, datasette):
    config = datasette.plugin_config("datasette-auth-passwords") or {}
    accounts = {
        key.split("_password_hash")[0]: value
        for key, value in config.items()
        if key.endswith("_password_hash")
    }
    actors = config.get("actors") or {}
    headers = dict(scope.get("headers") or {})
    authorization = headers.get(b"authorization") or b""
    if not authorization.startswith(b"Basic "):
        return None
    credentials = authorization.split(b"Basic ")[1]
    decoded = base64.b64decode(credentials).decode("ascii")
    username, _, password = decoded.partition(":")
    password_hash = accounts.get(username)
    if password_hash and verify_password(password, password_hash):
        print("verified")
        return actors.get(username) or {"id": username}
    else:
        print("no match", accounts, username, password, password_hash)
        return None
