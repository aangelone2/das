.PHONY: docs

test:
	poetry run python3 -m pytest
docs:
	poetry run mkdocs build
	poetry run mkdocs serve
