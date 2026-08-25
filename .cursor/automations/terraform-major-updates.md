# Automation: Terraform / provider major updates

Cursor Automations are configured in the dashboard ([cursor.com/automations/new](https://cursor.com/automations/new)), not as committed YAML. Use this file as the checklist and prompt to paste.

## Dashboard setup

1. Open [Create automation](https://cursor.com/automations/new).
2. **Trigger:** Scheduled — for example weekly Monday `0 9 * * 1` (UTC). Optional second trigger: Webhook, if an external release watcher should wake the agent immediately.
3. **Repositories:** Single repository → `joatmon08/manning-book` on `main`. Scheduled automations default to no repo; a repo is required to open PRs.
4. **Tools:** Pull request creation (default on). Enable **Memories** so repeat runs can skip an already-open bump.
5. **Environment:** Use the repo `.cursor/environment.json` (installs pinned Terraform + Python deps via `scripts/cloud-agent-install.sh`).
6. **Permissions:** Private (PRs as you) or Team Owned (PRs as `cursor`).
7. Paste the prompt below into the automation instructions, save, and activate.

## Prompt (paste into the automation)

```text
You maintain Terraform and provider majors for the Infrastructure as Code book examples in this repo.

## Goal
Check whether a new major version of the Terraform CLI or a chapter-used provider is available. If yes, open ONE focused pull request that performs that major upgrade. If nothing new, an open PR already covers it, or the upgrade is unsafe, make no code changes.

## Detect
1. Run: `python3 scripts/check_terraform_majors.py` and `python3 scripts/check_terraform_majors.py --json`
2. Only act on entries under `bumps` (major line changes). Ignore minor/patch-only drift.
3. Scope is `ch*/**`, README Terraform pin, and `.github/workflows` `terraform_version`. Do not change `live/**` unless the human follow-up explicitly asks.

## Decision rules
- If `has_major_bump` is false: stop. Do not open a PR.
- If Memories or `gh pr list` show an open PR for the same component/major: stop.
- Prefer one PR per run. Priority: Terraform CLI major, then hashicorp/google (+ google-beta together), then hashicorp/aws.
- Read the relevant HashiCorp upgrade guide / changelog. If breaking changes cannot be handled confidently in the examples, stop without edits and summarize blockers.

## Upgrade steps
1. Follow `.cursor/rules/terraform-major-updates.mdc`.
2. Update version pins, refresh `.terraform.lock.hcl` under `ch*/` with `terraform init -upgrade`, keep Python as source of truth and regenerate `*.tf.json` when needed.
3. Run `terraform validate` on touched examples. Run `pytest -m plan` when credentials allow; otherwise note that plan was skipped.
4. Open a PR with title `chore(terraform): bump <name> from <old> to <new> (major)` and a body that lists current → target, changelog links, validation performed, and residual risks.
```

## Optional: webhook from CI

After the automation is saved, copy its webhook URL and API key. A GitHub Action can run `scripts/check_terraform_majors.py` on a schedule and POST only when the exit code is `1` (major available), so the agent runs on demand instead of every week.
