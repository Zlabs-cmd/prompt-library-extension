#!/usr/bin/env bash
set -euo pipefail

ref="${VERCEL_GIT_COMMIT_REF:-}"
env_name="${VERCEL_ENV:-}"
message="$(git log -1 --pretty=%B 2>/dev/null || true)"

if grep -Eq '\[(skip ci|skip vercel)\]' <<<"$message"; then
  exit 0
fi

case "${env_name}:${ref}" in
  production:*|*:main|*:master|*:production|*:release/*|*:staging|*:preview/*) exit 1 ;;
  *:diag/*|*:bisect/*|*:debug/*|*:test/*|*:experiment/*|*:agent/*|*:chore/diag-*|*:*-retry|*:*-retry/*) exit 0 ;;
esac

if grep -Eq '\[(deploy preview|vercel preview)\]' <<<"$message"; then
  exit 1
fi

# Cost-first default: PR/feature branches do not receive paid Vercel previews
# unless explicitly requested with preview/*, staging, or [deploy preview].
exit 0
