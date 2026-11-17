"""Load the FHIR-AgentBench questions from the vendored CSV (read-only)."""

import ast
import csv
import re
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CSV_PATH = ROOT / "vendor/FHIR-AgentBench/final_dataset/questions_answers_sql_fhir.csv"


@dataclass(frozen=True)
class Question:
    question_id: str
    split: str  # train | valid | test
    question: str
    true_answer: list  # parsed; the raw string is kept in true_answer_raw
    true_answer_raw: str
    assumption: str  # "Assume the current time is ..."; empty for some questions
    patient_fhir_id: str
    template: str
    main_table_name: str
    true_fhir_ids: dict[str, list[str]]  # resource type -> ids needed to answer

    @property
    def no_answer(self) -> bool:
        # The benchmark's judge treats an empty true_fhir_ids as the answer "no answer"
        return not self.true_fhir_ids


def parse_answer(raw: str) -> list:
    try:
        return ast.literal_eval(raw)
    except (ValueError, SyntaxError):
        # 103 answers are printed numpy-style: rows split by newlines, no commas
        return ast.literal_eval(re.sub(r"\]\s*\n\s*\[", "], [", raw))


def load_questions(split: str | None = None, path: Path = CSV_PATH) -> list[Question]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    questions = [
        Question(
            question_id=r["question_id"],
            split=r["split"],
            question=r["question"],
            true_answer=parse_answer(r["true_answer"]),
            true_answer_raw=r["true_answer"],
            assumption=r["assumption"],
            patient_fhir_id=r["patient_fhir_id"],
            template=r["template"],
            main_table_name=r["main_table_name"],
            true_fhir_ids=ast.literal_eval(r["true_fhir_ids"]),
        )
        for r in rows
    ]
    return [q for q in questions if split is None or q.split == split]
