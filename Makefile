PY = .venv/bin/python

.PHONY: setup test lint

setup:
	uv venv --python 3.11 .venv
	uv pip install --python $(PY) -e .

# pytest exits 5 when it finds no tests; that is fine early on
test:
	$(PY) -m pytest || [ $$? -eq 5 ]

lint:
	$(PY) -m ruff check .
	$(PY) -m ruff format --check .
