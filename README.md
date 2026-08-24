# PERCH

Platform for Enhanced Reconnaissance & Cooperative Homing.

A simulated quadcopter UAV that flies an autonomous survey mission (RGB photo
capture, depth-based coverage mapping, payload drop), and a UGV ground rover
that patrols independently and serves as a mobile landing platform the UAV
detects (ArUco marker) and lands on.

## Status: working end-to-end in sim

`ros2 launch perch_bringup perch_sim.launch.py` brings up Gazebo, the ROS2/Gazebo
bridge, and every node, and runs the full mission unattended: takeoff, lawnmower
survey with periodic photo capture and live coverage-heatmap generation, a
mid-survey payload drop, then handoff to vision-based precision landing on the
UGV's deck marker while the UGV keeps patrolling (slowed, not stopped) —
the UAV leads the marker using the UGV's velocity and lands on the moving
platform.

## Scope (v1)

- Simulation only, built entirely on tools already available locally (Gazebo
  Harmonic + ROS2 Humble + OpenCV) — no PX4 SITL, no extra apt installs.
- UAV: velocity offboard control (Gazebo's `MulticopterVelocityControl`),
  lawnmower survey mission, RGB photo capture, depth-based coverage heatmap,
  payload drop via a detachable-joint plugin, ArUco-based precision landing.
- UGV: diff-drive rover with a lidar and an ArUco (`DICT_4X4_50`, id 0) deck
  marker, rectangular patrol controller, holds position during a landing.

## Stack

- ROS2 Humble
- Gazebo Harmonic (`gz sim`), via `ros_gz_bridge`
- OpenCV `cv2.aruco` for landing-marker detection (no `apriltag_ros` needed)
- nav2 / slam_toolbox are installed and reserved for a future upgrade from the
  current simple patrol controller to full SLAM-based UGV navigation

### Why not PX4?

PX4 SITL needs several apt packages (`genromfs`, `astyle`, `gperf`, `flex`,
`bison`, ...) that require root, which wasn't available in this environment.
Gazebo's built-in `MulticopterVelocityControl`/`MulticopterMotorModel` plugins
give the same body-frame velocity control PX4 offboard mode would, using only
what's already installed. Swapping in real PX4 SITL later is a drop-in
replacement for `offboard_control.py`'s command topic, not a rearchitecture.

## Running it

```bash
scripts/setup_sim_assets.sh          # one-time: downloads + patches the X3 UAV model with cameras
cd ros2_ws && colcon build --symlink-install && source install/setup.bash
ros2 launch perch_bringup perch_sim.launch.py
```

Photos land in `~/perch_captures/photos/`, the coverage heatmap is written to
`~/perch_captures/coverage_heatmap.png` (refreshed every 5s).

To fly/drive manually instead, `scripts/run_sim.sh` launches just the Gazebo
world (see the comments in `sim/worlds/perch_world.sdf` for raw `gz topic`
teleop commands).

## Repo layout

- `ros2_ws/src/` — ROS2 packages:
  - `perch_msgs` — `LandingTarget` msg, `DropPayload` srv
  - `perch_uav_control` — offboard velocity control, survey mission, payload
    drop, precision landing
  - `perch_vision` — photo capture, coverage mapper, ArUco landing detector
  - `perch_ugv_nav` — UGV patrol / landing-platform coordinator
  - `perch_bringup` — bridge config + top-level launch file
- `sim/worlds/perch_world.sdf` — the combined UAV + UGV + payload world
- `sim/models/perch_ugv/` — UGV model (diff-drive, lidar, ArUco deck marker)
- `scripts/` — asset setup and sim launch helpers
- `docs/` — roadmap and architecture notes

## Roadmap

See `docs/roadmap.md` — Milestones 1 and 2 are done; UGV SLAM/nav2 (Milestone 3)
is the next real piece of work.
