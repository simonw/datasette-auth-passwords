# datasette-auth-passwords

[![PyPI](https://img.shields.io/pypi/v/datasette-auth-passwords.svg)](https://pypi.org/project/datasette-auth-passwords/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-auth-passwords?label=changelog)](https://github.com/simonw/datasette-auth-passwords/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-auth-passwords/blob/master/LICENSE)

Datasette plugin for authenticating access using passwords

## Installation

Install this plugin in the same environment as Datasette.

    $ pip install datasette-auth-passwords

## Usage

This plugin works based on a list of username/password accounts that are hard-coded into the plugin configuration.

First, you'll need to create a password hash. You can do this using the tool located at `/-/password-tool` when the plugin is installed.

Now add the following to your `metadata.json`:

```json
{
    "plugins": {
        "datasette-auth-passwords": {
            "accounts": {
                "your_username": {
                    "password_hash": {
                        "$env": "PASSWORD_HASH_1"
                    },
                    "actor": {
                        "id": "your_username"
                    }
                }
            }
        }
    }
}
```

The password hash can now be specified in an environment variable when you run Datasette. You can do that like so:

    PASSWORD_HASH_1="pbkdf2_sha256$..." \
        datasette -m metadata.json

Or by using the `--plugin-secret` option to `datasette publish`, see [Secret configuration values](https://datasette.readthedocs.io/en/stable/plugins.html#secret-configuration-values).

You will now be able to log in to your instance using the form at `/-/login` with `your_username` as the username and the password that you used to create your hash as the password.

You can include as many accounts as you like in the configuration, each with different usernames.

The `"actor"` block in each one is the actor that will be authenticated - see [Actors](https://datasette.readthedocs.io/en/stable/authentication.html#actors) in the Datasette documentation for details.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-auth-passwords
    python3 -mvenv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and tests:

    pip install -e '.[test]'

To run the tests:

    pytest
