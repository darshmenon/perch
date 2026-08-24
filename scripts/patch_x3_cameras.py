#!/usr/bin/env python3
import sys

CAMERA_BLOCK = """
            <sensor name="perch_downward_camera" type="camera">
                <pose>0 0 -0.06 0 1.5707963 0</pose>
                <update_rate>15</update_rate>
                <camera>
                    <horizontal_fov>1.4</horizontal_fov>
                    <image>
                        <width>640</width>
                        <height>480</height>
                    </image>
                    <clip>
                        <near>0.05</near>
                        <far>50</far>
                    </clip>
                </camera>
                <always_on>1</always_on>
                <visualize>false</visualize>
            </sensor>
            <sensor name="perch_downward_depth_camera" type="depth_camera">
                <pose>0 0 -0.06 0 1.5707963 0</pose>
                <update_rate>10</update_rate>
                <camera>
                    <horizontal_fov>1.4</horizontal_fov>
                    <image>
                        <width>320</width>
                        <height>240</height>
                    </image>
                    <clip>
                        <near>0.1</near>
                        <far>30</far>
                    </clip>
                </camera>
                <always_on>1</always_on>
                <visualize>false</visualize>
            </sensor>
"""


def main():
    path = sys.argv[1]
    with open(path) as f:
        content = f.read()

    marker = '<link name="X3/base_link">'
    idx = content.index(marker)
    close_idx = content.index("</link>", idx)
    patched = content[:close_idx] + CAMERA_BLOCK + content[close_idx:]

    with open(path, "w") as f:
        f.write(patched)


if __name__ == "__main__":
    main()
