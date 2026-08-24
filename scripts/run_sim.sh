#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

bash "$REPO_ROOT/scripts/setup_sim_assets.sh"

export GZ_SIM_RESOURCE_PATH="$REPO_ROOT/sim/models:${GZ_SIM_RESOURCE_PATH:-}"

exec gz sim -r "$REPO_ROOT/sim/worlds/perch_world.sdf" "$@"
