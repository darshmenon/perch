# PERCH

Platform for Enhanced Reconnaissance & Cooperative Homing.

A simulated quadcopter UAV that flies autonomous surveillance/survey missions
(photo capture + depth-based coverage mapping, optional payload drop), and a
UGV ground rover that navigates/maps independently and serves as a mobile
landing platform the UAV can detect and land on.

## Scope (v1)

- Simulation only: Gazebo + PX4 SITL + ROS2.
- UAV: PX4 offboard control via ROS2, waypoint survey missions, RGB camera
  for photo capture, depth camera for coverage/obstacle mapping, payload
  drop mechanism (simulated).
- UGV: independent nav2-based navigation/SLAM, carries a visual landing
  marker (AprilTag) on its deck.
- Landing: UAV detects the UGV's marker via onboard camera and performs a
  precision landing on the moving/stationary platform.

## Stack

- ROS2 (Humble or Jazzy)
- PX4 Autopilot (SITL) + MAVSDK/ROS2 offboard control
- Gazebo (Harmonic/Garden, matching PX4 SITL support)
- nav2 for UGV navigation
- AprilTag (apriltag_ros) for vision-based landing target detection

## Repo layout

- `ros2_ws/src/` — ROS2 packages (UAV control, UGV nav, vision, bringup, msgs)
- `sim/` — Gazebo worlds and models
- `scripts/` — setup/build/launch helper scripts
- `docs/` — architecture notes and mission design

## Status

Early scaffolding. See `docs/roadmap.md` for planned milestones.
