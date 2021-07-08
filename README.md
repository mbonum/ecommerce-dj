# Clavem

Commands to set up the Clavem platform.

## Instructions for running locally on Debian 10 with Python 3.9:

1. Create project folder `mkdircd clvm`

2. Create a virtualenv using `python3 -m venv .`

3. Activate the virtualenv with `. bin/activate`

4. Install pip-tools using: `pip install pip-tools`

5. Run `pip-compile --output-file requirements.txt requirements.in && pip install -r requirements.txt`. This generates the requirements.txt file from the requirements.in file. If this doesn't work, try upgrading setuptools `pip install -U setuptools`.

## Start server:

./manage.py runserver

## Run tests:

./manage.py test

## Check for outdated root dependencies:

python scripts/list_outdated.py
