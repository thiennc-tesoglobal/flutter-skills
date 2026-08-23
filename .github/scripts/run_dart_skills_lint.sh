#!/usr/bin/env bash
set -euo pipefail

readonly LINTER_VERSION="${DART_SKILLS_LINT_VERSION:-0.4.0}"
readonly REPOSITORY="flutter/agent-plugins"

case "$(uname -s)-$(uname -m)" in
  Linux-x86_64) target="linux-x64" ;;
  Linux-aarch64|Linux-arm64) target="linux-arm64" ;;
  Darwin-x86_64) target="macos-x64" ;;
  Darwin-arm64) target="macos-arm64" ;;
  *)
    echo "Unsupported dart_skills_lint platform: $(uname -s)-$(uname -m)" >&2
    exit 2
    ;;
esac

readonly archive="dart_skills_lint-${target}.tar.gz"
readonly base_url="https://github.com/${REPOSITORY}/releases/download/dart_skills_lint-v${LINTER_VERSION}"
lint_temp_dir="$(mktemp -d "${TMPDIR:-/tmp}/flutter-skills-lint.XXXXXX")"
readonly lint_temp_dir

cleanup() {
  rm -rf -- "$lint_temp_dir"
}
trap cleanup EXIT

curl -fsSL "${base_url}/${archive}" -o "${lint_temp_dir}/${archive}"
curl -fsSL "${base_url}/SHA256SUMS" -o "${lint_temp_dir}/SHA256SUMS"

expected_checksum="$(awk -v archive="$archive" '$2 == archive || $2 == "*" archive { print $1; exit }' "${lint_temp_dir}/SHA256SUMS")"
if [[ -z "$expected_checksum" ]]; then
  echo "No checksum published for ${archive}" >&2
  exit 1
fi

if command -v sha256sum >/dev/null 2>&1; then
  actual_checksum="$(sha256sum "${lint_temp_dir}/${archive}" | awk '{print $1}')"
else
  actual_checksum="$(shasum -a 256 "${lint_temp_dir}/${archive}" | awk '{print $1}')"
fi

if [[ "$actual_checksum" != "$expected_checksum" ]]; then
  echo "Checksum mismatch for ${archive}" >&2
  exit 1
fi

tar -xzf "${lint_temp_dir}/${archive}" -C "$lint_temp_dir"
"${lint_temp_dir}/dart_skills_lint-${target}" \
  --skills-directory ./skills \
  --check-trailing-whitespace
