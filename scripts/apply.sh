#!/usr/bin/env bash
set -euo pipefail

ENV_NAME="${1:?usage: apply.sh <staging|prod>}"
RENDER_DIR="${2:-rendered}"

# apply in deterministic order across DBs and steps
for f in $(ls "${RENDER_DIR}/${ENV_NAME}__"*.sql | sort); do
  echo "Applying: $f"
  snowsql -a "$SNOWFLAKE_ACCOUNT" \
          -u "$SNOWFLAKE_USER" \
          -o exit_on_error=true \
          -q "$(cat "$f")"
done
