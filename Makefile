pipenv-setup:
	pipenv install

pipenv-setup-dev:
	pipenv install --dev

run-server:
	python manage.py runserver

code-convention:
	flake8