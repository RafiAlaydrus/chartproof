"""Load every FHIR NDJSON resource into one local SQLite database.

Usage: python -m chartproof.store.build
"""

import json
import sqlite3
import time
from collections import Counter
from pathlib import Path

from chartproof.store.inspect import find_references

ROOT = Path(__file__).resolve().parents[3]
RAW_DIR = ROOT / "data/raw/fhir"
DB_PATH = ROOT / "data/fhir.sqlite"

# First match wins. The first five are from the plan; the rest cover types the plan's
# fields miss (Procedure, Specimen, MedicationDispense, MedicationStatement).
TIME_FIELDS = [
    "effectiveDateTime",
    "issued",
    "authoredOn",
    "period.start",
    "effectivePeriod.start",
    "performedDateTime",
    "performedPeriod.start",
    "collection.collectedDateTime",
    "whenHandedOver",
    "dateAsserted",
]

SCHEMA = """
CREATE TABLE resources (
    id TEXT, type TEXT, patient_id TEXT, encounter_id TEXT,
    effective_time TEXT, effective_field TEXT, json TEXT,
    PRIMARY KEY (type, id)
);
CREATE TABLE refs (src_type TEXT, src_id TEXT, field TEXT, dst_type TEXT, dst_id TEXT);
"""

INDEXES = """
CREATE INDEX idx_resources_patient ON resources (type, patient_id);
CREATE INDEX idx_resources_encounter ON resources (encounter_id);
CREATE INDEX idx_resources_time ON resources (effective_time);
CREATE INDEX idx_refs_src ON refs (src_type, src_id);
CREATE INDEX idx_refs_dst ON refs (dst_type, dst_id);
"""


def dig(resource: dict, dotted: str):
    node = resource
    for key in dotted.split("."):
        node = node.get(key) if isinstance(node, dict) else None
    return node


def ref_id(resource: dict, *fields: str, want: str) -> str | None:
    """Id from the first of `fields` that holds a reference to a `want/<id>` resource."""
    for field in fields:
        ref = (resource.get(field) or {}).get("reference", "")
        if ref.startswith(want + "/"):
            return ref.split("/")[1]
    return None


def effective_time(resource: dict) -> tuple[str | None, str | None]:
    for field in TIME_FIELDS:
        value = dig(resource, field)
        if isinstance(value, str) and value:
            return value, field
    return None, None


def to_rows(resource: dict, line: str) -> tuple[tuple, list[tuple]]:
    rtype, rid = resource["resourceType"], resource["id"]
    # A Patient is its own patient, so patient searches work on every type
    patient = rid if rtype == "Patient" else ref_id(resource, "subject", "patient", want="Patient")
    encounter = ref_id(resource, "encounter", "context", want="Encounter")
    when, field = effective_time(resource)
    row = (rid, rtype, patient, encounter, when, field, line)
    refs = []
    for path, ref in find_references(resource):
        parts = ref.split("/")
        if len(parts) >= 2:
            refs.append((rtype, rid, path, parts[0], parts[1]))
    return row, refs


def build(db_path: Path = DB_PATH, raw_dir: Path = RAW_DIR) -> None:
    start = time.time()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    db_path.unlink(missing_ok=True)
    db = sqlite3.connect(db_path)
    db.executescript("PRAGMA journal_mode = OFF; PRAGMA synchronous = OFF;" + SCHEMA)

    def flush(resource_rows: list, ref_rows: list) -> None:
        db.executemany("INSERT INTO resources VALUES (?,?,?,?,?,?,?)", resource_rows)
        db.executemany("INSERT INTO refs VALUES (?,?,?,?,?)", ref_rows)
        counts.update(r[1] for r in resource_rows)
        resource_rows.clear()
        ref_rows.clear()

    counts: Counter = Counter()
    for path in sorted(raw_dir.glob("*.ndjson")):
        resource_rows, ref_rows = [], []
        for line in path.open():
            line = line.strip()
            if not line:
                continue
            row, refs = to_rows(json.loads(line), line)
            resource_rows.append(row)
            ref_rows += refs
            if len(resource_rows) >= 50_000:  # keep memory small on an 8GB laptop
                flush(resource_rows, ref_rows)
        flush(resource_rows, ref_rows)
        print(path.name)

    db.executescript(INDEXES)  # indexes after the bulk load are much faster
    db.commit()
    db.close()
    print(f"\n{sum(counts.values())} resources in {time.time() - start:.0f}s -> {db_path}")
    for rtype, n in sorted(counts.items()):
        print(f"  {rtype}: {n}")


if __name__ == "__main__":
    build()
