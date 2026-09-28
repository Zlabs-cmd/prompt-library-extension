#!/usr/bin/env bash
set -euo pipefail

ref="${VERCEL_GIT_COMMIT_REF:-}"
env_name="${VERCEL_ENV:-}"

case "${env_name}:${ref}" in
  production:*|*:main|*:master|*:production|*:release/*) exit 1 ;;
  *:diag/*|*:bisect/*|*:debug/*|*:test/*|*:experiment/*|*:agent/*|*:chore/diag-*|*:*-retry|*:*-retry/*) exit 0 ;;
esac

message="$(git log -1 --pretty=%B 2>/dev/null || true)"
if grep -Eq '\[(skip ci|skip vercel)\]' <<<"$message"; then
  exit 0
fi

exit 1
