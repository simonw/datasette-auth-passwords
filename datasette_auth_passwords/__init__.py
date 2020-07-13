from datasette import hookimpl
from datasette.utils.asgi import Response
from .utils import hash_password


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


@hookimpl
def register_routes():
    return [
        (r"^/-/password-tool$", password_tool),
    ]
