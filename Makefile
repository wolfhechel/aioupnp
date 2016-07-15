SETUP_PY := python setup.py

all:
	$(SETUP_PY) build

install:
	$(SETUP_PY) install

docs:
	$(SETUP_PY) build_sphinx

test:
	py.test tests --cov=tests

.PHONY: docs test install all