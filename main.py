"""Run the offline Creo CAD metadata diagnostic sample.

From the repository root: python main.py
"""

import argparse
import json
from pathlib import Path

from src.diagnose import diagnose, load_models

PROJECT_ROOT = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()


def main(argv=None):
    parser = argparse.ArgumentParser(description="Validate a synthetic CAD metadata CSV export.")
    parser.add_argument(
        "--input", type=Path, default=PROJECT_ROOT / "data" / "cad_models.csv",
        help="Path to a CAD metadata CSV (default: bundled sample).",
    )
    parser.add_argument(
        "--output", type=Path, default=PROJECT_ROOT / "reports" / "cad_diagnostics.json",
        help="Where to save the JSON findings report.",
    )
    args = parser.parse_args(argv)

    try:
        findings = diagnose(load_models(args.input))
        report = {"findings": findings, "count": len(findings)}
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    except (OSError, ValueError) as exc:
        parser.exit(1, f"CAD diagnostic error: {exc}\n")

    print(f"Analyzed: {args.input}")
    print(f"Found {len(findings)} issue(s):")
    if not findings:
        print("  No configuration issues found in supplied export.")
    for finding in findings:
        print(
            f"  [{finding['severity']}] {finding['model_id']}: "
            f"{finding['code']} ({finding['details']})"
        )
    print(f"Saved report: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
