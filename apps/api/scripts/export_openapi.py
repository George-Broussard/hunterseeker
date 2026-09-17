"""Write the API's OpenAPI document to ``packages/shared/openapi.json``.

    uv run python scripts/export_openapi.py          # write
    uv run python scripts/export_openapi.py --check  # exit 1 if the committed file is stale

The JSON is the source for ``packages/shared/src/api.d.ts`` (run
``pnpm --filter @hunterseeker/shared generate`` after this). Both files are committed
and CI verifies they match the API code.
"""

import argparse
import json
import sys
from pathlib import Path

from hunterseeker.core.app import create_app

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUT = REPO_ROOT / "packages" / "shared" / "openapi.json"


def render() -> str:
    schema = create_app().openapi()
    return json.dumps(schema, indent=2, ensure_ascii=False) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0] if __doc__ else None)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT, help="destination file")
    parser.add_argument(
        "--check", action="store_true", help="do not write; fail if the file is stale"
    )
    args = parser.parse_args(argv)
    out: Path = args.out
    rendered = render()

    if args.check:
        current = out.read_text(encoding="utf-8") if out.exists() else None
        if current != rendered:
            print(
                f"{out} is stale. Run `uv run python scripts/export_openapi.py` "
                "and `pnpm --filter @hunterseeker/shared generate`, then commit.",
                file=sys.stderr,
            )
            return 1
        print(f"{out} is up to date.")
        return 0

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(rendered, encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
