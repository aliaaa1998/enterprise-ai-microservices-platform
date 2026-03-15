#!/usr/bin/env bash
set -euo pipefail

curl -sS http://localhost:8000/api/v1/summarize \
  -H "Content-Type: application/json" \
  -d @examples/summarizer/policy.json | jq .
