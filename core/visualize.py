import matplotlib.pyplot as plt
import numpy as np

def plot_orbits(sat_pos, debris_positions, debris_names, closest_points):
    plt.figure(figsize=(8, 8))

    # Satellite orbit
    plt.plot(sat_pos[0], sat_pos[1], label="Satellite", linewidth=2)

    # Debris orbits
    for i, deb_pos in enumerate(debris_positions):
        plt.plot(deb_pos[0], deb_pos[1], linestyle="--", label=debris_names[i])

        # Closest approach point
        cx, cy = closest_points[i]
        plt.scatter(cx, cy)

    # Earth (approx circle)
    earth_radius = 6371  # km
    theta = np.linspace(0, 2*np.pi, 200)
    plt.plot(
        earth_radius * np.cos(theta),
        earth_radius * np.sin(theta),
        linewidth=1
    )

    plt.xlabel("X (km)")
    plt.ylabel("Y (km)")
    plt.title("Satellite vs Space Debris Orbits (2D)")
    plt.legend()
    plt.axis("equal")
    plt.grid(True)
    plt.show()
