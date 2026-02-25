#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ISSUE_DIR="${ROOT_DIR}/packs/fear-signal-radar/issues"
REPO="${1:-}"

if ! command -v gh >/dev/null 2>&1; then
  echo "error: gh CLI is required but not installed." >&2
  exit 1
fi

if ! gh auth status >/dev/null 2>&1; then
  echo "error: gh is not authenticated. Run: gh auth login" >&2
  exit 1
fi

if [[ ! -d "${ISSUE_DIR}" ]]; then
  echo "error: issue directory not found: ${ISSUE_DIR}" >&2
  exit 1
fi

shopt -s nullglob
issue_files=("${ISSUE_DIR}"/FSRA-*.md)

if [[ ${#issue_files[@]} -eq 0 ]]; then
  echo "error: no FSRA issue files found in ${ISSUE_DIR}" >&2
  exit 1
fi

trim() {
  local value="$1"
  value="${value#"${value%%[![:space:]]*}"}"
  value="${value%"${value##*[![:space:]]}"}"
  printf '%s' "$value"
}

for issue_file in "${issue_files[@]}"; do
  title="$(sed -n 's/^Title:[[:space:]]*//p' "${issue_file}" | head -n1)"
  labels_raw="$(sed -n 's/^Labels:[[:space:]]*//p' "${issue_file}" | head -n1)"

  if [[ -z "${title}" ]]; then
    echo "warning: skipping ${issue_file} (missing Title)" >&2
    continue
  fi

  labels_csv=""
  IFS=',' read -r -a labels_arr <<< "${labels_raw}"
  for label in "${labels_arr[@]}"; do
    cleaned="$(trim "${label}")"
    if [[ -n "${cleaned}" ]]; then
      if [[ -z "${labels_csv}" ]]; then
        labels_csv="${cleaned}"
      else
        labels_csv="${labels_csv},${cleaned}"
      fi
    fi
  done

  body_file="$(mktemp)"
  awk '!/^Title:[[:space:]]/ && !/^Labels:[[:space:]]/' "${issue_file}" > "${body_file}"

  cmd=(gh issue create --title "${title}" --body-file "${body_file}")
  if [[ -n "${labels_csv}" ]]; then
    cmd+=(--label "${labels_csv}")
  fi
  if [[ -n "${REPO}" ]]; then
    cmd+=(--repo "${REPO}")
  fi

  echo "creating: ${title}"
  "${cmd[@]}"

  rm -f "${body_file}"
  sleep 0.2
done

echo "done: created issues from ${ISSUE_DIR}"
