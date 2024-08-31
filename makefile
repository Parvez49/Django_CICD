# Define the Poetry command
POETRY = poetry

# Define the Python command within Poetry
PYTHON = $(POETRY) run python

# Default target
all: install lint test

# Install dependencies
install:
	$(POETRY) install

# Run Django migrations
migrate:
	$(PYTHON) backend/manage.py migrate

# Create Django superuser
createsuperuser:
	$(PYTHON) backend/manage.py createsuperuser

# Run Django development server
runserver:
	$(PYTHON) backend/manage.py runserver 0.0.0.0:9020

# Run tests
test:
	$(PYTHON) backend/manage.py test

# Lint the code
lint:
	$(PYTHON) -m flake8

# Collect static files
collectstatic:
	$(PYTHON) backend/manage.py collectstatic --noinput

# Clean up generated files
clean:
	rm -f *.pyc
