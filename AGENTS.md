# AGENTS.md

## Cursor Cloud specific instructions

This repo holds the code examples for the Manning book *Infrastructure as Code, Patterns & Practices*. Each `chNN/sNN` directory is a standalone example: a Python `main.py` writes a Terraform JSON config (`*.tf.json`), which Terraform then `init`/`validate`/`plan`/`apply`s.

### Interpreter and tooling
- The repo pins Python 3.9 (`.python-version` = 3.9.6). The system default `python3` is 3.12, on which the pinned 2021-era requirements (e.g. `grpcio==1.39.0`) fail to build. Use the pre-built virtualenv at `.venv/` (Python 3.9), which the startup update script keeps in sync with `requirements.txt`.
- Run tools via the venv, e.g. `.venv/bin/python`, `.venv/bin/pytest`, `.venv/bin/autopep8` (or `source .venv/bin/activate`). There is no bare `python` on PATH; use `python3` / the venv.
- `terraform` (v1.x) is installed on PATH. `requirements.txt` at the repo root is the single dependency list shared by all examples.

### Running an example (core workflow)
- `cd chNN/sNN && ../../.venv/bin/python main.py` generates `main.tf.json` (some examples write other `*.tf.json` names). Then `terraform init` and `terraform validate` work fully offline.
- `terraform plan`/`apply` require real cloud credentials and are expected to fail without them: GCP examples need Application Default Credentials / `CLOUDSDK_CORE_PROJECT` (see README "Run"); AWS examples (under `aws/` subdirs) need `AWS_ACCESS_KEY_ID`/`AWS_SECRET_ACCESS_KEY`/`AWS_DEFAULT_REGION`. No cloud credentials are provisioned in this environment, so end-to-end `apply` cannot be exercised here.

### Lint and test
- Lint (matches CI, `.github/workflows/pipeline.yml`): `cd ch07/s01 && ../../.venv/bin/autopep8 -r -d --exit-code .` (exit 0 = clean).
- Unit tests: `cd ch07/s01 && ../../.venv/bin/pytest -m unit`. Test markers (`unit`, `integration`) are defined in `ch07/s01/pytest.ini`; only `ch07/s01` has a `pytest.ini`. Integration/e2e tests in other chapters hit real cloud APIs and need credentials.
- Helper scripts in `scripts/` (`lint_all.sh`, `plan_all.sh`, `upgrade_all.sh`) iterate every example and assume `terraform` + a working Python on PATH; `plan_all`/`upgrade_all` touch the cloud and need credentials.

### Gotchas
- Some examples are intentionally abbreviated (per the README) and will not `plan`/`apply` cleanly even with credentials.
- Generated `*.tf.json` and `.terraform/` dirs are created in-place inside example folders; note that a few `*.tf.json` and `.terraform.lock.hcl` files are committed. Prefer copying an example to a temp dir before running Terraform if you want to avoid dirtying tracked files. `.venv/`, `.terraform/`, and `*.tfstate` are gitignored.
