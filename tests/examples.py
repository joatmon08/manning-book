from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _is_example(path: Path) -> bool:
    parts = path.relative_to(ROOT).parts
    if not parts or not parts[0].startswith("ch"):
        return False
    if any(part.startswith(".") or part == "__pycache__" for part in parts):
        return False
    if (path / ".terraform.lock.hcl").exists():
        return True
    if any(path.glob("*.tf.json")):
        return True
    main = path / "main.py"
    if not main.exists():
        return False
    source = main.read_text(encoding="utf-8")
    return "generate_json" in source or "__main__" in source


def iter_examples(chapter=None):
    roots = [ROOT / chapter] if chapter else sorted(
        path for path in ROOT.glob("ch*") if path.is_dir()
    )
    seen = set()
    for root in roots:
        if not root.is_dir():
            continue
        for path in [root, *sorted(p for p in root.rglob("*") if p.is_dir())]:
            if path in seen:
                continue
            if _is_example(path):
                seen.add(path)
                yield path


def example_id(path: Path) -> str:
    return str(path.relative_to(ROOT))
