#!/usr/bin/env python3
"""Validate the public Flutter Agent Skills catalog and package metadata."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
SKILLS_DIR = ROOT / "skills"
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
MAX_DESCRIPTION = 500
MAX_COMBINED_DESCRIPTION = 12_000
EXPECTED_VERSION = "0.1.0"


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def parse_frontmatter(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing opening YAML frontmatter delimiter")
    try:
        frontmatter_text, body = text[4:].split("\n---\n", 1)
    except ValueError as error:
        raise ValueError("missing closing YAML frontmatter delimiter") from error

    metadata: dict[str, str] = {}
    for line in frontmatter_text.splitlines():
        if not line.strip() or line.startswith((" ", "\t")):
            continue
        key, separator, value = line.partition(":")
        if separator:
            metadata[key.strip()] = value.strip().strip('"').strip("'")
    return metadata, body


def local_link_errors(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    for target in LINK_PATTERN.findall(text):
        clean_target = target.split("#", 1)[0]
        if not clean_target or clean_target.startswith(("http://", "https://", "mailto:")):
            continue
        if clean_target.startswith("/"):
            errors.append(f"{path.relative_to(ROOT)} uses absolute local link: {target}")
            continue
        resolved = (path.parent / clean_target).resolve()
        if not resolved.exists():
            errors.append(f"{path.relative_to(ROOT)} has broken local link: {target}")
    return errors


def validate_skill(skill_dir: Path) -> tuple[list[str], list[str], int, int]:
    errors: list[str] = []
    warnings: list[str] = []
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        return [f"{skill_dir.name}: missing SKILL.md"], warnings, 0, 0

    try:
        metadata, body = parse_frontmatter(skill_file)
    except ValueError as error:
        return [f"{skill_dir.name}: {error}"], warnings, 0, 0

    name = metadata.get("name", "")
    description = metadata.get("description", "")
    if name != skill_dir.name:
        errors.append(f"{skill_dir.name}: frontmatter name is {name!r}")
    if not NAME_PATTERN.fullmatch(name):
        errors.append(f"{skill_dir.name}: invalid skill name")
    if not description:
        errors.append(f"{skill_dir.name}: missing description")
    elif len(description) > MAX_DESCRIPTION:
        errors.append(f"{skill_dir.name}: description exceeds {MAX_DESCRIPTION} characters")
    if not body.strip():
        errors.append(f"{skill_dir.name}: empty instructions")

    line_count = len(skill_file.read_text(encoding="utf-8").splitlines())
    if line_count > 300:
        warnings.append(f"{skill_dir.name}: SKILL.md is {line_count} lines")
    errors.extend(local_link_errors(skill_file))

    references_dir = skill_dir / "references"
    if references_dir.is_dir():
        linked = {target.split("#", 1)[0] for target in LINK_PATTERN.findall(skill_file.read_text(encoding="utf-8"))}
        for reference in references_dir.rglob("*"):
            if reference.is_file():
                relative = reference.relative_to(skill_dir).as_posix()
                if relative not in linked:
                    errors.append(f"{skill_dir.name}: unlinked reference {relative}")
                errors.extend(local_link_errors(reference))

    eval_path = skill_dir / "evals" / "cases.json"
    if not eval_path.is_file():
        errors.append(f"{skill_dir.name}: missing evals/cases.json")
        return errors, warnings, len(description), 0

    try:
        cases = load_json(eval_path)
    except (json.JSONDecodeError, OSError) as error:
        errors.append(f"{skill_dir.name}: invalid eval JSON: {error}")
        return errors, warnings, len(description), 0
    if not isinstance(cases, list) or len(cases) < 2:
        errors.append(f"{skill_dir.name}: requires at least two eval cases")
        return errors, warnings, len(description), 0

    names: set[str] = set()
    for index, case in enumerate(cases):
        label = f"{skill_dir.name} eval {index + 1}"
        if not isinstance(case, dict):
            errors.append(f"{label}: must be an object")
            continue
        case_name = case.get("name")
        if not isinstance(case_name, str) or not NAME_PATTERN.fullmatch(case_name):
            errors.append(f"{label}: invalid stable name")
        elif case_name in names:
            errors.append(f"{label}: duplicate name {case_name}")
        else:
            names.add(case_name)
        if not isinstance(case.get("prompt"), str) or not case["prompt"].strip():
            errors.append(f"{label}: missing prompt")
        expectations = case.get("expectations")
        if not isinstance(expectations, list) or not expectations or not all(isinstance(item, str) and item.strip() for item in expectations):
            errors.append(f"{label}: expectations must be non-empty strings")

    return errors, warnings, len(description), len(cases)


def normalized_skill_paths(values: list[str]) -> set[str]:
    return {value.removeprefix("./").removeprefix("skills/") for value in values}


def validate_packages(skill_names: set[str]) -> list[str]:
    errors: list[str] = []
    marketplace = load_json(ROOT / ".claude-plugin" / "marketplace.json")
    tessl = load_json(ROOT / ".tessl-plugin" / "plugin.json")
    tessl_root = load_json(ROOT / "tessl.json")

    versions = {marketplace.get("metadata", {}).get("version"), tessl.get("version")}
    versions.update(plugin.get("version") for plugin in marketplace.get("plugins", []))
    if versions != {EXPECTED_VERSION}:
        errors.append(f"package versions are not aligned at {EXPECTED_VERSION}: {sorted(str(value) for value in versions)}")

    plugins = {plugin.get("name"): plugin for plugin in marketplace.get("plugins", [])}
    all_bundle = plugins.get("all-flutter-skills")
    if not all_bundle:
        errors.append("missing all-flutter-skills Claude bundle")
    elif normalized_skill_paths(all_bundle.get("skills", [])) != skill_names:
        errors.append("all-flutter-skills membership does not match public skills")

    for plugin_name, plugin in plugins.items():
        unknown = normalized_skill_paths(plugin.get("skills", [])) - skill_names
        if unknown:
            errors.append(f"{plugin_name}: unknown skills {sorted(unknown)}")

    if normalized_skill_paths(tessl.get("skills", [])) != skill_names:
        errors.append("Tessl skill membership does not match public skills")
    if tessl.get("name") != tessl_root.get("name"):
        errors.append("Tessl package names are not aligned")
    return errors


def validate_repository() -> tuple[list[str], list[str], dict[str, int]]:
    errors: list[str] = []
    warnings: list[str] = []
    skill_dirs = sorted(path for path in SKILLS_DIR.iterdir() if path.is_dir())
    skill_names = {path.name for path in skill_dirs}
    if len(skill_names) != 18:
        errors.append(f"expected 18 public skills, found {len(skill_names)}")

    description_total = 0
    eval_total = 0
    for skill_dir in skill_dirs:
        skill_errors, skill_warnings, description_size, eval_count = validate_skill(skill_dir)
        errors.extend(skill_errors)
        warnings.extend(skill_warnings)
        description_total += description_size
        eval_total += eval_count

    if description_total > MAX_COMBINED_DESCRIPTION:
        errors.append(f"combined discovery descriptions exceed {MAX_COMBINED_DESCRIPTION} characters")

    try:
        errors.extend(validate_packages(skill_names))
    except (FileNotFoundError, json.JSONDecodeError) as error:
        errors.append(f"invalid package metadata: {error}")

    for markdown in [ROOT / "README.md", ROOT / "CONTRIBUTING.md", ROOT / "docs" / "SOURCES.md"]:
        errors.extend(local_link_errors(markdown))

    return errors, warnings, {
        "skills": len(skill_names),
        "evals": eval_total,
        "description_characters": description_total,
    }


def main() -> int:
    errors, warnings, counts = validate_repository()
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    if errors:
        print(f"Validation failed with {len(errors)} error(s).", file=sys.stderr)
        return 1
    print(
        f"Validated {counts['skills']} skills, {counts['evals']} eval cases, "
        f"and {counts['description_characters']} discovery-description characters."
    )
    if warnings:
        print(f"Validation passed with {len(warnings)} advisory warning(s).")
    else:
        print("Validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
