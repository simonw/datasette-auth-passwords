from datasette import hookimpl
from datasette.utils.asgi import Response
from .utils import hash_password, verify_password


async def password_tool(request, datasette):
    post_vars = await request.post_vars()
    password = post_vars.get("password")
    hashed_password = None
    if password:
        hashed_password = hash_password(password)
    return Response.html(
        await datasette.render_template(
            "password_tool.html", {"hashed_password": hashed_password,}, request=request
        )
    )


async def password_login(request, datasette):
    config = datasette.plugin_config("datasette-auth-passwords") or {}
    accounts = {
        key.split("_password_hash")[0]: value
        for key, value in config.items()
        if key.endswith("_password_hash")
    }
    actors = config.get("actors") or {}
    error = None
    if not accounts:
        error = "This instance does not have any configured accounts"
    post_vars = await request.post_vars()
    username = post_vars.get("username") or ""
    password = post_vars.get("password") or ""
    if request.method == "POST":
        # Look up user
        password_hash = accounts.get(username)
        if password_hash and verify_password(password, password_hash):
            actor = actors.get(username) or {"id": "username"}
            response = Response.redirect("/")
            response.set_cookie("ds_actor", datasette.sign({"a": actor}, "actor"))
            return response
        else:
            error = "Invalid username or password"

    return Response.html(
        await datasette.render_template(
            "password_login.html", {"error": error}, request=request
        )
    )


@hookimpl
def register_routes():
    return [
        (r"^/-/password-tool$", password_tool),
        (r"^/-/login$", password_login),
    ]
