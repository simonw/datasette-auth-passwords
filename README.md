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
            "someusername_password_hash": {
                "$env": "PASSWORD_HASH_1"
            }
        }
    }
}
```

The password hash can now be specified in an environment variable when you run Datasette. You can do that like so:

    PASSWORD_HASH_1='pbkdf2_sha256$...' \
        datasette -m metadata.json

Be sure to use single quotes here otherwise the `$` symbols in the password hash may be incorrectly interpreted by your shell.

You will now be able to log in to your instance using the form at `/-/login` with `someusername` as the username and the password that you used to create your hash as the password.

You can include as many accounts as you like in the configuration, each with different usernames.

### Specifying actors

By default, a logged in user will result in an [actor block](https://datasette.readthedocs.io/en/stable/authentication.html#actors) that just contains their username:

```json
{
    "id": "someusername"
}
```

You can customize the actor that will be used for a username by including an `"actors"` configuration block, like this:

```json
{
    "plugins": {
        "datasette-auth-passwords": {
            "someusername_password_hash": {
                "$env": "PASSWORD_HASH_1"
            },
            "actors": {
                "someusername": {
                    "id": "someusername",
                    "name": "Some user"
                }
            }
        }
    }
}
```

### Using with datasette publish

If you are publishing data using a [datasette publish](https://datasette.readthedocs.io/en/stable/publish.html#datasette-publish) command you can use the `--plugin-secret` option to securely configure your password hashes (see [secret configuration values](https://datasette.readthedocs.io/en/stable/plugins.html#secret-configuration-values)).

You would run the command something like this:

    datasette publish cloudrun mydatabase.db \
        --install datasette-auth-passwords \
        --plugin-secret datasette-auth-passwords root_password_hash 'pbkdf2_sha256$...' \
        --service datasette-auth-passwords-demo

This will allow you to log in as username `root` using the password that you used to create the hash.

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
