# Roadmap

## Milestone 1 — Environment
- [ ] Install ROS2 (Jazzy), Gazebo, PX4-Autopilot SITL
- [ ] Get PX4 SITL + Gazebo default quadcopter flying via ROS2 offboard control
- [ ] Get a simple UGV (e.g. TurtleBot-style diff-drive) spawned in the same world

## Milestone 2 — UAV survey mission
- [ ] Waypoint survey mission node (`survey_mission`)
- [ ] RGB photo capture on trigger/interval (`photo_capture`)
- [ ] Depth camera coverage/heatmap builder (`coverage_mapper`)
- [ ] Simulated payload drop service (`DropPayload.srv`)

## Milestone 3 — UGV autonomy
- [ ] SLAM + nav2 stack for the UGV
- [ ] UGV explores/patrols independently
- [ ] AprilTag mounted on UGV deck (landing marker)

## Milestone 4 — Cooperative landing
- [ ] `landing_target_detector`: UAV-side AprilTag detection, publish `LandingTarget`
- [ ] `precision_landing`: descend and land relative to detected marker (moving or stationary)
- [ ] `landing_platform_coordinator`: UGV slows/holds when a landing is in progress

## Milestone 5 — Polish
- [ ] Single `perch_sim.launch.py` bringing up world + UAV + UGV + all nodes
- [ ] Demo recording (survey → photo/coverage capture → payload drop → land on UGV)
- [ ] README gifs/screenshots
