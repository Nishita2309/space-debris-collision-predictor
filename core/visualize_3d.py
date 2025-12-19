import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

def plot_orbits_3d(sat_pos, debris_positions, debris_names, closest_points):
    fig = plt.figure(figsize=(9, 9))
    ax = fig.add_subplot(111, projection="3d")

    # Satellite orbit
    ax.plot(
        sat_pos[0], sat_pos[1], sat_pos[2],
        label="Satellite",
        linewidth=2
    )

    # Debris orbits
    for i, deb_pos in enumerate(debris_positions):
        ax.plot(
            deb_pos[0], deb_pos[1], deb_pos[2],
            linestyle="--",
            label=debris_names[i]
        )

        # Closest approach point
        cx, cy, cz = closest_points[i]
        ax.scatter(cx, cy, cz, s=40)

    # Earth (sphere)
    earth_radius = 6371  # km
    u = np.linspace(0, 2 * np.pi, 50)
    v = np.linspace(0, np.pi, 50)

    x = earth_radius * np.outer(np.cos(u), np.sin(v))
    y = earth_radius * np.outer(np.sin(u), np.sin(v))
    z = earth_radius * np.outer(np.ones_like(u), np.cos(v))

    ax.plot_surface(x, y, z, alpha=0.2)

    ax.set_xlabel("X (km)")
    ax.set_ylabel("Y (km)")
    ax.set_zlabel("Z (km)")
    ax.set_title("3D Satellite–Debris Orbit Visualization")

    ax.legend()
    plt.show()
