from skyfield.api import load, EarthSatellite
import numpy as np

# ---------- SETUP ----------
ts = load.timescale()

with open("data/tle.txt") as f:
    lines = f.read().strip().split("\n")

satellite = EarthSatellite(lines[1], lines[2], lines[0], ts)
debris = EarthSatellite(lines[4], lines[5], lines[3], ts)

# ---------- TIME WINDOW ----------
minutes = np.arange(0, 24 * 60, 10)
times = ts.now() + minutes / (24 * 60)

# ---------- POSITIONS ----------
sat_pos = satellite.at(times).position.km
deb_pos = debris.at(times).position.km

# ---------- DISTANCE ----------
distances = np.linalg.norm(sat_pos - deb_pos, axis=0)

min_distance = distances.min()
idx = distances.argmin()
collision_time = times[idx].utc_strftime()

# ---------- RISK LOGIC ----------
if min_distance < 2:
    risk = "🔴 HIGH RISK"
elif min_distance < 10:
    risk = "🟡 WARNING"
else:
    risk = "🟢 SAFE"

# ---------- OUTPUT ----------
print("🛰️ Satellite :", satellite.name)
print("🧩 Debris    :", debris.name)
print(f"📏 Min Distance : {min_distance:.2f} km")
print(f"⏱️ Time        : {collision_time}")
print(f"⚠️ Risk Level  : {risk}")
