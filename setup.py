from setuptools import setup
import os

VERSION = "1.0"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="datasette-auth-passwords",
    description="Datasette plugin for authenticating access using passwords",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Simon Willison",
    url="https://github.com/simonw/datasette-auth-passwords",
    project_urls={
        "Issues": "https://github.com/simonw/datasette-auth-passwords/issues",
        "CI": "https://github.com/simonw/datasette-auth-passwords/actions",
        "Changelog": "https://github.com/simonw/datasette-auth-passwords/releases",
    },
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["datasette_auth_passwords"],
    entry_points={"datasette": ["auth_passwords = datasette_auth_passwords"]},
    install_requires=["datasette>=0.59"],
    extras_require={"test": ["pytest", "pytest-asyncio", "httpx"]},
    package_data={
        "datasette_auth_passwords": [
            "templates/*.html",
        ]
    },
)
