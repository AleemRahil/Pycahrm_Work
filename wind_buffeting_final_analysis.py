import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
import matplotlib.pyplot as plt

# Define the parameters of the bridge and wind loading
L = 100.0 # length of bridge in meters
nx = 100 # number of elements
dx = L / nx # element length
h = 5.0 # height of bridge deck in meters
b = 10.0 # width of bridge deck in meters
rho = 2500.0 # mass density of bridge deck in kg/m^3
E = 2.0e11 # modulus of elasticity of bridge deck in Pa
I = b*h**3/12 # second moment of area of bridge deck
v = 30.0 # wind speed in m/s
rho_air = 1.225 # air density in kg/m^3
Cp = 1.0 # wind pressure coefficient

# Define the finite element model
conn = np.column_stack((np.arange(nx), np.arange(1, nx+1)))
K = sp.csr_matrix((nx+1, nx+1))
Me = np.array([[2., 1.], [1., 2.]]) * dx / 6.0
for i in range(nx):
    indices = conn[i]
    K[indices, indices] += E*I/dx * np.array([[1., -1.], [-1., 1.]])
    K[indices, indices] += rho*b*h/dt**2 * Me

M = sp.csr_matrix((nx+1, nx+1))
for i in range(nx):
    indices = conn[i]
    M[indices, indices] += Me

# Define the boundary conditions
bc = np.array([0, nx], dtype=np.int32) # fixed at both ends

# Solve the static problem
F_wind = Cp * 0.5 * rho_air * v**2 * h * dx * np.array([1., 0., 1., 0.]) # nodal wind forces
F_static = np.zeros(nx+1)
F_static[1:-1] = F_wind[2:] + F_wind[:-2] # nodal static forces
F_static[bc] = 0.0 # apply boundary conditions
u_static = spla.spsolve(K, F_static)

# Solve the dynamic problem
dt = 0.001 # time step size in seconds
T = 10.0 # total simulation time in seconds
nt = int(T / dt) # number of time steps

A = M + dt**2 * K
B = 2.0*M - dt**2 * K
C = M - dt**2 * K

u = np.zeros((nx+1, nt))
u[:, 0] = u_static
u[:, 1] = u_static

# Solve the dynamic problem
dt = 0.001  # time step size in seconds
T = 10.0  # total simulation time in seconds
nt = int(T / dt)  # number of time steps

A = M + dt ** 2 * K
B = 2.0 * M - dt ** 2 * K
C = M - dt ** 2 * K

u = np.zeros((nx + 1, nt))
u[:, 0] = u_static
u[:, 1] = u_static


# Define the dynamic wind loading
def wind_load(t):
    return Cp * 0.5 * rho_air * v ** 2 * h * dx * np.array(
        [1.0, np.sin(2 * np.pi * t / T), 1.0, np.sin(2 * np.pi * t / T)])


# Iterate over time steps to solve for u
for i in range(1, nt):
    # Compute the dynamic load vector
    F_dynamic = wind_load(i * dt)
    F = B.dot(u[:, i - 1]) - C.dot(u[:, i - 2]) + dt ** 2 * F_dynamic
    F[bc] = 0.0  # apply boundary conditions

    # Solve for u at the current time step
    u[:, i] = spla.spsolve(A, F)

# Plot the results
x = np.linspace(0.0, L, nx + 1)
for i in range(nt):
    plt.plot(x, u[:, i])
plt.xlabel('Position (m)')
plt.ylabel('Displacement (m)')
plt.title('Dynamic Response of Bridge to Wind Loading')
plt.show()