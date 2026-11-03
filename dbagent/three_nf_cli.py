"""Offline runner for students' 3NF functions; never calls an LLM.

Run: python -m dbagent.three_nf_cli --input examples/normalization_case.json
"""
import argparse
import json
from pathlib import Path
from .normalization import find_3nf_violations, decompose_to_3nf


def main(argv=None):
    parser = argparse.ArgumentParser(description="Offline 3NF extension runner")
    parser.add_argument("--input", required=True, help="JSON file containing attributes and functional_dependencies")
    parser.add_argument("--task", choices=["violations", "decompose"], default="decompose")
    args = parser.parse_args(argv)
    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    attrs = data["attributes"]
    fds = data["functional_dependencies"]
    result = (find_3nf_violations if args.task == "violations" else decompose_to_3nf)(attrs, fds)
    print(json.dumps(result, indent=2, default=lambda value: sorted(value) if isinstance(value, set) else str(value)))


if __name__ == "__main__":
    main()
