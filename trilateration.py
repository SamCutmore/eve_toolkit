import numpy as np
import matplotlib.pyplot as plt

# Sphere centers and radii (km)
Gate = np.array([0, 0, 0])
Z = np.array([0, 0, 2290])  # Z sphere center
Y = np.array([0, 890, 0])   # Y sphere center

# Radii (in kilometers)
Gate_radius = 1840
Z_radius = 4132
Y_radius = 2115

# Function to calculate the distance between two points
def distance(p1, p2):
    return np.linalg.norm(p2 - p1)

# Function to calculate the intersection of two spheres (for demonstration)
def spheres_intersection(center1, radius1, center2, radius2):
    d = distance(center1, center2)
    
    # Check if the spheres intersect (sum of radii > distance between centers)
    if d > radius1 + radius2 or d < abs(radius1 - radius2):
        return None  # No intersection
    
    # Compute the point of intersection along the line connecting the two centers
    a = (radius1**2 - radius2**2 + d**2) / (2 * d)
    h = np.sqrt(radius1**2 - a**2)
    
    # Compute the point of intersection on the line joining the centers
    mid_point = center1 + a * (center2 - center1) / d
    intersection_points = []
    
    # Perpendicular vector to the line joining the centers
    perpendicular = np.array([- (center2[1] - center1[1]), center2[0] - center1[0], 0])
    perpendicular = perpendicular / np.linalg.norm(perpendicular)  # Normalize
    
    # Points of intersection (two solutions)
    intersection_points.append(mid_point + h * perpendicular)
    intersection_points.append(mid_point - h * perpendicular)
    
    return intersection_points

# Function to check all sphere intersections
def check_all_intersections():
    # Check pairwise intersections of the three spheres
    intersections_gate_z = spheres_intersection(Gate, Gate_radius, Z, Z_radius)
    intersections_z_y = spheres_intersection(Z, Z_radius, Y, Y_radius)
    intersections_gate_y = spheres_intersection(Gate, Gate_radius, Y, Y_radius)
    
    if intersections_gate_z is None:
        print("No intersection found between Gate and Z spheres.")
    else:
        print("Intersections between Gate and Z spheres:", intersections_gate_z)
        
    if intersections_z_y is None:
        print("No intersection found between Z and Y spheres.")
    else:
        print("Intersections between Z and Y spheres:", intersections_z_y)
        
    if intersections_gate_y is None:
        print("No intersection found between Gate and Y spheres.")
    else:
        print("Intersections between Gate and Y spheres:", intersections_gate_y)

# Function to plot the spheres
def plot_spheres_projection():
    fig, axs = plt.subplots(1, 3, figsize=(18, 6))

    # Define a grid for plotting the circles
    theta = np.linspace(0, 2 * np.pi, 100)
    
    # Plot for the x-z plane (x vs z)
    axs[0].plot(Gate[0] + Gate_radius * np.cos(theta), Gate[2] + Gate_radius * np.sin(theta), label="Gate", color='r')
    axs[0].plot(Z[0] + Z_radius * np.cos(theta), Z[2] + Z_radius * np.sin(theta), label="Z", color='g')
    axs[0].plot(Y[0] + Y_radius * np.cos(theta), Y[2] + Y_radius * np.sin(theta), label="Y", color='b')
    axs[0].scatter(Gate[0], Gate[2], color='r', zorder=5)  # Gate center
    axs[0].scatter(Z[0], Z[2], color='g', zorder=5)  # Z center
    axs[0].scatter(Y[0], Y[2], color='b', zorder=5)  # Y center
    axs[0].set_xlabel('X')
    axs[0].set_ylabel('Z')
    axs[0].set_title('X-Z Plane')
    axs[0].set_aspect('equal', 'box')
    axs[0].legend()

    # Plot for the y-z plane (y vs z)
    axs[1].plot(Gate[1] + Gate_radius * np.cos(theta), Gate[2] + Gate_radius * np.sin(theta), label="Gate", color='r')
    axs[1].plot(Z[1] + Z_radius * np.cos(theta), Z[2] + Z_radius * np.sin(theta), label="Z", color='g')
    axs[1].plot(Y[1] + Y_radius * np.cos(theta), Y[2] + Y_radius * np.sin(theta), label="Y", color='b')
    axs[1].scatter(Gate[1], Gate[2], color='r', zorder=5)  # Gate center
    axs[1].scatter(Z[1], Z[2], color='g', zorder=5)  # Z center
    axs[1].scatter(Y[1], Y[2], color='b', zorder=5)  # Y center
    axs[1].set_xlabel('Y')
    axs[1].set_ylabel('Z')
    axs[1].set_title('Y-Z Plane')
    axs[1].set_aspect('equal', 'box')
    axs[1].legend()

    # Plot for the x-y plane (x vs y)
    axs[2].plot(Gate[0] + Gate_radius * np.cos(theta), Gate[1] + Gate_radius * np.sin(theta), label="Gate", color='r')
    axs[2].plot(Z[0] + Z_radius * np.cos(theta), Z[1] + Z_radius * np.sin(theta), label="Z", color='g')
    axs[2].plot(Y[0] + Y_radius * np.cos(theta), Y[1] + Y_radius * np.sin(theta), label="Y", color='b')
    axs[2].scatter(Gate[0], Gate[1], color='r', zorder=5)  # Gate center
    axs[2].scatter(Z[0], Z[1], color='g', zorder=5)  # Z center
    axs[2].scatter(Y[0], Y[1], color='b', zorder=5)  # Y center
    axs[2].set_xlabel('X')
    axs[2].set_ylabel('Y')
    axs[2].set_title('X-Y Plane')
    axs[2].set_aspect('equal', 'box')
    axs[2].legend()

    plt.tight_layout()
    plt.show()


check_all_intersections()
plot_spheres_projection()
