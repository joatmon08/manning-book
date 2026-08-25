#!/usr/bin/env bash
# Idempotent Cloud Agent bootstrap for this repository.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

TF_VERSION="$(
  python3 - <<'PY'
import re
from pathlib import Path
text = Path("README.md").read_text(encoding="utf-8")
match = re.search(r"Install Terraform\s+(\d+\.\d+\.\d+)", text)
print(match.group(1) if match else "1.15.9")
PY
)"

if ! command -v terraform >/dev/null 2>&1 || ! terraform version -json 2>/dev/null | grep -q "\"terraform_version\": \"${TF_VERSION}\""; then
  echo "Installing Terraform ${TF_VERSION}..."
  tmp="$(mktemp -d)"
  curl -fsSL "https://releases.hashicorp.com/terraform/${TF_VERSION}/terraform_${TF_VERSION}_linux_amd64.zip" -o "${tmp}/terraform.zip"
  sudo unzip -o "${tmp}/terraform.zip" -d /usr/local/bin
  sudo rm -f /usr/local/bin/LICENSE.txt
  rm -rf "${tmp}"
fi
terraform version

export PATH="${HOME}/.local/bin:${PATH}"
python3 -m pip install --user -r requirements.txt

mkdir -p "${HOME}/.terraform.d/plugin-cache"
echo "Cloud agent install complete."
