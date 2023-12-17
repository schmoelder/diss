(model_solution)=
# Solution of chromatographic process models

The chromatographic models introduced in {numref}`section %s<model_formulation>` form systems of partial differential equations (PDE) or partial differential algebraic equations (PDAE) in space and time.
While highly detailed models that incorporate numerous transport effects can provide accurate approximations of chromatographic separation, they often demand substantial computational resources, even with modern software and hardware {cite}`Puettmann2015`.
However, it is often possible to achieve accurate results with less detailed models, which can significantly reduce computational costs.
This is particularly beneficial when multiple simulations need to be performed for purposes like parameter estimation or optimization.
Using simpler models, which include only essential components, can also prevent overfitting and enhance the interpretability of the model.
Moreover, it's crucial to consider that more complex models may involve a larger number of parameters, which can be challenging to measure or estimate accurately {cite}`Heymann2022`.
Therefore, it is generally recommended to select the simplest model that can accurately describe the specific separation problem at hand.

(analytical_solutions)=
## Analytical solutions

For the calculation of concentration profiles of chromatographic processes, a closed-form analytic solution would generally be desirable since it allows for an accurate and fast computation.
However, such analytic solutions are limited to specific models and rely on very restrictive, simplifying assumptions.
For example, the equilibrium model can be solved analytically for the linear isotherm, as well as the multicomponent Langmuir isotherm {cite}`SchmidtTraub2020`.
Additionally, Fechtner et al. have demonstrated a semi-analytical approach applicable any implicit isotherm model in the equilibrium model {cite}`Fechtner2017`.
But also more complicated models can be solved analytically when a linear adsorption isotherm is assumed {cite}`Qamar2014,Leweke2021`.
However, these restrictions limit their applicability for a general purpose modeling tool.
Consequently, numerical approaches to approximate the solution of the chromatographic models are commonly used.

