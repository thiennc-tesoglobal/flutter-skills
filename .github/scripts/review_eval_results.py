#!/usr/bin/env python3
"""Create and summarize reproducible human-review samples for eval results."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
from pathlib import Path
from typing import Any


class ReviewError(RuntimeError):
    """Raised when a review template does not match its source result."""


def read_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def text_sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def create_review_template(
    result_path: Path,
    rate: float,
    seed: int,
) -> dict[str, Any]:
    if not 0 < rate <= 1:
        raise ReviewError("sample rate must be greater than 0 and at most 1")
    result = read_json(result_path)
    behavior = result.get("behavior")
    if not isinstance(behavior, list) or not behavior:
        raise ReviewError("result has no behavior cases to review")

    count = min(len(behavior), max(1, math.ceil(len(behavior) * rate)))
    selected = random.Random(seed).sample(behavior, count)
    cases: list[dict[str, Any]] = []
    for item in selected:
        block = item.get("with_skill", {})
        response = block.get("response")
        primary = block.get("judgment")
        if not isinstance(response, str) or not isinstance(primary, dict):
            raise ReviewError(
                f"invalid behavior result {item.get('skill')}:{item.get('case')}"
            )
        expectations = primary.get("expectations")
        if not isinstance(expectations, list):
            raise ReviewError("behavior judgment has no expectations")
        cases.append(
            {
                "skill": item["skill"],
                "case": item["case"],
                "response_sha256": text_sha256(response),
                "expectations": [
                    {
                        "criterion": expectation["criterion"],
                        "human_met": None,
                        "notes": "",
                    }
                    for expectation in expectations
                ],
            }
        )

    return {
        "schema_version": 1,
        "source": str(result_path),
        "source_sha256": file_sha256(result_path),
        "sample_rate": rate,
        "seed": seed,
        "reviewer": None,
        "reviewed_at": None,
        "cases": cases,
    }


def summarize_review(
    result_path: Path,
    review_path: Path,
) -> dict[str, Any]:
    result = read_json(result_path)
    review = read_json(review_path)
    if review.get("source_sha256") != file_sha256(result_path):
        raise ReviewError("review source hash does not match the eval result")
    if not review.get("reviewer") or not review.get("reviewed_at"):
        raise ReviewError("reviewer and reviewed_at are required before summarizing")

    by_identity = {
        (item["skill"], item["case"]): item for item in result.get("behavior", [])
    }
    judge_totals: list[dict[str, int]] = []
    reviewed_expectations = 0
    for review_case in review.get("cases", []):
        identity = (review_case.get("skill"), review_case.get("case"))
        item = by_identity.get(identity)
        if item is None:
            raise ReviewError(f"review has unknown behavior case {identity}")
        block = item["with_skill"]
        if review_case.get("response_sha256") != text_sha256(block["response"]):
            raise ReviewError(f"response hash mismatch for {identity[0]}:{identity[1]}")
        judgments = block.get("judgments") or [block["judgment"]]
        while len(judge_totals) < len(judgments):
            judge_totals.append({"agreed": 0, "total": 0})
        human_expectations = review_case.get("expectations", [])
        if len(human_expectations) != len(judgments[0]["expectations"]):
            raise ReviewError(f"expectation count mismatch for {identity[0]}:{identity[1]}")
        for index, human in enumerate(human_expectations):
            decision = human.get("human_met")
            if not isinstance(decision, bool):
                raise ReviewError(
                    f"human_met must be boolean for {identity[0]}:{identity[1]} "
                    f"expectation {index + 1}"
                )
            reviewed_expectations += 1
            for judge_index, judgment in enumerate(judgments):
                judge_totals[judge_index]["total"] += 1
                if judgment["expectations"][index]["met"] == decision:
                    judge_totals[judge_index]["agreed"] += 1

    return {
        "reviewed_cases": len(review.get("cases", [])),
        "reviewed_expectations": reviewed_expectations,
        "reviewer": review["reviewer"],
        "reviewed_at": review["reviewed_at"],
        "judge_human_agreement": [
            {
                "judge_index": index + 1,
                "agreed": totals["agreed"],
                "total": totals["total"],
                "agreement_rate": round(
                    totals["agreed"] / totals["total"] * 100, 2
                )
                if totals["total"]
                else None,
            }
            for index, totals in enumerate(judge_totals)
        ],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    sample = subparsers.add_parser("sample")
    sample.add_argument("result", type=Path)
    sample.add_argument("--output", type=Path, required=True)
    sample.add_argument("--rate", type=float, default=0.15)
    sample.add_argument("--seed", type=int, default=0)

    summarize = subparsers.add_parser("summarize")
    summarize.add_argument("result", type=Path)
    summarize.add_argument("review", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.command == "sample":
        template = create_review_template(args.result, args.rate, args.seed)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(template, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote {len(template['cases'])} review cases to {args.output}")
        return 0
    print(json.dumps(summarize_review(args.result, args.review), indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ReviewError as error:
        print(f"ERROR: {error}")
        raise SystemExit(2)
