# wave_simulation

Simulation of the [wave equation](https://en.wikipedia.org/wiki/Wave_equation) in 2D in an inhomogenous medium, inhomogenous means that the speed of the wave changes depending on the position in the medium, e.g the propagation of sound in an oceanic environment or seismic activity. Motivation: This project is intended to be a learning experience for me.

[There is a interactive version of this simulation on my web page](https://sebastiankind.de/wave_simulation.html) (work in progress)

![Wave Propagating](plot2.png)


The simulation uses a 2D grid to model the behavior of waves as they propagate across an inhomogeneous medium. The key objective is to simulate how waves behave and observe emerging patterns. Meaning, where are they going, how are they reflecting, are there areas where the waves focus?


This is the 2D wave equation:

$$
\frac{\partial^2 u(x, y, t)}{\partial t^2} = c^2(x, y) \left( \frac{\partial^2 u(x, y, t)}{\partial x^2} + \frac{\partial^2 u(x, y, t)}{\partial y^2} \right)
$$

Where:
- $(u(x, y, t))$ is the wave field, representing the displacement of the medium at location $(x, y)$ and time $t$,
- $(c(x, y))$ is the wave speed being dependent on the location $(x, y)$, meaning it can change -> inhomogenous medium
- $(\frac{\partial^2}{\partial t^2})$ is the time second derivative,
- $(\frac{\partial^2}{\partial x^2})$ and $(\frac{\partial^2}{\partial y^2})$ are the spatial second derivatives.


The Wave Equation is a continuous PDE, that needs to be discretized first, in order to be simulated. We will be using a finite difference approximation for this. 
Discretization, aka the nifty math of turning the PDE into something approximated, that can be simulated on a big grid with a step size $(dx)$ and $(dy)$ in the $(x)$- and $(y)$-directions. 

Approximation of the spatial derivatives with a a second-order finite difference approximation:

$$
\frac{\partial^2 u(x, y, t)}{\partial x^2} \approx \frac{u(x + dx, y, t) - 2u(x, y, t) + u(x - dx, y, t)}{dx^2}
$$

$$
\frac{\partial^2 u(x, y, t)}{\partial y^2} \approx \frac{u(x, y + dy, t) - 2u(x, y, t) + u(x, y - dy, t)}{dy^2}
$$


Same thing with for the time derivatives

$$
\frac{\partial^2 u(x, y, t)}{\partial t^2} \approx \frac{u(x, y, t + dt) - 2u(x, y, t) + u(x, y, t - dt)}{dt^2}
$$

Where:
- $(dt)$ is the time step,
- $(dx)$ and $(dy)$ are the spatial step sizes.

Substitute the terms in the PDE waveequation with the discretized difference approximation (see above) and solve for $(u(...))$ to get the function for  the numerical update for earch point in the grid at time $(t+dt)$:


$$
u(x, y, t + dt) = 2u(x, y, t) - u(x, y, t - dt) + r^2 \left[ u(x + dx, y, t) + u(x - dx, y, t) + u(x, y + dy, t) + u(x, y - dy, t) - 4u(x, y, t) \right]
$$

Where $(r = \frac{c(x, y) \cdot dt}{dx})$ is the stability parameter that depends on the wave speed $(c(x, y))$ and the spatial resolution $(dx)$. Numerical stability is achieved by ensuring that $(r \leq 1)$, i.e., the Courant-Friedrichs-Lewy (CFL) condition must be satisfied, else the numerical stability will be unhappy :(


This formula can be implemented in Python to simulate the 2D wave.

```python
for i in range(1, Nx-1):  

        r_i = (c[i] * dt / dx) 
        u_new[i, 1:-1] = (2 * u[i, 1:-1] - u_old[i, 1:-1] + 
                          r_i**2 * (u[i+1, 1:-1] + u[i-1, 1:-1] + 
                                    u[i, 2:] + u[i, :-2] - 4 * u[i, 1:-1]))
```

The simulation also handles boundary conditions, where the waves are reflected.

I tried to implement Perfectly Matched Layer (short PML) to prevent wave reflections. Tho this not as simple as I thought it to be. I realize that waves still reflect no matter how I treat the boundary with a PML. I am still gradually learning. The reasoning behind PML let's us pretend that waves are leaving the simulation domain, simulating an open end to the wave field, where no reflections are expected, e.g. infinitely far range.



Problems:
- Numerical Instability: The numerical simulation may suffer from instabilities if the time step $(dt)$ or the spatial resolution $( dx, dy )$ are not chosen appropriately. The CLF condition must be followed to ensure stability in the wave propagation.

- Boundary Reflections: Reflection artifacts occur at the boundaries of the grid, but these reflections interfere with the wave propagation in the interior of the grid, creating unnatural interference patterns. I was trying to reduce reflections with a dampening of the waves close to the boundaries trying to implement a perfectly matched layer PML

- Perfectly Matched Layer (PML) is implemented to avoid these reflections, I am still seing numerical reflections at PML, i'd rather comment this part of the code

- Performance Issues: i mean the evaluation is slow, each "frame" is calculated in the update functions and runs the code execution through the UI. A smarter approach would first calculate all simulation values, and then run a smooth visualization in a video or gif


Good Ressources that helped:
- [the Wikipedia article about the wave eqation](https://en.wikipedia.org/wiki/Wave_equation)
- [Nils Berglund's presentation about boundary conditions ](https://www.youtube.com/watch?v=pN-gi_omIVE)
- your favorite LLM to get a quick starter on the math needed
- other helpful knowlege about Taylor series and Euler method or Runge-Kutta-method are helpful for the understanding of the math


![Initial Impulse](plot1.png)

The plot above shows the initial pulse

![Wave Propagating](plot2.png)

The second plot displays the **wave front** as it propagates inhomogeneous medium, the waves will bend accordingling, and converge to zones with a lower propagation speed

This little project achieved my goal of learning how the wave equation can be modeled. I did another project that uses ray tracing to simulate the refraction of waves in an inhomogeneous medium, especially to discover shadow zones with high damping in sonar applications. Future projects should solve the boundary conditions so waves can leave the simulation domain without any reflections or artifacts that keep interfering with the simulation.

I am interested in how these insights here can be scaled to the same problem for electromagnetic waves to simulate the radiation pattern of antennas in 3D.



Bonus:

Screenshot of the interactive wave simulation in JavaScript on my webpage

![Screenshot of the interactive wave simulation in JavaScript on my webpage](interactive_simulation.png)
[There is a interactive version of this simulation on my web page](https://sebastiankind.de/wave_simulation.html) (work in progress)
