#!/usr/bin/env python3
"""Prove the responsive-layout verifier rejects seeded defects and accepts a fix."""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EXECUTABLE = ROOT / ".github" / "evals" / "executable"
FIXTURE = EXECUTABLE / "fixtures" / "responsive-checkout"
ORACLE = EXECUTABLE / "oracles" / "responsive-checkout" / "checkout_screen.dart"


def check(workspace: Path, command: list[str], *, fails_with: str | None = None) -> None:
    result = subprocess.run(
        command,
        cwd=workspace,
        text=True,
        capture_output=True,
        timeout=180,
        check=False,
    )
    output = result.stdout + result.stderr
    if fails_with is None and result.returncode != 0:
        raise AssertionError(f"{' '.join(command)} failed:\n{output[-6000:]}")
    if fails_with is not None and (
        result.returncode == 0 or fails_with not in output
    ):
        raise AssertionError(
            f"{' '.join(command)} did not catch {fails_with!r}:\n{output[-6000:]}"
        )


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="responsive-fixture-proof-") as directory:
        workspace = Path(directory) / "checkout"
        shutil.copytree(FIXTURE, workspace)
        source = workspace / "lib" / "checkout_screen.dart"

        check(workspace, ["flutter", "analyze"])
        check(
            workspace,
            ["flutter", "test", "--reporter=expanded"],
            fails_with="Independent controls must not intersect",
        )
        print("Seeded control overlap: caught")
        check(
            workspace,
            ["flutter", "test", "--reporter=expanded", "--plain-name", "at breakpoint"],
            fails_with="The controls switch composition at 600 logical pixels",
        )
        print("Missing wide composition at breakpoint: caught")

        shutil.copy2(ORACLE, source)
        check(workspace, ["dart", "format", "--output=none", "--set-exit-if-changed", "lib", "test"])
        check(workspace, ["flutter", "analyze"])
        check(workspace, ["flutter", "test", "--reporter=expanded"])
        print("Corrected layout and intentional badge overlay: 6 scenarios passed")

        corrected = source.read_text(encoding="utf-8")
        clipped = corrected.replace(
            "const Text(errorMessage),",
            "SizedBox(height: 18, child: Text(errorMessage, maxLines: 1)),",
        )
        if clipped == corrected:
            raise AssertionError("Error-text mutation no longer matches the oracle")
        source.write_text(clipped, encoding="utf-8")
        check(
            workspace,
            ["flutter", "test", "--reporter=expanded", "--plain-name", "compact long RTL enlarged error with keyboard"],
            fails_with="The validation message must not be ellipsized",
        )
        print("Seeded validation-message clipping: caught")

        covered = corrected.replace(
            "padding: const EdgeInsets.fromLTRB(16, 16, 16, 112)",
            "padding: const EdgeInsets.all(16)",
        )
        if covered == corrected:
            raise AssertionError("Sticky-action mutation no longer matches the oracle")
        source.write_text(covered, encoding="utf-8")
        check(
            workspace,
            ["flutter", "test", "--reporter=expanded", "--plain-name", "wide"],
            fails_with="The final field must scroll above the sticky action",
        )
        print("Seeded sticky-action obstruction: caught")

        offscreen = corrected.replace(
            "bottom: 0,\n              child: ColoredBox(",
            "bottom: -120,\n              child: ColoredBox(",
        )
        if offscreen == corrected:
            raise AssertionError("Offscreen-action mutation no longer matches the oracle")
        source.write_text(offscreen, encoding="utf-8")
        check(
            workspace,
            ["flutter", "test", "--reporter=expanded", "--plain-name", "wide"],
            fails_with="The action must stay above the simulated keyboard",
        )
        print("Seeded offscreen action: caught")


if __name__ == "__main__":
    main()