It is important to note that analytical solutions are still very useful, even in the context of numerical simulation tools.
They can serve as benchmark and test cases to validate the implementation of numerical schemes (see also {numref}`software_tests`).
For example, [CADET-Semi-analytic](https://github.com/modsim/CADET-semi-analytic) computes reference solutions of the general rate model with proven error bounds using analytical solutions in the Laplace domain and numerical inversion {cite}`Leweke2016`.
Although this method is only applicable for the linear isotherm, due to the modular nature of the CADET-Core code, binding models make up only for a fraction of the overall source code.
Consequently, all other aspects of the code can still be validated, including convection, diffusion, and networks of unit operations.

(numerical_solutions)=
## Numerical solution

To estimate a numerical approximation to the solution of the model equations, the method of lines is commonly applied.
First, the spatial coordinates are discretized, resulting in a system of ordinary differential equations (ODEs) or differential algebraic equations (DAEs), depending on the isotherm being used.
Next, the system is discretized in time using either explicit or implicit methods.

Generally, the finer the grid used to discretize the continuous space-time domain, the closer the approximation will be to the exact solution.
However, this comes at the cost of increased computational effort.
To analyze the performance of a numerical solution method, the order of convergence is examined.
Convergence order is a measure of the rate at which a numerical solution method approaches the exact solution as the grid size is increased.
However, methods with higher convergence orders may demand more computational resources per grid point.
Moreover, it's worth noting that convergence order is generally only reached asymptotically with an increase in degrees of freedom (DOFs).
Nonetheless, utilizing numerical methods with high convergence orders is recommended for achieving accurate and efficient solutions for chromatographic models.
These higher-order methods often come with other advantageous properties, such as better stability {cite}`Atkinson2011`.

Several numerical methods have successfully been applied to solve chromatographic models.
In the following, an overview is given on selected methods which are currently used in state-of-the-art simulation software.
First, different approaches for the spatial semi-discretization are discussed, followed by an overview off methods for time integration.

(spatial_discretization)=
### Spatial discretiation

% Finite Difference
The finite difference method (FDM) is based on Taylor's theorem.
Here, a Taylor series is used to replace the spatial differentials with discrete difference quotients.
For instance, the spatial first-order forward finite difference is derived by approximating the derivative at a point $z_i$ by

```{math}
:label: finite_difference_scheme

\frac{\partial c(z_i)}{\partial z} \approx \frac{c(z_i+\Delta z) - c(z_i)}{\Delta z}
```

where $\Delta z$ is the grid spacing.
The FDM has been widely used due to its simplicity and efficiency for problems with smooth solutions.
To achieve higher accuracy, more neighboring points can be used in higher order schemes.

A well-known first order FDM scheme is the forward-backward method by Rouchon et al {cite}`Rouchon1987`.
It solves the EDM equations by neglecting the dispersion term in the FDM formulation and using the second-order truncation error to approximate the apparent dispersion.
Although this numerical scheme is straightforward, it can result in a large ODE system due to the relatively fine grid required for accurate approximations if dispersion is low {cite}`SchmidtTraub2020`.
Moreover, it can suffer from numerical dispersion and instability for problems with steep gradients or high-frequency oscillations.
It is important to note that FDM is usually not mass conservative.
**Another drawback is the treatment of boundary conditions: We are limited to low order at boundaries [@jan: what does this mean?]**

% Finite Volume
In contrast to the FDM, which computes the solution at discrete points, finite volume schemes (FV) define a grid of cells that give a constant value for each conservative variable inside the cell.
For instance, in the case of chromatographic models, the interstitial concentrations are spatially averaged in $j \in \{ 0, \dots, N_{z} - 1 \}$ uniform cells with grid spacing $\Delta z = L/N_z$.
This leads to a staircase function defining a local Riemann problem at each cell interface {cite}`Guiochon2006`.
The flux at these interfaces is approximated by a feasible numerical flux function $F$ leading to the following semi-discretized formulation (in 1D):

```{math}
\frac{d c_j(t)}{d t} \approx \frac{1}{\Delta z} (F(c_{j-1}, c_j) - F(c_j, c_{j+1}))
```

for each control volume $j \in \{ 0, \dots, N_{z} - 1 \}$, with c_{-1}, c_{N_z} given by boundary conditions.

This procedure is naturally conservative and monotonicity preserving {cite}`Blazek2015,Koren1993`.
High-order FV schemes adjust the control volumes by higher order (e.g. polynomial) reconstruction using the information provided by a stencil of control volumes.
This preserves mass conservation but comes at the cost of the monotonicity property.
Every linear high-order scheme suffers from oscillations at steep gradients, since they cannot be monotone {cite}`Godunov1959`.
To overcome this problem, a nonlinear mechanism can be built into the reconstruction, such as a slope limiter {cite}`Blazek2015`, or a weighted essentially non-oscillatory (WENO) scheme {cite}`Lieres2010`.
The latter is currently implemented in **CADET** and used for this work {cite}`Leweke2018`.

% Finite Elements Method
The finite element method (FEM) divides the spatial domain into cells, similar to FV.
However, FEM introduces a polynomial of arbitrary order for each cell, allowing for high accuracy with a comparably low number of cells if the solution is sufficiently smooth {cite}`SchmidtTraub2020`.

The classical FEM approach, known as the continuous Galerkin method (CG), conditions cell interfaces to be continuous, leading to a tightly coupled ODE system.
This method presents some drawbacks, such as not naturally being conservative, challenges retaining higher order at boundaries **(das stimmt glaube ich nur fuer bestimmte stabilisierte varianten, das originale schema benutzt denke ich einfach nur den Wert der boundary condition [@jan: what does this mean?])**, and being generally more complicated than FV.
Nonetheless, this approach is currently used in Cytiva's commercial GoSilico™ Chromatography Modeling Software {cite}`gosilico` **wobei die auch eine stabilisierte variante benutzen** [@jan wie würdest du das beschreiben?].

In contrast, the discontinuous Galerkin approach (DG) allows discontinuous cell interfaces, making it a combination of FV and FEM.
This allows for a feasible numerical flux to solve the local Riemann problem, which adds numerical dispersion to the scheme.
This additional artificial dispersion is considered beneficial due to its stabilizing effects {cite}`Brezzi2006` which reduces oscillations.
While the DG has some drawbacks when compared to CG, such as a larger state vector due to the discontinuous cell boundaries, its stabilizing properties as well as a generally easier integration of boundary conditions compensate for these downsides.
Recent work has shown that DG can be highly performant in terms of computational speed and is hence currently actively being researched {cite}`Meyer2020`.
**Bei FE koenntest du noch sagen, dass wir im gegensatz zu FV und FD nicht durch die boundary conditions auf eine Konvergenzordnung limitiert sind sondern arbitrary order polynome auch arbitrary order Konvergenz heissen [asymptotisch und solange keine echte Diskontinuität auftritt; bei steilen Gradienten tritt die high order Konvergenz auch erst spaeter ein](@jan: what does this mean?)**

(time_integration)=
### Time integration

As previously mentioned, the spatial semi-discretization of the underlying equations leads to a system of coupled ODEs or DAEs in time.
For the time integration, implicit as well as explicit schemes exist.

Explicit schemes yield an explicit formulation for the future state depending solely on known states of the system.
Consequently, the computation can be performed relatively quickly.
The most straightforward example of an explicit time integration scheme is the explicit Euler method.
In this method, the current state of the system and its derivative are used to project the system into the future.
The next state of the system is then obtained by stepping forward in time by a small time increment.
The explicit Euler method is a first-order method.
Among the most popular explicit methods is the Runge-Kutta (RK) family which can be constructed to yield higher order with further beneficial properties such as low storage requirements {cite}`Carpenter1994`.

However, all explicit methods are limited by the step size in order to maintain numerical stability and accuracy.
Therefore, explicit methods are generally less suitable for stiff problems, such as those encountered in chromatography, where steep gradients can occur due to discontinuous injections or even self-sharpening effects of nonlinear isotherms.
These effects demand very small step sizes for explicit methods to retain stability which increases the computational cost.
In these cases, implicit methods are usually preferred.

Implicit methods, on the other hand allow for larger time step sizes for stiff problems since time step sizes are only limited by accuracy (and not by stability).
Unlike explicit methods, implicit methods result in an algebraic system of equations that needs to be solved, making them computationally more expensive per time step.
However, due to the aforementioned stiffness inherent to chromatographic separation models, the larger time steps usually outweigh this downside.
Backwards differentiation formula (BDF) methods use a polynomial approximation of the solution that is based on the current state and (several) past time steps {cite}`Atkinson2011`.
Higher order BDF methods can be constructed to improve computational efficiency.
Additionally, adaptive time stepping can be used with both Runge-Kutta and BDF methods to dynamically adjust the time step size based on the stiffness of the problem, further improving the accuracy and efficiency of the simulation.

## Solution of the system of unit operations

Before the model equations of a unit operation can be solved, their inlet profiles coming from previous units upstream (i.e. their boundary conditions) need to be known.
For acyclic connections, the profiles can simply be calculated by starting from the system inlets and sequentially solving all units downstream.
In contrast, systems with internal recycles need to be solved simultaneously because the outlet of one unit can directly influence its own input.
This can be achieved by a Newton iteration which requires the Jacobians of the unit operations and the connectivity configuration which couples the unit operations.
Then, for each unit operation the outlet is computed and using these values, the inlet profiles are updated and the unit operations are solved again.
This procedure is iterated until the system is fully solved.
