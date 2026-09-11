#!/usr/bin/env python3
"""Run repeatable deep-link or notification lifecycle scenarios on one device."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit, urlunsplit


SECRET_PATTERNS = (
    (re.compile(r"(?i)(authorization:\s*bearer\s+)\S+"), r"\1[REDACTED]"),
    (re.compile(r"(?i)(bearer\s+)\S+"), r"\1[REDACTED]"),
    (
        re.compile(r'(?i)(["\']?(?:access_?token|refresh_?token|cookie)["\']?\s*[:=]\s*)\S+'),
        r"\1[REDACTED]",
    ),
)


class MatrixError(ValueError):
    """Raised when a lifecycle matrix is invalid."""


def redact(text: str, limit: int = 4000) -> str:
    value = text[-limit:]
    for pattern, replacement in SECRET_PATTERNS:
        value = pattern.sub(replacement, value)
    return value


def safe_uri(uri: str) -> str:
    parts = urlsplit(uri)
    return urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))


def safe_command(argv: list[str]) -> list[str]:
    return [
        safe_uri(item) if "://" in item else redact(item, limit=500)
        for item in argv
    ]


def _steps(value: Any, field: str) -> list[dict[str, Any]]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise MatrixError(f"{field} must be an array")
    checked: list[dict[str, Any]] = []
    for index, step in enumerate(value):
        if not isinstance(step, dict):
            raise MatrixError(f"{field}[{index}] must be an object")
        name = step.get("name")
        argv = step.get("argv")
        if not isinstance(name, str) or not name.strip():
            raise MatrixError(f"{field}[{index}].name must be a non-empty string")
        if (
            not isinstance(argv, list)
            or not argv
            or not all(isinstance(item, str) and item for item in argv)
        ):
            raise MatrixError(f"{field}[{index}].argv must be a non-empty string array")
        checked.append({"name": name, "argv": argv})
    return checked


def validate_matrix(data: Any) -> dict[str, Any]:
    if not isinstance(data, dict):
        raise MatrixError("matrix root must be an object")
    platform = data.get("platform")
    if platform not in {"android", "ios"}:
        raise MatrixError("platform must be android or ios")
    for field in ("device_id", "app_id"):
        if not isinstance(data.get(field), str) or not data[field].strip():
            raise MatrixError(f"{field} must be a non-empty string")
    timeout = data.get("timeout_seconds", 60)
    if not isinstance(timeout, int) or not 1 <= timeout <= 600:
        raise MatrixError("timeout_seconds must be an integer from 1 to 600")
    scenarios = data.get("scenarios")
    if not isinstance(scenarios, list) or not scenarios:
        raise MatrixError("scenarios must be a non-empty array")

    names: set[str] = set()
    checked_scenarios: list[dict[str, Any]] = []
    for index, scenario in enumerate(scenarios):
        if not isinstance(scenario, dict):
            raise MatrixError(f"scenarios[{index}] must be an object")
        name = scenario.get("name")
        if not isinstance(name, str) or not name.strip():
            raise MatrixError(f"scenarios[{index}].name must be a non-empty string")
        if name in names:
            raise MatrixError(f"duplicate scenario name: {name}")
        names.add(name)
        lifecycle = scenario.get("lifecycle")
        if lifecycle not in {"cold", "warm"}:
            raise MatrixError(f"{name}.lifecycle must be cold or warm")
        has_uri = isinstance(scenario.get("uri"), str) and bool(scenario["uri"])
        has_trigger = scenario.get("trigger") is not None
        if has_uri == has_trigger:
            raise MatrixError(f"{name} must define exactly one of uri or trigger")
        trigger_count = scenario.get("trigger_count", 1)
        if not isinstance(trigger_count, int) or not 1 <= trigger_count <= 10:
            raise MatrixError(f"{name}.trigger_count must be an integer from 1 to 10")
        checked = {
            "name": name,
            "lifecycle": lifecycle,
            "trigger_count": trigger_count,
            "before": _steps(scenario.get("before"), f"{name}.before"),
            "assert": _steps(scenario.get("assert"), f"{name}.assert"),
            "after": _steps(scenario.get("after"), f"{name}.after"),
        }
        if not checked["assert"]:
            raise MatrixError(f"{name}.assert must contain at least one verification step")
        if has_uri:
            checked["uri"] = scenario["uri"]
        else:
            checked["trigger"] = _steps([scenario["trigger"]], f"{name}.trigger")[0]
        checked_scenarios.append(checked)

    return {
        "platform": platform,
        "device_id": data["device_id"],
        "app_id": data["app_id"],
        "timeout_seconds": timeout,
        "scenarios": checked_scenarios,
    }


def lifecycle_command(platform: str, device_id: str, app_id: str) -> list[str]:
    if platform == "android":
        return ["adb", "-s", device_id, "shell", "am", "force-stop", app_id]
    return ["xcrun", "simctl", "terminate", device_id, app_id]


def deep_link_command(
    platform: str, device_id: str, app_id: str, uri: str
) -> list[str]:
    if platform == "android":
        return [
            "adb",
            "-s",
            device_id,
            "shell",
            "am",
            "start",
            "-W",
            "-a",
            "android.intent.action.VIEW",
            "-d",
            uri,
            app_id,
        ]
    return ["xcrun", "simctl", "openurl", device_id, uri]


def run_step(
    name: str, argv: list[str], timeout: int, execute: bool
) -> dict[str, Any]:
    if not execute:
        return {
            "name": name,
            "status": "planned",
            "command": safe_command(argv),
            "duration_seconds": 0,
        }
    started = time.monotonic()
    try:
        completed = subprocess.run(
            argv,
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout,
            shell=False,
        )
        output = redact(
            "\n".join(
                part for part in (completed.stdout, completed.stderr) if part
            )
        )
        result: dict[str, Any] = {
            "name": name,
            "status": "passed" if completed.returncode == 0 else "failed",
            "exit_code": completed.returncode,
            "duration_seconds": round(time.monotonic() - started, 3),
        }
        if output:
            result["output_tail"] = output
        return result
    except subprocess.TimeoutExpired as error:
        output = redact(
            "\n".join(str(part or "") for part in (error.stdout, error.stderr))
        )
        result = {
            "name": name,
            "status": "timeout",
            "duration_seconds": round(time.monotonic() - started, 3),
        }
        if output:
            result["output_tail"] = output
        return result
    except OSError as error:
        return {
            "name": name,
            "status": "error",
            "error": redact(str(error)),
            "duration_seconds": round(time.monotonic() - started, 3),
        }


def normalize_lifecycle_result(
    platform: str, result: dict[str, Any]
) -> dict[str, Any]:
    if platform != "ios" or result["status"] != "failed":
        return result
    output = result.get("output_tail", "").lower()
    if "no such process" in output or "not running" in output:
        result["status"] = "passed"
        result["note"] = "app was already stopped"
    return result


def run_matrix(matrix: dict[str, Any], execute: bool) -> dict[str, Any]:
    platform = matrix["platform"]
    device_id = matrix["device_id"]
    app_id = matrix["app_id"]
    timeout = matrix["timeout_seconds"]
    scenario_results: list[dict[str, Any]] = []

    for scenario in matrix["scenarios"]:
        steps: list[dict[str, Any]] = []
        failed = False

        try:
            for step in scenario["before"]:
                result = run_step(
                    f"before: {step['name']}", step["argv"], timeout, execute
                )
                steps.append(result)
                failed = result["status"] not in {"passed", "planned"}
                if failed:
                    break

            if not failed and scenario["lifecycle"] == "cold":
                result = normalize_lifecycle_result(
                    platform,
                    run_step(
                        "prepare: terminate app",
                        lifecycle_command(platform, device_id, app_id),
                        timeout,
                        execute,
                    ),
                )
                steps.append(result)
                failed = result["status"] not in {"passed", "planned"}

            if not failed:
                if "uri" in scenario:
                    trigger_name = f"trigger: {safe_uri(scenario['uri'])}"
                    trigger_argv = deep_link_command(
                        platform, device_id, app_id, scenario["uri"]
                    )
                else:
                    trigger_name = f"trigger: {scenario['trigger']['name']}"
                    trigger_argv = scenario["trigger"]["argv"]
                for number in range(scenario["trigger_count"]):
                    suffix = (
                        f" ({number + 1}/{scenario['trigger_count']})"
                        if scenario["trigger_count"] > 1
                        else ""
                    )
                    result = run_step(
                        trigger_name + suffix, trigger_argv, timeout, execute
                    )
                    steps.append(result)
                    failed = result["status"] not in {"passed", "planned"}
                    if failed:
                        break

            if not failed:
                for step in scenario["assert"]:
                    result = run_step(
                        f"assert: {step['name']}", step["argv"], timeout, execute
                    )
                    steps.append(result)
                    failed = result["status"] not in {"passed", "planned"}
                    if failed:
                        break
        finally:
            for step in scenario["after"]:
                result = run_step(
                    f"cleanup: {step['name']}", step["argv"], timeout, execute
                )
                steps.append(result)
                if result["status"] not in {"passed", "planned"}:
                    failed = True

        scenario_results.append(
            {
                "name": scenario["name"],
                "lifecycle": scenario["lifecycle"],
                "status": (
                    "failed" if failed else ("planned" if not execute else "passed")
                ),
                "steps": steps,
            }
        )

    return {
        "schema_version": 1,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "executed": execute,
        "platform": platform,
        "device_id": device_id,
        "app_id": app_id,
        "status": (
            "failed"
            if any(item["status"] == "failed" for item in scenario_results)
            else ("planned" if not execute else "passed")
        ),
        "scenarios": scenario_results,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("matrix", type=Path, help="JSON lifecycle matrix")
    parser.add_argument(
        "--execute", action="store_true", help="run the matrix; default is a dry run"
    )
    parser.add_argument("--report", type=Path, help="write the JSON report to this path")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        matrix = validate_matrix(json.loads(args.matrix.read_text(encoding="utf-8")))
        report = run_matrix(matrix, args.execute)
    except (OSError, json.JSONDecodeError, MatrixError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    rendered = json.dumps(report, indent=2) + "\n"
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 1 if report["status"] == "failed" else 0


if __name__ == "__main__":
    raise SystemExit(main())
