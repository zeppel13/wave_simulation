# Sebastian Kind 2025
# this project started at the CERN Art and Science Conference, as a visualization of different FDM wave models


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


c0 = 3.0 #reference wave speed

# Dimension of Grid, 100, 100 is good for fast checks
# 400, 800 works on my Laptop
Nx, Ny = 400, 800  
dx = dy = 0.5  #rather magic trial-and-error parameter


x = np.linspace(0, Nx-1, Nx)
x = np.linspace(0, Nx-1, Nx)  # x-coordinate

## Parameter of the SSP = Sound Speed Profile
# I want to super impose 2 different linear function with a minimum
# in the middle to roughly approximate oceanic conditions for a SOFAR Channel

# minium position
x_min = Nx // 4  # remember: integer division, bc those values will be indices

# really this doesn't work, but still gives a good enough SSP
c_min = 1  #Minimum speed at x_min
c_max = 3  #Maximum speed at edges

# Linear functions that create a V-shape centered at x_min
c1 = (c_max - c_min) * (1 + np.abs(x - x_min) / (Nx//2))
c2 = (c_max - c_min) * (1 + np.abs(x - x_min) / (Nx//2))

# Total sound speed profile
c = c1 + c2 + c_min  # Ensuring minimum is at c_min

# Prevent values below c_min
c = np.maximum(c, c_min)  
#print(c)

# Initialize wave grids
u = np.zeros((Nx, Ny))      # current wave state, this is what will be plotted
u_old = np.zeros((Nx, Ny))  # previous time step, needed for discretized PDE/FDM calculation
u_new = np.zeros((Nx, Ny))  # next time step, we are going to calculate this, and then swap all values with u and u_old

#initial disturbance at the center
# cx, cy = Nx//4,  3*Ny // 4  #position
# u[cx, cy] = 2  #pulse by indexing

dt = 0.7 * dx / np.max(c)
r = (c0 * dt / dx)  #CFL stability parameter, this need some playing aroung with the parameters


# smooth guassian disturbance, the decrease numerical artifacts, reducing harsh changes
cx, cy =  Nx // 6, 8* Ny // 9  #center of 2d gaussian
sigma = .1  # sigma controls the width of the pulse
A = 1  # amplitude of the pulse, how high, or what color the pulse will have on the heat map

# loop over coordinates and draw the gaussiang pulse over the initial wave
for i in range(Nx):
    for j in range(Ny):
        u[i, j] = A * np.exp(-((i - cx)**2 + (j - cy)**2) / (2 * sigma**2)) 

# Set up the figure for animation
#fig, ax = plt.subplots()
#fig, ax = plt.subplots(1, 2, figsize=(12, 6))
fig, ax = plt.subplots(1, 2, figsize=(12, 6), gridspec_kw={'width_ratios': [4, 1]})
im = ax[0].imshow(u, cmap="inferno", origin="upper", vmin=-0, vmax=0.05)

ax[1].plot(c, x, label='Sound Speed Profile')
ax[1].set_title('Sound Speed Profile')
ax[1].set_xlabel('Sound Speed (c)')
ax[1].set_ylabel('Depth')
ax[1].invert_yaxis()  #y-axis should point downwards
ax[1].set_xlim(min(c), max(c))  #scaling of the speed value
ax[1].grid(True)


# I have very low certainty about which PML parameters are right here
pml_thickness = 25  #thickness of PML in gridpoints
sigma_max = 0.005   #maximum damping factor
pml_decay = 0.0015  #decay rate for the damping

# pml_damping is a bit tricky, and i havn't figured out the right parameters yet
def pml_damping(i, max_val, thickness, decay):
    # Function to create a smooth exponential damping layer
    distance = min(i, max_val - i)  # Distance to the boundary
    damping = np.exp(-decay * (distance / thickness)**2)  # Exponential decay based on distance
    return damping


def update(frame):
    global u, u_old, u_new
    
    for i in range(1, Nx-1):  #range over all x, the calculations are applied to numpy arrays(vectors) for all vertical columns of the simulation

        r_i = (c[i] * dt / dx) #no forgetti, the value of the stability condition contains our position dependant speed 
        
        #This is the magic of the whole script:
        #here we update the wave field (u_new) with the calculation of the discretized PDE
        u_new[i, 1:-1] = (2 * u[i, 1:-1] - u_old[i, 1:-1] + 
                          r_i**2 * (u[i+1, 1:-1] + u[i-1, 1:-1] + 
                                    u[i, 2:] + u[i, :-2] - 4 * u[i, 1:-1]))

        #horizontal damping
        if i < pml_thickness:
            damping_left = pml_damping(i, Nx, pml_thickness, pml_decay)
            u_new[i, 1:-1] *= damping_left  # Apply gradual damping for left boundary

        if i > Nx - pml_thickness:
            damping_right = pml_damping(i, Nx, pml_thickness, pml_decay)
            u_new[i, 1:-1] *= damping_right  #right boundary

        #vertical damping
        if i < pml_thickness:
            damping_top = pml_damping(i, Ny, pml_thickness, pml_decay)
            u_new[i, :] *= damping_top  #top boundary

        if i > Ny - pml_thickness:
            damping_bottom = pml_damping(i, Ny, pml_thickness, pml_decay)
            u_new[i, :] *= damping_bottom #bottom boundary

    #explanation: here we are swapping the values of our state of right now, with the previous one
    u_old[:], u[:] = u[:], u_new[:]
    
    
    im.set_array(u)
    return [im]




#voila do the animaion
ani = animation.FuncAnimation(fig, update, frames=200, interval=30, blit=True)

plt.show()
