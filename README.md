# Call Calculator

This REST api records phone calls (start and end) from source to destination, calculating the call prince in the end,
and it provides billings per year or month.

## Environment used to run this project

Computer: Samsung Expert - 16GB RAM - intel core i7

OS: Ubuntu 18.04.2 LTS 64 bits

IDE: Pycharm Community Edition 2019.1.3

Libraries: 
- Python 3.6.8 with pip 19.1.1
- Pipenv 2018.11.26
- Django 2.2.3
- Django REST Framework 3.9.4


## API Docs

Run the application locally and access in /docs endpoint (eg http://127.0.0.1:8000/docs)

## Requirements

- [Python 3.6.8](https://www.python.org/downloads/release/python-368/)
- [pip](https://pypi.org/project/pip/)

Optional:

- [Pipenv](https://github.com/pypa/pipenv)
- [Make](https://www.gnu.org/software/make/)

## Setup

For a local setup, the most convenient way is by installing all dependencies via pipenv:

`pipenv install --dev`

It will create a virtual environment with all dependencies

But if you prefer setup in other virtual environment, just run:

`pip install -r requirements.txt`

## Tests

For tests running, you should install all development dependencies. It can be installed with pipenv by running:

`pipenv install --dev`

or

`make pipenv-setup-dev`

Before run the tests, apply all migrations in test databse by running:

`python manage.py migrate --settings=callcalculator.settings.testing`

And run all tests:

`python manage.py test --settings=callcalculator.settings.testing`

or just run:

`make test`

### Coding style tests

This project uses flake8 checking. Install all development dependencies and run:

`flake8`

or

`make code-convention`

### Heroku

https://caioaraujo-callcalculator.herokuapp.com/