# Automation: monthly Terraform / provider updates

Cursor Automations are configured in the dashboard, not as committed YAML. Use this file as the checklist and prompt to paste.

## Dashboard setup

1. Open the Automations create page in Cursor.
2. **Trigger:** Scheduled — monthly, for example `0 9 1 * *` (09:00 UTC on the 1st). Optional second trigger: Webhook, if an external release watcher should wake the agent immediately.
3. **Repositories:** Single repository → `joatmon08/manning-book` on `main`. Scheduled automations default to no repo; a repo is required to open PRs.
4. **Tools:** Pull request creation (default on). Enable **Memories** so repeat runs can skip an already-open bump.
5. **Environment:** Use the repo `.cursor/environment.json` (installs pinned Terraform + Python deps via `scripts/cloud-agent-install.sh`).
6. **Permissions:** Private (PRs as you) or Team Owned (PRs as `cursor`).
7. Paste the prompt below into the automation instructions, save, and activate.

## Prompt (paste into the automation)

```text
You maintain Terraform CLI and provider versions for the Infrastructure as Code book examples in this repo.

## Goal
Once a month, check whether a newer stable Terraform CLI or chapter-used provider version is available. If yes, open ONE focused pull request that applies that upgrade. If nothing new, an open PR already covers it, or the upgrade is unsafe, make no code changes.

Terraform rarely ships major versions — treat patch and minor updates as first-class (for example 1.15.8 → 1.15.9).

## Detect
1. Run: `python3 scripts/check_terraform_updates.py` and `python3 scripts/check_terraform_updates.py --json`
2. Act on entries under `bumps` (any newer stable version: patch, minor, or major).
3. Scope is `ch*/**`, README Terraform pin, and `.github/workflows` `terraform_version`.

## Decision rules
- If `has_update` is false: stop. Do not open a PR.
- If Memories or `gh pr list` show an open PR for the same component/target version: stop.
- Prefer one PR per run. Priority: Terraform CLI, then hashicorp/google (+ google-beta together), then hashicorp/aws.
- Read the relevant HashiCorp upgrade guide / changelog. If breaking changes cannot be handled confidently in the examples, stop without edits and summarize blockers.

## Upgrade steps
1. Follow `.cursor/rules/terraform-updates.mdc`.
2. Update version pins, refresh `.terraform.lock.hcl` under `ch*/` with `terraform init -upgrade`, keep Python as source of truth and regenerate `*.tf.json` when needed.
3. Run `terraform validate` on touched examples. Run `pytest -m plan` when credentials allow; otherwise note that plan was skipped.
4. Open a PR with title `chore(terraform): bump <name> from <old> to <new>` and a body that lists current → target, bump kind, changelog links, validation performed, and residual risks.
```

## Optional: webhook from CI

After the automation is saved, copy its webhook URL and API key. A GitHub Action can run `scripts/check_terraform_updates.py` on a schedule and POST only when the exit code is `1` (update available), so the agent runs on demand instead of only on the monthly schedule.
