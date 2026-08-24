#!/usr/bin/env bash
set -euo pipefail

VERSION=6
MODEL_URI="https://fuel.gazebosim.org/1.0/OpenRobotics/models/X3 UAV"
CACHE_DIR="$HOME/.gz/fuel/fuel.gazebosim.org/openrobotics/models/x3 uav/$VERSION"
MODEL_SDF="$CACHE_DIR/model.sdf"

if [ ! -f "$MODEL_SDF" ]; then
  echo "Downloading X3 UAV model $VERSION from Fuel..."
  gz fuel download -u "$MODEL_URI/$VERSION"
fi

if grep -q "perch_downward_camera" "$MODEL_SDF"; then
  echo "X3 UAV model already patched with cameras, skipping."
  exit 0
fi

echo "Patching X3 UAV base_link with downward RGB + depth cameras..."
python3 "$(dirname "$0")/patch_x3_cameras.py" "$MODEL_SDF"
echo "Done."
