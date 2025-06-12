import numpy as np
import matplotlib.pyplot as plt

def graph_warp_path(initial_radius, destination_radius, destination_center):
    """
    Graphs the possible warp paths in EVE Online as a wireframe of discrete lines.

    Parameters:
        initial_radius (float): Radius of the initial circle.
        destination_radius (float): Radius of the destination circle.
        destination_center (tuple of floats): (x, y, z) coordinates of the destination circle center.
    """
    num_points = 16  # Number of points on each circle

    # Generate points on the initial circle
    theta1 = np.linspace(0, 2 * np.pi, num_points, endpoint=False)
    x1 = initial_radius * np.cos(theta1)
    y1 = initial_radius * np.sin(theta1)
    z1 = np.zeros_like(x1)

    # Generate points on the destination circle
    theta2 = np.linspace(0, 2 * np.pi, num_points, endpoint=False)
    x2 = destination_radius * np.cos(theta2) + destination_center[0]
    y2 = destination_radius * np.sin(theta2) + destination_center[1]
    z2 = np.full_like(x2, destination_center[2])

    # Set up the 3D plot
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Plot the initial circle
    ax.plot(x1, y1, z1, color='blue', label='Initial Circle')
    ax.scatter(x1, y1, z1, color='blue')

    # Plot the destination circle
    ax.plot(x2, y2, z2, color='red', label='Destination Circle')
    ax.scatter(x2, y2, z2, color='red')

    # Plot lines connecting every point on the initial circle to every point on the destination circle
    for i in range(num_points):
        for j in range(num_points):
            ax.plot([x1[i], x2[j]], [y1[i], y2[j]], [z1[i], z2[j]], color='green', alpha=0.6, linewidth=0.7)

    # Set plot labels and aspect
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_zlabel('Z-axis')
    ax.legend()
    ax.set_box_aspect([1, 1, 1])  # Equal aspect ratio

    plt.show()

graph_warp_path(initial_radius=10000, destination_radius=2500, destination_center=(0, 0, 20000000))