# Define the Poetry command
POETRY = poetry

# Define the Python command within Poetry
PYTHON = $(POETRY) run python

# Default target
all: install lint test

# Install dependencies
install:
	$(POETRY) install

# Install from Requirements.txt
requirements:
	${POETRY} run pip install -r requirements.txt 

# Run Django migrations
migrate:
	$(PYTHON) api/manage.py migrate

# Create Django superuser
createsuperuser:
	$(PYTHON) api/manage.py createsuperuser

# Run Django development server
runserver:
	$(PYTHON) api/manage.py runserver 0.0.0.0:9020

# Gunicorn Production
gunicorn:
	poetry run nohup bash api/gunicorn_run.sh > gunicorn.log 2>&1 &

gunicorn_kill:
	poetry run bash api/gunicorn_kill.sh &

# Run tests
test:
	$(PYTHON) api/manage.py test

# Lint the code
lint:
	$(PYTHON) -m flake8

format:
	$(POETRY) run black .

# Collect static files
collectstatic:
	$(PYTHON) api/manage.py collectstatic --noinput

# Clean up generated files
clean:
	rm -f *.pyc

# 

