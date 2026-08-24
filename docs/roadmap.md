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
      exploration — nav2_bringup/slam_toolbox are installed but not wired up
      yet

## Milestone 4 — Cooperative landing — done
- [x] `landing_target_detector`: UAV-side ArUco detection + pinhole
      pixel-to-world offset, publishes `LandingTarget`
- [x] `precision_landing`: descends toward detected marker, disarms on
      touchdown
- [x] `landing_platform_coordinator` holds position while `perch/landing_in_progress`

## Milestone 5 — Polish
- [x] Single `perch_sim.launch.py` bringing up world + bridge + UAV + UGV + all nodes
- [ ] Demo recording (survey → photo/coverage capture → payload drop → land on UGV)
- [ ] README gifs/screenshots
- [ ] Tune `landing_target_detector`'s pixel→world mapping against a
      ground-truth offset (currently derived analytically from the camera's
      pose, not empirically calibrated in sim)
