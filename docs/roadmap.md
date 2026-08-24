# Roadmap

## Milestone 1 — Environment — done
- [x] ROS2 Humble + Gazebo Harmonic already available; PX4 SITL swapped for
      Gazebo's built-in multicopter velocity control (no root/apt access, see
      README "Why not PX4?")
- [x] X3 UAV (Fuel model, patched with downward RGB + depth cameras) flying
      via `MulticopterVelocityControl`
- [x] Custom diff-drive UGV (`sim/models/perch_ugv`) with lidar + ArUco deck
      marker, spawned in the same world

## Milestone 2 — UAV survey mission — done
- [x] Lawnmower waypoint survey mission node (`survey_mission`)
- [x] RGB photo capture on a timer (`photo_capture`)
- [x] Depth camera coverage heatmap builder (`coverage_mapper`)
- [x] Payload drop via detachable-joint plugin + `DropPayload.srv`
      (`payload_drop`)

## Milestone 3 — UGV autonomy — partial
- [x] Rectangular patrol controller (`landing_platform_coordinator`)
- [x] ArUco marker mounted on UGV deck (landing marker)
- [ ] Upgrade patrol controller to real SLAM (slam_toolbox) + nav2
      exploration by reusing `rosnav_bot` (github.com/darshmenon/rosnav) as an
      external dependency instead of writing nav2/SLAM tuning from scratch:
  - [x] `perch_ugv`'s `DiffDrive` plugin now publishes `odom`/`base_link`
        frames and the ROS/Gazebo bridge (`bridge.yaml`) exposes
        unnamespaced `scan`/`odom`/`cmd_vel`, matching `rosnav_bot`'s default
        `nav2_params.yaml`/`slam_params.yaml` (`scan_topic: scan`,
        `odom_topic: /odom`, `base_frame_id: base_link`) with no remapping
        needed
  - [ ] Clone `rosnav_bot` alongside `perch/ros2_ws/src` (separate repo, not
        vendored) and `colcon build` it in the same workspace
  - [ ] Launch its `slam_nav.launch.py` (or `nav2.launch.py` against a
        pre-built map) instead of/alongside `perch_bringup`'s launch, pointed
        at the already-running perch world
  - [ ] Retire `landing_platform_coordinator`'s hardcoded rectangular
        patrol in favor of nav2 goal poses (frontier exploration via
        `explore_lite`/`rrt_explore`, both already in `rosnav_bot`) — the
        "hold during landing" behavior becomes a nav2 goal cancel/pause
        instead of a raw `Twist` override
  - [ ] Not yet validated end-to-end: no combined perch+rosnav_bot launch
        has actually been run in sim

## Milestone 4 — Cooperative landing — done
- [x] `landing_target_detector`: UAV-side ArUco detection + pinhole
      pixel-to-world offset, publishes `LandingTarget`
- [x] `precision_landing`: tracks the detected marker with a velocity-led
      goal, descends once horizontally aligned, disarms on touchdown
- [x] `landing_platform_coordinator` keeps patrolling (slowed) during
      landing instead of stopping — UAV lands on a moving platform

## Milestone 5 — Polish
- [x] Single `perch_sim.launch.py` bringing up world + bridge + UAV + UGV + all nodes
- [ ] Demo recording (survey → photo/coverage capture → payload drop → land on UGV)
- [ ] README gifs/screenshots
- [ ] Tune `landing_target_detector`'s pixel→world mapping against a
      ground-truth offset (currently derived analytically from the camera's
      pose, not empirically calibrated in sim)
