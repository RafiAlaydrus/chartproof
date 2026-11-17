"""Summarise the FHIR demo NDJSON files: line counts, resource types, reference fields.

Usage: python -m chartproof.store.inspect [data/raw/fhir]
"""

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

DEFAULT_DIR = Path("data/raw/fhir")


def find_references(node: object, path: str = ""):
    """Yield (field path, reference string) for every {"reference": "..."} in a resource."""
    if isinstance(node, dict):
        ref = node.get("reference")
        if isinstance(ref, str) and path:
            yield path, ref
        for key, value in node.items():
            if key != "reference":
                yield from find_references(value, f"{path}.{key}" if path else key)
    elif isinstance(node, list):
        for item in node:  # list indices are left out of the path
            yield from find_references(item, path)


def inspect_file(path: Path) -> dict:
    lines = 0
    types: Counter = Counter()
    refs: dict[str, Counter] = defaultdict(Counter)  # field path -> target type counts
    for line in path.open():
        if not line.strip():
            continue
        resource = json.loads(line)
        lines += 1
        types[resource.get("resourceType", "?")] += 1
        for field, ref in find_references(resource):
            refs[field][ref.split("/")[0]] += 1
    return {"file": path.name, "lines": lines, "types": types, "refs": refs}


def main() -> None:
    folder = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_DIR
    results = [inspect_file(p) for p in sorted(folder.glob("*.ndjson"))]

    totals: Counter = Counter()
    for r in results:
        totals.update(r["types"])
    print("| resourceType | Count |")
    print("|---|---|")
    for kind, n in sorted(totals.items()):
        print(f"| {kind} | {n} |")
    print(f"| **Total** | **{sum(totals.values())}** |\n")

    print("| File | Lines | resourceType |")
    print("|---|---|---|")
    for r in results:
        kinds = ", ".join(f"{t} ({n})" if len(r["types"]) > 1 else t for t, n in r["types"].items())
        print(f"| {r['file']} | {r['lines']} | {kinds} |")

    print("\n| File | Reference field | Points to |")
    print("|---|---|---|")
    for r in results:
        for field, targets in sorted(r["refs"].items()):
            print(f"| {r['file']} | {field} | {', '.join(sorted(targets))} |")

    patients = sum(r["lines"] for r in results if "Patient" in r["types"])
    print(f"\nPatients: {patients}")


if __name__ == "__main__":
    main()
