#!/usr/bin/env python3
"""Validate or execute a reproducible forward-evaluation matrix."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVALS_DIR = ROOT / ".github" / "evals"
RUNNER = ROOT / ".github" / "scripts" / "run_behavior_evals.py"
DEFAULT_MATRIX = EVALS_DIR / "codex-matrix.json"
CROSS_AGENT_MATRIX = EVALS_DIR / "cross-agent-matrix.json"
SUPPORTED_AGENTS = {"codex", "claude"}
ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class MatrixError(RuntimeError):
    """Raised when a matrix is unsafe or inconsistent."""


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def resolve_profile(value: str) -> Path:
    path = (EVALS_DIR / value).resolve()
    if not path.is_relative_to(EVALS_DIR.resolve()) or not path.is_file():
        raise MatrixError(f"profile must resolve inside {EVALS_DIR}: {value}")
    return path


def validate_matrix(matrix: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not isinstance(matrix.get("name"), str) or not matrix["name"].strip():
        errors.append("matrix requires a name")
    runs = matrix.get("runs")
    if not isinstance(runs, list) or not runs:
        return [*errors, "matrix requires at least one run"]
    seen: set[str] = set()
    for index, run in enumerate(runs):
        if not isinstance(run, dict):
            errors.append(f"run {index + 1} must be an object")
            continue
        identity = run.get("id")
        if not isinstance(identity, str) or not ID_PATTERN.fullmatch(identity):
            errors.append(f"run {index + 1} has an invalid id")
        elif identity in seen:
            errors.append(f"matrix repeats run id {identity}")
        else:
            seen.add(identity)
        if run.get("agent") not in SUPPORTED_AGENTS:
            errors.append(f"run {identity}: unsupported solver {run.get('agent')}")
        judges = run.get("judges")
        if (
            not isinstance(judges, list)
            or not judges
            or not all(judge in SUPPORTED_AGENTS for judge in judges)
        ):
            errors.append(f"run {identity}: requires at least one supported judge")
        elif len(set(judges)) != len(judges):
            errors.append(f"run {identity}: judges must be distinct")
        require_independent = run.get("require_independent_judge", False)
        if not isinstance(require_independent, bool):
            errors.append(f"run {identity}: require_independent_judge must be boolean")
        elif (
            require_independent
            and isinstance(judges, list)
            and judges
            and judges[0] == run.get("agent")
        ):
            errors.append(f"run {identity}: primary judge must differ from solver")
        try:
            resolve_profile(str(run.get("profile", "")))
        except MatrixError as error:
            errors.append(f"run {identity}: {error}")
    return errors


def command_for_run(
    run: dict[str, Any],
    output_dir: Path,
    agent_timeout: float,
    profile_override: str | None = None,
) -> list[str]:
    command = [
        sys.executable,
        str(RUNNER),
        "--execute",
        "--agent",
        run["agent"],
        "--agent-timeout",
        str(agent_timeout),
        "--profile",
        str(resolve_profile(profile_override or run["profile"])),
        "--output",
        str(output_dir / f"{run['id']}.json"),
        "--markdown-output",
        str(output_dir / f"{run['id']}.md"),
    ]
    for judge in run["judges"]:
        command.extend(["--judge-agent", judge])
    if run.get("require_independent_judge", False):
        command.append("--require-independent-judge")
    if run.get("skip_baseline", False):
        command.append("--skip-baseline")
    return command


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--matrix", type=Path, default=DEFAULT_MATRIX)
    parser.add_argument("--run", action="append", dest="run_ids")
    parser.add_argument(
        "--profile",
        help="profile path relative to .github/evals; overrides every selected run",
    )
    parser.add_argument("--output-dir", type=Path, default=ROOT / "benchmarks" / "matrix")
    parser.add_argument("--agent-timeout", type=float, default=180)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not 0 < args.agent_timeout <= 1800:
        raise MatrixError("agent timeout must be greater than 0 and at most 1800 seconds")
    if args.profile:
        resolve_profile(args.profile)
    matrix = load_json(args.matrix)
    errors = validate_matrix(matrix)
    if errors:
        raise MatrixError("; ".join(errors))
    selected = [
        run
        for run in matrix["runs"]
        if not args.run_ids or run["id"] in set(args.run_ids)
    ]
    unknown = set(args.run_ids or []) - {run["id"] for run in matrix["runs"]}
    if unknown:
        raise MatrixError(f"unknown matrix run ids: {sorted(unknown)}")
    print(f"Validated {len(matrix['runs'])} matrix runs; selected {len(selected)}.")
    if not args.execute:
        print("Validation-only mode; pass --execute to invoke external agents.")
        return 0

    args.output_dir.mkdir(parents=True, exist_ok=True)
    failures: list[str] = []
    for run in selected:
        completed = subprocess.run(
            command_for_run(run, args.output_dir, args.agent_timeout, args.profile),
            cwd=ROOT,
            check=False,
        )
        if completed.returncode:
            failures.append(run["id"])
    if failures:
        print(f"Failed matrix runs: {', '.join(failures)}")
        return 1
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except MatrixError as error:
        print(f"ERROR: {error}")
        raise SystemExit(2)
