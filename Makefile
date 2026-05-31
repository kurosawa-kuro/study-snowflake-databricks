.PHONY: install snowflake-test snowflake-context snowflake-sql-file gcs-inspect databricks-job-run test lint clean

PYTHON ?= python3
VENV ?= .venv
BIN := $(VENV)/bin

install:
	$(PYTHON) -m venv $(VENV)
	$(BIN)/pip install --upgrade pip
	$(BIN)/pip install -e .

snowflake-test:
	$(BIN)/python -m src.snowflake_sql

snowflake-context:
	$(BIN)/python -m src.snowflake_sql --mode context

snowflake-sql-file:
	@test -n "$(SQL_FILE)" || (echo "Usage: make snowflake-sql-file SQL_FILE=path/to/file.sql" && exit 1)
	$(BIN)/python -m src.snowflake_sql --sql-file "$(SQL_FILE)"

gcs-inspect:
	@test -n "$(BUCKET)" || (echo "Usage: make gcs-inspect BUCKET=<bucket> OBJECT=<path> [OUTPUT=local-file]" && exit 1)
	@test -n "$(OBJECT)" || (echo "Usage: make gcs-inspect BUCKET=<bucket> OBJECT=<path> [OUTPUT=local-file]" && exit 1)
	$(BIN)/python -m src.gcs_fixture_inspector --bucket "$(BUCKET)" --object "$(OBJECT)" $(if $(OUTPUT),--output "$(OUTPUT)")

databricks-job-run:
	@test -n "$(JOB_ID)" || (echo "Usage: make databricks-job-run JOB_ID=<id> [NOTEBOOK_PARAMS='{\"key\":\"value\"}']" && exit 1)
	$(BIN)/python -m src.databricks_job_trigger --job-id "$(JOB_ID)" --notebook-params '$(or $(NOTEBOOK_PARAMS),{})'

test: lint

lint:
	$(BIN)/python -m py_compile src/*.py

clean:
	rm -rf $(VENV) build dist *.egg-info
