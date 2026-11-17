"""Build and freeze the evaluation splits (section 4 of the plan). Only question IDs are saved.

Usage: python -m chartproof.eval.splits
"""

import json
import random
from collections import defaultdict
from pathlib import Path

from chartproof.eval.dataset import ROOT, Question, load_questions

SEED = 42
SPLIT_DIR = ROOT / "results/splits"


def allocate(counts: dict[str, int], k: int) -> dict[str, int]:
    """Split k picks across tables in proportion to size, at least one per table."""
    total = sum(counts.values())
    alloc = {t: max(1, int(c * k / total)) for t, c in counts.items()}
    by_remainder = sorted(counts, key=lambda t: counts[t] * k / total - alloc[t], reverse=True)
    i = 0
    while sum(alloc.values()) < k:
        t = by_remainder[i % len(by_remainder)]
        if alloc[t] < counts[t]:
            alloc[t] += 1
        i += 1
    while sum(alloc.values()) > k:
        alloc[max(alloc, key=alloc.get)] -= 1
    return alloc


def stratified_sample(questions: list[Question], k: int, seed: int = SEED) -> list[str]:
    """Pick k question IDs stratified by main_table_name, returned in a shuffled order."""
    by_table: dict[str, list[str]] = defaultdict(list)
    for q in questions:
        by_table[q.main_table_name].append(q.question_id)
    alloc = allocate({t: len(ids) for t, ids in by_table.items()}, k)
    rng = random.Random(seed)
    picked: list[str] = []
    for table in sorted(by_table):
        picked += rng.sample(sorted(by_table[table]), alloc[table])
    rng.shuffle(picked)
    return picked


def build_splits() -> dict[str, dict]:
    dev60 = stratified_sample(load_questions("valid"), 60)
    test150 = stratified_sample(load_questions("test"), 150)
    # test150 is already shuffled, so local50 and "the first 60" are just prefixes
    return {
        "dev60": {"source_split": "valid", "seed": SEED, "question_ids": dev60},
        "test150": {"source_split": "test", "seed": SEED, "question_ids": test150},
        "local50": {"source_split": "test", "seed": SEED, "question_ids": test150[:50]},
    }


def load_split(name: str, folder: Path = SPLIT_DIR) -> list[str]:
    return json.loads((folder / f"{name}.json").read_text())["question_ids"]


def main() -> None:
    SPLIT_DIR.mkdir(parents=True, exist_ok=True)
    for name, split in build_splits().items():
        (SPLIT_DIR / f"{name}.json").write_text(json.dumps(split, indent=2) + "\n")
        print(f"{name}: {len(split['question_ids'])} ids")


if __name__ == "__main__":
    main()
