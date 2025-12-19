from skyfield.api import load, EarthSatellite
import numpy as np
from core.visualize_3d import plot_orbits_3d

ts = load.timescale()

# Load TLEs
with open("data/tle.txt") as f:
    lines = [l.strip() for l in f if l.strip()]

# Parse blocks
blocks = [lines[i:i+3] for i in range(0, len(lines), 3)]

# Satellite
sat_name, l1, l2 = blocks[0]
sat = EarthSatellite(l1, l2, sat_name, ts)

# Time range
minutes = np.arange(0, 24 * 60, 10)
times = ts.now() + minutes / (24 * 60)
sat_pos = sat.at(times).position.km

# Debris
debris_positions = []
debris_names = []
closest_points = []

for block in blocks[1:]:
    name, d1, d2 = block
    deb = EarthSatellite(d1, d2, name, ts)

    deb_pos = deb.at(times).position.km
    debris_positions.append(deb_pos)
    debris_names.append(name)

    distances = np.linalg.norm(sat_pos - deb_pos, axis=0)
    idx = distances.argmin()
    closest_points.append(
        (deb_pos[0][idx], deb_pos[1][idx], deb_pos[2][idx])
    )

# Plot
plot_orbits_3d(
    sat_pos,
    debris_positions,
    debris_names,
    closest_points
)
