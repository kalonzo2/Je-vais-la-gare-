import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Simulation parameters
L = 1.0           # Length of the string (meters)
T = 1000          # Tension (N)
mu = 0.01         # Linear mass density (kg/m)
c = np.sqrt(T/mu) # Wave speed

# Discretization
nx = 200          # Number of spatial points
dx = L / (nx - 1)
dt = 0.0005       # Time step
nt = 1000         # Number of time steps

# Stability condition (CFL condition)
assert c * dt / dx <= 1, "Unstable configuration: decrease dt or increase dx"

# Initial conditions
x = np.linspace(0, L, nx)
u = np.zeros(nx)              # Displacement at t
u_new = np.zeros(nx)          # Displacement at t + dt
u_old = np.zeros(nx)          # Displacement at t - dt

# Initial pulse (plucked in the middle)
u[int(nx/2)] = 0.1

# Animation setup
fig, ax = plt.subplots()
line, = ax.plot(x, u)
ax.set_ylim(-0.2, 0.2)
ax.set_title("Vibrating String Simulation")

def update(frame):
    global u, u_old, u_new
    for i in range(1, nx - 1):
        u_new[i] = (2 * u[i] - u_old[i] +
                    (c**2) * (dt**2 / dx**2) * (u[i+1] - 2*u[i] + u[i-1]))
    u_old, u = u, u_new.copy()
    line.set_ydata(u)
    return line,

ani = animation.FuncAnimation(fig, update, frames=nt, 
