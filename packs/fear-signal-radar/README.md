# Fear Signal Radar Pack

## How to run tests (one command)

Run:

```bash
make doctor
```

`make doctor` validates the test environment before running tests:
- verifies you are in `packs/fear-signal-radar`
- checks Docker availability and socket wiring (`DOCKER_HOST`)
- runs DB sanity (`tests/test_db_schema.py`) to confirm testcontainers can start Postgres
- runs DB permission/auth checks and then the full suite
- prints a single final status: `FSRA TESTS: GREEN` or `FSRA TESTS: RED`

For a wrapper that also activates `.venv` if present:

```bash
make test
```
