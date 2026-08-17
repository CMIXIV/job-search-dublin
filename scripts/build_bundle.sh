#!/usr/bin/env bash
# Build the installable bundles from whatever is currently in this repo.
#
#   bash scripts/build_bundle.sh
#
# Produces dist/job-search-agent.skill and dist/job-search-agent.zip - the same
# archive twice, because Cowork's one-click install looks for .skill while some
# upload forms only accept .zip.
#
# The archive must contain a single top-level folder named job-search-agent
# with SKILL.md inside it. Build from source rather than copying an old bundle,
# or the shipped skill silently drifts from the repo.

set -euo pipefail
cd "$(dirname "$0")/.."
ROOT="$PWD"

STAGE=$(mktemp -d)
trap 'rm -rf "$STAGE"' EXIT

mkdir -p "$STAGE/job-search-agent"
cp -r SKILL.md README.md LICENSE references scripts templates "$STAGE/job-search-agent/"
rm -f "$STAGE/job-search-agent/scripts/build_bundle.sh"

mkdir -p dist
rm -f dist/job-search-agent.skill dist/job-search-agent.zip
( cd "$STAGE" && zip -qr "$ROOT/dist/job-search-agent.skill" job-search-agent )
cp dist/job-search-agent.skill dist/job-search-agent.zip

python3 - <<'PY'
import zipfile
z = zipfile.ZipFile("dist/job-search-agent.skill")
names = z.namelist()
assert "job-search-agent/SKILL.md" in names, "SKILL.md missing from bundle"
assert z.read("job-search-agent/SKILL.md").startswith(b"---"), "no frontmatter"
print(f"Built dist/job-search-agent.skill and .zip - {len(names)} entries, SKILL.md present.")
PY
