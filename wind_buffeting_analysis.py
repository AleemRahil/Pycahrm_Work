import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

# Define the bridge geometry and material properties
L = 100.0 # length of the bridge in meters
b = 5.0 # width of the bridge in meters
h = 2.0 # height of the bridge in meters
rho = 7850.0 # density of steel in kg/m^3
E = 200.0e9 # elastic modulus of steel in Pa
mu = 0.3 # Poisson's ratio of steel

# Define the wind loading
v = 10.0 # wind velocity in m/s
rho_air = 1.23 # density of air in kg/m^3
Cp = 1.2 # pressure coefficient

# Define the finite element mesh
dx = 5.0 # element size in meters
nx = int(L / dx) # number of elements
x = np.linspace(0.0, L, nx+1) # node coordinates
conn = np.array([np.arange(nx), np.arange(1, nx+1)]).T # element connectivity

# Assemble the stiffness matrix
Ke = np.zeros((4, 4))
Ke[0, 0] = 12.0 * E * h**3 / (b*dx**3)
Ke[0, 2] = -6.0 * E * h**2 / (b*dx**2)
Ke[0, 3] = Ke[0, 1] = -Ke[0, 0]
Ke[1, 1] = 4.0 * E * h / (b*dx)
Ke[1, 3] = -Ke[1, 2] = -Ke[1, 1]
Ke[2, 2] = 2.0 * E * h / (b*dx)
Ke[2, 3] = -Ke[2, 2]
Ke[3, 3] = Ke[0, 0]

K = sp.lil_matrix((nx+1, nx+1))
for i in range(nx):
    K[conn[i, 0]:conn[i, 1]+1, conn[i, 0]:conn[i, 1]+1] += Ke

K = K.tocsr()

# Assemble the mass matrix
Me = np.zeros((4, 4))
Me[0, 0] = 156.0 * rho * h * dx / 420.0
Me[0, 2] = Me[2, 0] = 22.0 * rho * h * dx / 420.0
Me[0, 3] = Me[3, 0] = Me[1, 1] = 4.0 * rho * h * dx / 420.0
Me[1, 3] = Me[3, 1] = -Me[1, 2] = -Me[2, 1] = 13.0 * rho * h * dx / 420.0
Me[2, 2] = 156.0 * rho * dx * h / 420.0
Me[2, 3] = Me[3, 2] = Me[1, 2]
Me[3, 3] = 2.0 * rho * dx * h / 420.0

M = sp.lil_matrix((nx+1, nx+1))
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

A = M + dt2 * K
B = 2.0*M - dt2 * K
C = M - dt**2 * K

u = np.zeros((nx+1, nt))
u[:, 0] = u_static
u[:, 1] = u_static + dt*np.zeros(nx+1)

for i in range(2, nt):
    F_wind = Cp * 0.5 * rho_air * v**2 * h * dx * np.array([1.0, 0.0, 1.0, 0.0])
    F_dynamic = B.dot(u[:, i-1]) - C.dot(u[:, i-2]) + F_wind
    F_dynamic[bc] = 0.0
    u[:, i] = spla.spsolve(A, F_dynamic)

# Compute the displacement and velocity time histories
t = np.linspace(0.0, T, nt)
displacement = u[1, :]
velocity = (u[1, 1:] - u[1, :-1]) / dt