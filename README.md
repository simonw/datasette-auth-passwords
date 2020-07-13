# datasette-auth-passwords

[![PyPI](https://img.shields.io/pypi/v/datasette-auth-passwords.svg)](https://pypi.org/project/datasette-auth-passwords/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-auth-passwords?label=changelog)](https://github.com/simonw/datasette-auth-passwords/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-auth-passwords/blob/master/LICENSE)

Datasette plugin for authenticating access using passwords

## Installation

Install this plugin in the same environment as Datasette.

    $ pip install datasette-auth-passwords

## Usage

Usage instructions go here.

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
