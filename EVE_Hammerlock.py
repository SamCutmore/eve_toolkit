import numpy as np
import matplotlib.pyplot as plt

class Ship:
    def __init__(self, max_velocity, mass, inertia):
        self.max_velocity = max_velocity
        self.mass = mass
        self.inertia = inertia
        self.position = np.array([0.0, 0.0])
        self.velocity = np.array([0.0, 0.0])

    def update_velocity(self, time, target_direction):
        target_direction = target_direction / np.linalg.norm(target_direction)
        target_speed = self.max_velocity * (1 - np.exp(-time * 1e6 / (self.inertia * self.mass)))
        target_velocity = target_speed * target_direction
        
        # Adjust current velocity towards target velocity smoothly
        adjustment_factor = 0.1  # Controls how fast the ship turns to new heading
        self.velocity = (1 - adjustment_factor) * self.velocity + adjustment_factor * target_velocity
    
    def move(self):
        self.position += self.velocity

# Ship parameters
tholos = Ship(max_velocity=2153, mass=1_700_000, inertia=1.856)
crow = Ship(max_velocity=6134, mass=1_565_000, inertia=1.278)

# Simulation parameters
timesteps = 100
target_distance = 24000
running_mode = True
max_relative_velocity = -np.inf
switch_time = None

# Initial positions
crow.position = np.array([24000.0, 0.0])
tholos_positions = []
crow_positions = []
tholos_velocities = []
crow_velocities = []
distances = []

for t in range(1, timesteps + 1):
    crow_to_tholos = tholos.position - crow.position
    current_distance = np.linalg.norm(crow_to_tholos)
    relative_velocity = np.dot(tholos.velocity - crow.velocity, crow_to_tholos / current_distance)
    
    if current_distance > target_distance:
        crow_target_direction = crow_to_tholos
    elif current_distance < target_distance:
        crow_target_direction = -crow_to_tholos
    else:
        crow_target_direction = np.array([-crow_to_tholos[1], crow_to_tholos[0]])
    
    if running_mode:
        tholos_direction = -crow_to_tholos
        if relative_velocity > max_relative_velocity:
            max_relative_velocity = relative_velocity
            switch_time = t + 1
    else:
        tholos_direction = crow.position - tholos.position
    
    if running_mode and switch_time is not None and t >= switch_time:
        running_mode = False
    
    tholos.update_velocity(t, tholos_direction)
    crow.update_velocity(t, crow_target_direction)
    tholos.move()
    crow.move()
    
    tholos_positions.append(tholos.position.copy())
    crow_positions.append(crow.position.copy())
    tholos_velocities.append(np.linalg.norm(tholos.velocity))
    crow_velocities.append(np.linalg.norm(crow.velocity))
    distances.append(current_distance)

tholos_positions = np.array(tholos_positions)
crow_positions = np.array(crow_positions)
min_distance = min(distances)

plt.figure(figsize=(10, 5))
plt.plot(range(1, timesteps + 1), distances, label="Distance Between Ships", color="purple")
plt.axhline(y=min_distance, color="black", linestyle="--", label=f"Min Distance: {min_distance:.2f} m")
plt.axhline(y=target_distance, color="green", linestyle="--", label=f"Target Distance: {target_distance} m")
plt.xlabel("Time (s)")
plt.ylabel("Distance (m)")
plt.title("Relative Distance Between Tholos and Crow Over Time")
plt.legend()
plt.grid()
plt.show()

plt.figure(figsize=(10, 5))
plt.plot(range(1, timesteps + 1), tholos_velocities, label="Tholos Velocity", color="blue")
plt.plot(range(1, timesteps + 1), crow_velocities, label="Crow Velocity", color="red")
plt.xlabel("Time (s)")
plt.ylabel("Velocity (m/s)")
plt.title("Velocity of Tholos and Crow Over Time")
plt.legend()
plt.grid()
plt.show()

plt.figure(figsize=(10, 5))
plt.plot(tholos_positions[:, 0], tholos_positions[:, 1], label="Tholos Path", color="blue")
plt.plot(crow_positions[:, 0], crow_positions[:, 1], label="Crow Path", color="red")
plt.xlabel("X Position (m)")
plt.ylabel("Y Position (m)")
plt.title("X-Y Position of Tholos and Crow Over Time")
plt.legend()
plt.grid()
plt.show()

print(f"Minimum distance achieved: {min_distance:.2f} meters")
