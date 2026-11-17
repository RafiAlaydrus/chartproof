import pytest

from chartproof.eval.dataset import CSV_PATH, load_questions, parse_answer
from chartproof.eval.splits import SPLIT_DIR, build_splits, load_split

needs_benchmark = pytest.mark.skipif(
    not CSV_PATH.exists(), reason="run scripts/fetch_benchmark.sh first"
)


def test_parse_answer_handles_numpy_style_rows():
    assert parse_answer("[['a']\n ['b c']\n ['d']]") == [["a"], ["b c"], ["d"]]
    assert parse_answer("[['2133-12-31 02:00:00']]") == [["2133-12-31 02:00:00"]]
    assert parse_answer("[]") == []


@needs_benchmark
def test_all_questions_load_with_expected_split_sizes():
    questions = load_questions()
    sizes = {s: sum(q.split == s for q in questions) for s in ("train", "valid", "test")}
    assert sizes == {"train": 2098, "valid": 424, "test": 409}


@needs_benchmark
def test_splits_are_deterministic():
    assert build_splits() == build_splits()


@needs_benchmark
def test_split_sizes_and_overlap():
    splits = {name: s["question_ids"] for name, s in build_splits().items()}
    assert [len(splits[n]) for n in ("dev60", "test150", "local50")] == [60, 150, 50]
    assert all(len(ids) == len(set(ids)) for ids in splits.values())
    assert not set(splits["dev60"]) & set(splits["test150"])
    assert splits["local50"] == splits["test150"][:50]


@needs_benchmark
def test_splits_draw_from_the_right_source_and_cover_every_table():
    by_id = {q.question_id: q for q in load_questions()}
    for name, source in (("dev60", "valid"), ("test150", "test")):
        picked = [by_id[i] for i in build_splits()[name]["question_ids"]]
        assert {q.split for q in picked} == {source}
        tables_in_source = {q.main_table_name for q in load_questions(source)}
        assert {q.main_table_name for q in picked} == tables_in_source


@needs_benchmark
def test_committed_split_files_match_a_fresh_build():
    for name, split in build_splits().items():
        assert load_split(name, SPLIT_DIR) == split["question_ids"]
