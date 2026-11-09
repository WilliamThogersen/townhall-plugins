import json
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
MARKETPLACE = ".townhall-plugin/marketplace.json"
MANIFEST = ".townhall-plugin/plugin.json"

errors = []


def fail(message):
    errors.append(message)


def load(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        fail(f"{path.relative_to(ROOT)}: {e}")
        return None


def safe_inside(base, value, what):
    if not isinstance(value, str) or not value:
        fail(f"{what}: path must be a non-empty string")
        return None
    if value.startswith("/") or "\\" in value or value[1:2] == ":":
        fail(f"{what}: `{value}` must be relative")
        return None
    if ".." in value.split("/"):
        fail(f"{what}: `{value}` must not contain `..`")
        return None
    target = (base / value).resolve()
    if base != target and base not in target.parents:
        fail(f"{what}: `{value}` leaves {base.name}")
        return None
    if not target.exists():
        fail(f"{what}: `{value}` does not exist")
        return None
    return target


def manifest_paths(manifest):
    contributes = manifest.get("contributes", {})
    yield from contributes.get("agentTypes", [])
    yield from contributes.get("prompts", {}).values()
    for key in ("settings", "theme", "hooks"):
        if key in contributes:
            yield contributes[key]
    for ui in contributes.get("ui", []):
        yield ui.get("entry")
    yield from manifest.get("claude", {}).values()


def check_plugin(folder, name):
    manifest_file = folder / MANIFEST
    if not manifest_file.is_file():
        fail(f"{name}: {MANIFEST} is missing")
        return
    manifest = load(manifest_file)
    if not isinstance(manifest, dict):
        return
    if manifest.get("name") != name:
        fail(f"{name}: manifest name is `{manifest.get('name')}`")
    for path in manifest_paths(manifest):
        safe_inside(folder, path, f"{name}")


def main():
    for path in sorted(ROOT.rglob("*.json")):
        if ".git" not in path.relative_to(ROOT).parts:
            load(path)

    market_file = ROOT / MARKETPLACE
    if not market_file.is_file():
        fail(f"{MARKETPLACE} is missing")
    else:
        market = load(market_file)
        for entry in (market or {}).get("plugins", []):
            name = entry.get("name", "?")
            source = entry.get("source")
            if not isinstance(source, str):
                continue
            if not source.startswith("./"):
                fail(f"{name}: source `{source}` must start with ./")
                continue
            folder = safe_inside(ROOT, source[2:], f"{name} source")
            if folder is None:
                continue
            if not folder.is_dir():
                fail(f"{name} source: `{source}` is not a folder")
                continue
            check_plugin(folder, name)

    for message in errors:
        print(f"error: {message}")
    if errors:
        sys.exit(1)
    print("ok")


main()
