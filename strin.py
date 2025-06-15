import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# --- Parameters ---
L = 1.0
T = 5.0
n = 2
c = 1.0
pi = np.pi
ħ = 1.0
m = 1.0
G = 1.0  # Gravitational constant (in natural units)

nx = 100
nt = 200
x = np.linspace(0, L, nx)
t = np.linspace(0, T, nt)
X, T_grid = np.meshgrid(x, t)

# --- Schrödinger Wavefunction ---
E_n = (n * pi * ħ)**2 / (2 * m * L**2)
psi_n = np.sqrt(2 / L) * np.sin(n * pi * x / L)
Psi = np.outer(np.exp(-1j * E_n * t / ħ), psi_n)
prob_density = np.abs(Psi)**2

# --- Wick-Rotated Worldsheet ---
tau_E = 1j * t
T_grid_E, X_E = np.meshgrid(tau_E, x, indexing='ij')
Y_E = np.sin(n * pi * X_E / L) * np.exp(-n * pi * c * T_grid_E.imag / L)
conformal_factor_E = 1 + 0.3 * np.sin(4 * pi * X_E) * np.cos(2 * pi * T_grid_E.imag / T)
Y_E_gauged = (Y_E.real) * conformal_factor_E

# --- Polyakov Action (Euclidean) ---
dX_dσ_E = np.gradient(Y_E_gauged, axis=1) / (x[1] - x[0])
dX_dτ_E = np.gradient(Y_E_gauged, axis=0) / (t[1] - t[0])
integrand_E = dX_dτ_E**2 + dX_dσ_E**2
polyakov_action_E = np.sum(integrand_E) * (x[1] - x[0]) * (t[1] - t[0])

# --- Branes & Strings ---
brane_positions = [(0.2, 'red'), (0.5, 'green'), (0.8, 'blue')]
strings = [(0.2, 0.5), (0.5, 0.8), (0.2, 0.8)]

# --- Einstein Field Equations (EFE) Visualization ---
# Simplified: Einstein tensor trace ~ curvature from energy density
curvature = G * prob_density  # T_μν ∝ |Ψ|², G_μν ∝ T_μν (in natural units)

# --- Plotting ---
fig = plt.figure(figsize=(18, 6))

# Plot 1: Schrödinger Probability Density
ax1 = fig.add_subplot(131, projection='3d')
ax1.plot_surface(X, T_grid, prob_density, cmap='viridis', edgecolor='none')
ax1.set_title('Quantum Probability Density (Ψ*Ψ)')
ax1.set_xlabel('x')
ax1.set_ylabel('t')
ax1.set_zlabel('|Ψ|²')
ax1.view_init(elev=30, azim=-60)

# Plot 2: Worldsheet with Polyakov Action
ax2 = fig.add_subplot(132, projection='3d')
ax2.plot_surface(X_E, T_grid_E.imag, Y_E_gauged, cmap='inferno', edgecolor='none')
ax2.set_title(f'Euclidean Worldsheet (Polyakov S ≈ {polyakov_action_E:.2f})')
ax2.set_xlabel('σ')
ax2.set_ylabel('τ_E')
ax2.set_zlabel('Amplitude')
ax2.view_init(elev=30, azim=-60)

# Plot 3: Curvature from EFE (Einstein tensor trace ~ energy density)
ax3 = fig.add_subplot(133, projection='3d')
ax3.plot_surface(X, T_grid, curvature, cmap='plasma', edgecolor='none')
ax3.set_title('Einstein Curvature from Energy Density')
ax3.set_xlabel('x')
ax3.set_ylabel('t')
ax3.set_zlabel('Gμν ∼ |Ψ|²')
ax3.view_init(elev=30, azim=-60)

plt.tight_layout()
plt.show()
