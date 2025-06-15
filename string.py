import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.special import lpmv

# --- Constants ---
ħ = 1.0       # Reduced Planck constant
m = 1.0       # Mass
G = 1.0       # Gravitational constant (natural units)
pi = np.pi
c = 1.0       # Speed of light (natural units)

# --- Parameters for 1D String ---
L = 1.0
T = 5.0
nx = 100
nt = 200
x = np.linspace(0, L, nx)
t = np.linspace(0, T, nt)
X, T_grid = np.meshgrid(x, t)

# --- Schrödinger Wavefunction ---
n_s = 2  # quantum mode
E_n = (n_s * pi * ħ)**2 / (2 * m * L**2)
psi_n = np.sqrt(2 / L) * np.sin(n_s * pi * x / L)
Psi = np.outer(np.exp(-1j * E_n * t / ħ), psi_n)
prob_density = np.abs(Psi)**2

# --- Wick Rotation (Euclidean time) ---
tau_E = 1j * t
T_grid_E, X_E = np.meshgrid(tau_E, x, indexing='ij')
Y_E = np.sin(n_s * pi * X_E / L) * np.exp(-n_s * pi * c * T_grid_E.imag / L)
conformal_factor_E = 1 + 0.3 * np.sin(4 * pi * X_E) * np.cos(2 * pi * T_grid_E.imag / T)
Y_E_gauged = Y_E.real * conformal_factor_E

# --- Polyakov Action (Euclidean) ---
dX_dσ_E = np.gradient(Y_E_gauged, axis=1) / (x[1] - x[0])
dX_dτ_E = np.gradient(Y_E_gauged, axis=0) / (t[1] - t[0])
integrand_E = dX_dτ_E**2 + dX_dσ_E**2
polyakov_action_E = np.sum(integrand_E) * (x[1] - x[0]) * (t[1] - t[0])

# --- Einstein Field Equations (simplified: curvature from energy) ---
curvature = G * prob_density  # Gμν ~ Tμν ~ |Ψ|²

# --- Spherical Quantum Calculus ---
r_max = 5.0
nr = 100
ntheta = 100
r = np.linspace(0, r_max, nr)
theta = np.linspace(0, pi, ntheta)
R, Theta = np.meshgrid(r, theta)

# Valid hydrogen-like quantum numbers
n = 3
l = 2

def radial_wavefunction(n, l, r):
    rho = 2 * r / n
    coeff = (2 / n)**3 * np.math.factorial(n - l - 1) / (2 * n * np.math.factorial(n + l))
    normalization = np.sqrt(coeff)
    return normalization * rho**l * np.exp(-rho / 2)

def angular_wavefunction(l, m, theta):
    return lpmv(m, l, np.cos(theta))

R_nl = radial_wavefunction(n, l, R)
Y_lm = angular_wavefunction(l, 0, Theta)
Psi_sph = R_nl * Y_lm
prob_density_sph = np.abs(Psi_sph)**2 * R**2 * np.sin(Theta)

# Convert spherical to Cartesian for visualization
X_sph = R * np.sin(Theta)
Z_sph = R * np.cos(Theta)

# --- Plotting ---
fig = plt.figure(figsize=(18, 12))

# 1. Schrödinger Probability Density
ax1 = fig.add_subplot(221, projection='3d')
ax1.plot_surface(X, T_grid, prob_density, cmap='viridis', edgecolor='none')
ax1.set_title('1D Quantum String |Ψ|²')
ax1.set_xlabel('x')
ax1.set_ylabel('t')
ax1.set_zlabel('|Ψ|²')
ax1.view_init(elev=30, azim=-60)

# 2. Polyakov Worldsheet (Euclidean)
ax2 = fig.add_subplot(222, projection='3d')
ax2.plot_surface(X_E, T_grid_E.imag, Y_E_gauged, cmap='inferno', edgecolor='none')
ax2.set_title(f'Polyakov Worldsheet (S ≈ {polyakov_action_E:.2f})')
ax2.set_xlabel('σ')
ax2.set_ylabel('τ_E')
ax2.set_zlabel('Amplitude')
ax2.view_init(elev=30, azim=-60)

# 3. EFE Curvature from |Ψ|²
ax3 = fig.add_subplot(223, projection='3d')
ax3.plot_surface(X, T_grid, curvature, cmap='plasma', edgecolor='none')
ax3.set_title('Spacetime Curvature via EFE (Gμν ~ |Ψ|²)')
ax3.set_xlabel('x')
ax3.set_ylabel('t')
ax3.set_zlabel('Curvature')
ax3.view_init(elev=30, azim=-60)

# 4. Spherical Quantum Probability Density
ax4 = fig.add_subplot(224, projection='3d')
ax4.plot_surface(X_sph, Z_sph, prob_density_sph, cmap='coolwarm', edgecolor='none', alpha=0.9)
ax4.set_title('Spherical Quantum Density (n=3, l=2)')
ax4.set_xlabel('x')
ax4.set_ylabel('z')
ax4.set_zlabel('Probability Density')
ax4.view_init(elev=30, azim=-60)

plt.tight_layout()
plt.show()
