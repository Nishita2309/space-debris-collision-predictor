from skyfield.api import load, EarthSatellite
from core.visualize import plot_orbits
import numpy as np
import math

ts = load.timescale()

def parse_tle_blocks(lines):
    # Remove empty lines
    clean_lines = [line.strip() for line in lines if line.strip()]

    blocks = []
    for i in range(0, len(clean_lines), 3):
        blocks.append(clean_lines[i:i+3])

    return blocks


def risk_level(distance):
    if distance < 2:
        return "HIGH"
    elif distance < 10:
        return "WARNING"
    else:
        return "SAFE"

def predict_collision(tle_lines, hours=24, step_minutes=10):
    blocks = parse_tle_blocks(tle_lines)

    if len(blocks) < 2:
        raise ValueError("At least one satellite and one debris object are required")


    # First block = satellite
    sat_name, sat_l1, sat_l2 = blocks[0]
    satellite = EarthSatellite(sat_l1, sat_l2, sat_name, ts)

    minutes = np.arange(0, hours * 60, step_minutes)
    times = ts.now() + minutes / (24 * 60)
    sat_pos = satellite.at(times).position.km

    debris_results = []

    for block in blocks[1:]:
        name, l1, l2 = block
        debris = EarthSatellite(l1, l2, name, ts)

        deb_pos = debris.at(times).position.km
        distances = np.linalg.norm(sat_pos - deb_pos, axis=0)

        min_dist = float(distances.min())
        idx = distances.argmin()

        prob = collision_probability(min_dist)

        debris_results.append({
            "debris": name,
            "min_distance_km": round(min_dist, 2),
            "time_utc": times[idx].utc_strftime(),
            "risk_level": risk_level(min_dist),
            "collision_probability": prob
        })


    # Find most dangerous debris
    worst = max(debris_results, key=lambda x: x["collision_probability"])

    # ---- Visualization data prep ----
    debris_positions = []
    debris_names = []
    closest_points = []

    for block in blocks[1:]:
        name, l1, l2 = block
        debris = EarthSatellite(l1, l2, name, ts)

        deb_pos = debris.at(times).position.km
        debris_positions.append(deb_pos)
        debris_names.append(name)

        distances = np.linalg.norm(sat_pos - deb_pos, axis=0)
        idx = distances.argmin()
        closest_points.append((deb_pos[0][idx], deb_pos[1][idx]))

    # Plot (for demo/testing)
    plot_orbits(
        sat_pos,
        debris_positions,
        debris_names,
        closest_points
    )

    return {
        "satellite": satellite.name,
        "prediction_window_hours": hours,
        "time_step_minutes": step_minutes,
        "most_dangerous_debris": worst,
        "all_debris": debris_results
    }

def collision_probability(distance_km):
    D = 5.0  # scaling factor (km)
    return round(math.exp(-distance_km / D), 3)
