pipenv-setup:
	pipenv install

pipenv-setup-dev:
	pipenv install --dev

run-server:
	python manage.py migrate --settings=callcalculator.settings.development
	python manage.py runserver

code-convention:
	flake8

collect-static:
	python manage.py collectstatic

migrations:
	python manage.py makemigrations

test:
	python manage.py migrate --settings=callcalculator.settings.testing
	python manage.py test --settings=callcalculator.settings.testing
