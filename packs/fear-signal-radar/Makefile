.PHONY: doctor test test-fast test-db

doctor:
	bash scripts/fsra_doctor.sh

test:
	bash scripts/fsra_test.sh

test-fast:
	@if [ -f .venv/bin/activate ]; then \
		source .venv/bin/activate; \
	fi; \
	python -m pytest -q tests/test_topic_config_schema.py tests/test_youtube_collector.py tests/test_loader_stubs.py tests/test_synthesize_api.py

test-db:
	@if [ -f .venv/bin/activate ]; then \
		source .venv/bin/activate; \
	fi; \
	python -m pytest -q tests/test_db_schema.py tests/test_db_permissions.py
