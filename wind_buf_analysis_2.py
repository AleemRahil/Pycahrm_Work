import numpy as np
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
conn = np.zeros((nx, 2), dtype=np.int32)
for i in range(nx):
    conn[i, 0] = i
    conn[i, 1] = i + 1

K = np.zeros((nx+1, nx+1))
Me = np.zeros((2, 2))
Me[0, 0] = Me[1, 1] = 2.0
Me[0, 1] = Me[1, 0] = 1.0
Me *= dx/6.0

for i in range(nx):
    K[conn[i, 0]:conn[i, 1]+1, conn[i, 0]:conn[i, 1]+1] += E*I/dx * np.array([[1.0, -1.0], [-1.0, 1.0]])
    K[conn[i, 0]:conn[i, 1]+1, conn[i, 0]:conn[i, 1]+1] += rho*A/dt**2 * Me

M = np.zeros((nx+1, nx+1))
for i in range(nx):
    M[conn[i, 0]:conn[i, 1]+1, conn[i, 0]:conn[i, 1]+1] += Me

M = M.tocsr()

# Define the boundary conditions
bc = np.array([0, nx], dtype=np.int32) # fixed at both ends

# Solve the static problem
F_wind = Cp * 0.5 * rho_air * v**2 * h * dx * np.array([1.0, 0.0, 1.0, 0.0]) # nodal wind forces
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
u[:, 1] = u_static + dt*np.zeros(nx+1)

for i in range(2, nt):
    F_wind = Cp * 0.5 * rho_air * v**2 * h * dx * np.array([1.0, 0.0, 1.0, 0.0]) # nodal wind forces
    F_dynamic = np.zeros(nx+1)
    F_dynamic[1:-1] = F_wind[2:] + F_wind[:-2] # nodal dynamic forces
    F_dynamic[bc] = 0.0 # apply boundary conditions

    u[:, i] = spla.spsolve(A, B.dot(u[:, i-1]) - C.dot(u[:, i-2]) + F_dynamic)

# Compute the maximum displacement for each node
max_disp = np.max(u, axis=1)

# Plot the maximum displacement as a function of position
x = np.linspace(0, L, nx+1)
plt.plot(x, max_disp)
plt.xlabel('Position (m)')
plt.ylabel('Maximum displacement (m)')
plt.title('Wind buffeting analysis of bridge')
plt.show()

