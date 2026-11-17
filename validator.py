"""Validate visa route YAML files against route-schema.json."""

import json
import sys
from pathlib import Path

try:
    import yaml
    import jsonschema
except ImportError:
    print("Install dependencies: pip install pyyaml jsonschema")
    sys.exit(1)


SCHEMA_PATH = Path(__file__).parent / "schema" / "route-schema.json"
ROUTES_DIR = Path(__file__).parent / "routes"


def load_schema() -> dict:
    with SCHEMA_PATH.open(encoding="utf-8") as f:
        return json.load(f)


def validate_route(path: Path, schema: dict) -> list[str]:
    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    errors = []
    validator = jsonschema.Draft202012Validator(schema)
    for err in validator.iter_errors(data):
        errors.append(f"{'.'.join(str(p) for p in err.absolute_path) or 'root'}: {err.message}")
    return errors


def main() -> int:
    schema = load_schema()
    if len(sys.argv) > 1:
        paths = [Path(p) for p in sys.argv[1:]]
    else:
        paths = sorted(ROUTES_DIR.glob("*.yaml"))

    if not paths:
        print("No route files found.")
        return 0

    failed = 0
    for path in paths:
        errors = validate_route(path, schema)
        if errors:
            print(f"FAIL {path.name}")
            for e in errors:
                print(f"  - {e}")
            failed += 1
        else:
            print(f"OK   {path.name}")

    if failed:
        print(f"\n{failed}/{len(paths)} route(s) failed validation.")
        return 1
    print(f"\nAll {len(paths)} route(s) valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
