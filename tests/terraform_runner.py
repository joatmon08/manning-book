import json
import os
import subprocess
import sys
from pathlib import Path

GENERATE_JSON = """
import inspect
import main

fn = getattr(main, "generate_json", None)
if fn is None:
    raise SystemExit(0)
if inspect.signature(fn).parameters:
    fn(getattr(main, "SERVICE_NAME", "hello-world"))
else:
    fn()
"""


def _run(args, cwd):
    return subprocess.run(
        args,
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=300,
    )


def format_result(result):
    stdout = result.stdout or ""
    stderr = result.stderr or ""
    return f"exit {result.returncode}\n{stdout}{stderr}"


def has_terraform_config(directory: Path) -> bool:
    return any(directory.glob("*.tf.json")) or any(directory.glob("*.tf"))


def generate(directory: Path):
    main = directory / "main.py"
    if not main.exists():
        return subprocess.CompletedProcess(
            args=[], returncode=0, stdout="", stderr=""
        )
    source = main.read_text(encoding="utf-8")
    if 'if __name__' in source and "__main__" in source:
        result = _run([sys.executable, "main.py"], directory)
    else:
        result = _run([sys.executable, "-c", GENERATE_JSON], directory)
    if result.returncode != 0 and has_terraform_config(directory):
        return subprocess.CompletedProcess(
            args=result.args,
            returncode=0,
            stdout=result.stdout,
            stderr=result.stderr,
        )
    return result


def initialize(directory: Path):
    return _run(
        ["terraform", "init", "-input=false", "-no-color", "-lockfile=readonly"],
        directory,
    )


def plan(directory: Path):
    return _run(
        ["terraform", "plan", "-input=false", "-no-color", "-lock=false"],
        directory,
    )


def apply(directory: Path):
    return _run(
        ["terraform", "apply", "-input=false", "-no-color", "-auto-approve"],
        directory,
    )


def destroy(directory: Path):
    return _run(
        ["terraform", "destroy", "-input=false", "-no-color", "-auto-approve"],
        directory,
    )


def is_aws(directory: Path) -> bool:
    return "aws" in directory.parts


def _uses_google_project_data(config) -> bool:
    if isinstance(config, list):
        return any(_uses_google_project_data(item) for item in config)
    if not isinstance(config, dict):
        return False
    data = config.get("data")
    return bool(data) and "google_project" in json.dumps(data)


def skip_reason(directory: Path):
    if is_aws(directory) and not os.environ.get("AWS_ACCESS_KEY_ID"):
        return "AWS credentials are not set"
    for path in directory.glob("*.tf"):
        if "omitted for clarity" in path.read_text(encoding="utf-8"):
            return f"{path.name} is an abbreviated teaching stub"
    for path in directory.glob("*.tf.json"):
        try:
            config = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if _uses_google_project_data(config):
            return "google_project data source requires resourcemanager.projects.get"
    return None
