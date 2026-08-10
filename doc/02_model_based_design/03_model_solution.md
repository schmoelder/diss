(model_solution)=
# Solution of chromatographic process models
The chromatographic models introduced in {numref}`model_formulation` consist of systems of partial differential equations (PDEs) or partial differential-algebraic equations (PDAEs) in space and time.
While highly detailed models that account for numerous transport effects can provide highly accurate approximations of chromatographic separation, they often require substantial computational resources, even with modern software and hardware {cite}`Puettmann2015`.
However, it is often possible to achieve accurate results with simpler models, which focus on capturing only the essential transport and interaction phenomena necessary to describe the process accurately.
For example, simplified models may neglect minor effects that have minimal influence on the outcome, reducing complexity while retaining predictive power.
This approach is particularly advantageous in scenarios requiring multiple simulations, such as parameter estimation or process optimization, where computational efficiency is critical.


(analytical_solutions)=
## Analytical solutions

For calculating concentration profiles in chromatographic processes, closed-form analytical solutions are highly desirable because they allow for accurate and fast computations.
However, such analytical solutions are limited to specific models and rely on restrictive simplifying assumptions.
For example, the equilibrium model can be solved analytically for the linear isotherm, as well as for the multicomponent Langmuir isotherm {cite}`SchmidtTraub2020`.
Moreover, Fechtner et al. have demonstrated a semi-analytical approach applicable to any implicit isotherm model in the equilibrium model {cite}`Fechtner2017`.

Additionally, even more complex models can be solved analytically when a linear adsorption isotherm is assumed {cite}`Qamar2014,Leweke2021`.
Moment analysis provides a further analytical route, deriving integral characteristics such as retention time and peak variance without evaluating the concentration profile, which makes it widely used for initial parameter determination {cite}`Guiochon2006`.
However, the restrictive assumptions required for these solutions limit their utility as general-purpose modeling tools, and numerical approaches are commonly employed to approximate the solutions of chromatographic models.

Despite their limitations, analytical solutions remain valuable in the context of chromatography.
They can serve as benchmark and test cases to validate the implementation of numerical schemes (see also {numref}`software_tests`).
For instance, the [CADET-Semi-analytic](https://github.com/modsim/CADET-semi-analytic) framework computes reference solutions for the general rate model with proven error bounds using analytical solutions in the Laplace domain combined with numerical inversion {cite}`Leweke2016`.
Although this method is restricted to the linear isotherm, it is particularly useful due to the modular nature of CADET-Core.
Here, binding models represent only a small fraction of the overall source code.
As such, analytical solutions can still validate critical aspects of the code, including convection, diffusion, and networks of unit operations.
To validate the connectivity and dynamic events of the operating modes described later in this work, equilibrium theory for single columns is applied (see {numref}`equilibrium_model`) to determine propagation velocities and corresponding elution times {cite}`SchmidtTraub2020`.
The general principle for advanced operating modes is to track how far each component front would have traveled at the time points corresponding to key process events, such as the end of a recycling phase, a valve switch, or a re-injection.
From these positions, the outlet concentration profiles are reconstructed analytically.
While the specific logic differs per operating mode (recycling, flip-flop, serial columns), the underlying approach is the same: propagation velocities determine component positions at each event, and the outlet profile is assembled from the resulting concentration fronts.
These ideal chromatograms are then compared to the numerical solutions obtained from CADET-Core.

For the equilibrium model with nonlinear isotherms, propagation velocities of concentration fronts can be derived analytically using the method of characteristics {cite}`SchmidtTraub2020`.
Using the chain rule, the time derivative of the solid phase concentration can be expressed in terms of the isotherm slope and the liquid phase time derivative:

```{math}
:label: solid_phase_derivative_chain_rule

\frac{\partial c^s_i}{\partial t} = \left. \frac{\text{d} c^s_i}{\text{d} c^b_i} \right|_{c^{b,+}_i} \cdot \frac{\partial c^b_i}{\partial t}.
```

Rearranging eq. {eq}`mass_balance_em` and substituting eq. {eq}`solid_phase_derivative_chain_rule` yields the propagation velocity $w(c^{b,+}_i)$
of a concentration front $c^{b,+}_i$:

```{math}
:label: propagation_velocity

w(c^{b,+}_i) = \frac{u}{1 + F \cdot \left. \frac{\text{d} c^s_i}{\text{d} c^b_i} \right|_{c^{b,+}_i}}.
```

By considering the column length $L_c$, the retention time $t_{\text{R},i}(c^{b,+}_i)$ can be derived as:

```{math}
:label: retention_time

t_{\text{R},i}(c^{b,+}_i) = \frac{L_c}{w(c^{b,+}_i)} = t_{0,t} \cdot \left( 1 + F \cdot \left. \frac{\text{d} c^s_i}{\text{d} c^b_i} \right|_{c^{b,+}_i} \right),
```
where $t_{0,t} = L_c / u$ is the column dead time.
For a linear isotherm, where $\frac{\text{d} c^s_i}{\text{d} c^b_i} = a_i$ (Henry coefficient), this simplifies to:

```{math}
:label: retention_time_linear

t_{\text{R,lin},i} = t_{0,t} \cdot \left( 1 + F \cdot a_i \right).
```

(numerical_solutions)=
## Numerical solution

Where analytical solutions are unavailable, numerical approaches approximate the solution of the model equations and can be applied to more complex model formulations.
They differ in how they represent or discretize the underlying continuous transport equations.
Plate and cell models postulate a cascade of equilibrium stages as the model itself and thus yield an ODE system without an intermediate partial differential equation.
This construction can also be interpreted as a low-order discretization of the transport equations, with the number of stages controlling the effective axial dispersion {cite}`SchmidtTraub2020`.

In contrast, for models formulated in terms of continuous transport equations, the method of lines is commonly applied.
It discretizes space first while leaving time continuous, allowing the spatial discretization and the time integrator to be chosen independently.
This also provides access to established adaptive integrators for stiff ODE and DAE systems, which is important here because transport processes and fast adsorption kinetics can act on widely separated time scales.

The spatial semi-discretization transforms the governing equations into a system of ordinary differential equations (ODEs) or differential-algebraic equations (DAEs), depending on the model formulation and the algebraic constraints it contains.
The resulting system is then integrated in time using an explicit or implicit time-integration method.

Provided the discretization is consistent and stable, refining the grid reduces the discretization error, although at the cost of increased computational effort.
The performance of a numerical method is often characterized by its order of convergence, which describes how rapidly the numerical solution approaches the exact solution as the grid is refined {cite}`Atkinson2011`.
Higher-order methods can reduce the discretization error more rapidly and may therefore attain a prescribed accuracy with fewer grid points, but can require greater computational effort per degree of freedom.
The theoretical convergence order is, however, an asymptotic property and is typically observed only once the grid is sufficiently fine for the expected error behavior to emerge.
On coarser grids, other error contributions may dominate, such that a higher formal order does not necessarily result in a more accurate solution.
The practical advantage of higher-order methods therefore depends on the required accuracy, the characteristics of the solution, and the associated computational cost.

Several numerical methods have been successfully applied to chromatographic models.
The following sections provide an overview of commonly used methods in established chromatography simulation software.
First, different approaches for spatial semi-discretization are discussed, followed by an overview of methods for time integration.


(spatial_discretization)=
### Spatial discretization

% Finite Difference
The finite difference method (FDM) is based on Taylor's theorem, where a Taylor series is used to replace spatial derivatives with discrete difference quotients.
For example, the spatial first-order forward finite difference is derived by approximating the derivative at a point $z_n$ as:

```{math}
:label: finite_difference_scheme

\frac{\partial c(z_n)}{\partial z} \approx \frac{c(z_n+\Delta z) - c(z_n)}{\Delta z},
```

where $\Delta z$ is the grid spacing.

FDM is widely used due to its simplicity and computational efficiency, especially for problems with smooth solutions.
To achieve higher accuracy, higher-order schemes can incorporate additional neighboring points.

The FDM has several limitations, however.
One challenge is numerical dispersion, an artifact of the discretization that can distort sharp gradients or high-frequency oscillations in the solution.
The well-known forward-backward method by Rouchon et al. {cite}`Rouchon1987` deliberately exploits this truncation error to approximate physical dispersion in the EDM, avoiding explicit discretization of the dispersion term.
However, this is a controlled approximation and compromises accuracy for low axial dispersion coefficients or steep concentration fronts, where the numerical and physical dispersion differ significantly, and can result in large ODE systems when a fine grid is required {cite}`SchmidtTraub2020`.
Additionally, FDM is not inherently mass-conservative, meaning the total mass in the system may not be preserved, which can lead to accumulated errors in multicomponent systems or long-duration simulations.
Despite these drawbacks, FDM remains widely used, as its simplicity and efficiency make it a practical choice for many applications.


% Finite Volume
Unlike FDM, which computes solutions at discrete points, the finite volume method (FVM) defines a grid of cells and computes spatially averaged values within each cell.
For chromatographic models, interstitial concentrations are averaged over $n \in \{ 0, \dots, N_z - 1 \}$ uniform cells with a grid spacing $\Delta z = L_c / N_z$.
This results in a staircase representation of the solution and defines a local Riemann problem at each cell interface {cite}`Guiochon2006`.
The flux across these interfaces is approximated using a numerical flux function $\mathcal{F}$, yielding the following semi-discretized formulation in 1D:

```{math}
:label: finite_volume_semi_discretized

\frac{d c_{n}(t)}{d t} \approx \frac{1}{\Delta z} (\mathcal{F}(c_{n-1}, c_{n}) - \mathcal{F}(c_{n}, c_{n+1})),
```

for each control volume $n \in \{ 0, \dots, N_{z} - 1 \}$, with $c_{-1}$ and $c_{N_z}$ given by boundary conditions.

FVM offers key advantages over FDM, particularly due to its intrinsic conservation properties, ensuring that mass is preserved across cell interfaces.
Mass conservation is especially important in chromatographic models, where errors in the total mass balance directly affect predicted yield and purity.
Additionally, FVM is monotonicity-preserving, which prevents unphysical oscillations in the solution, making it well-suited for problems involving sharp concentration gradients {cite}`Blazek2015,Koren1993`.
To achieve higher accuracy, the finite volume method (FVM) can employ polynomial reconstructions to approximate values within each control volume using information from neighboring cells.
This stencil-based reconstruction enables high-order schemes that preserve mass conservation.
However, as described by Godunov's theorem, linear high-order schemes cannot maintain monotonicity, resulting in oscillations near steep gradients {cite}`Godunov1959`.
To address this issue, nonlinear reconstruction techniques are commonly applied, such as slope limiters {cite}`Blazek2015` or weighted essentially non-oscillatory (WENO) schemes.
The WENO scheme works by adaptively selecting between multiple polynomial reconstructions based on local smoothness, using lower-order approximations near discontinuities and higher-order ones in smooth regions.
Given its ability to handle steep concentration fronts without sacrificing accuracy in smooth regions, the WENO scheme is implemented in CADET-Core and applied throughout this work {cite}`Lieres2010,Leweke2018`.

% Finite Elements Method
The finite element method (FEM) divides the spatial domain into cells, similar to the FVM.
However, FEM introduces a polynomial of arbitrary order for each cell, enabling high accuracy with a relatively low number of cells, provided the solution is sufficiently smooth {cite}`SchmidtTraub2020`.
The classical FEM approach, known as the continuous Galerkin (CG) method, enforces continuity across cell interfaces, resulting in a tightly coupled system of ODEs.
This method, however, has several drawbacks.
Unlike FVM, FEM does not guarantee that fluxes balance across cell interfaces, which can lead to violations of mass conservation.
Additionally, retaining high-order accuracy at boundaries can be difficult, and the implementation is generally more complex compared to FVM.
Nonetheless, CG is currently implemented in Cytiva's commercial GoSilico™ Chromatography Modeling Software, where a streamline-upwind Petrov-Galerkin stabilization (SUPG) technique is applied to improve numerical stability {cite}`Hahn2015`.
In contrast to CG, the discontinuous Galerkin (DG) method allows for discontinuities at cell interfaces, combining elements of FVM and FEM.
This flexibility permits the use of numerical fluxes to solve the local Riemann problem, introducing artificial numerical dispersion into the scheme.
Unlike in FDM, this artificial dispersion is considered beneficial in DG, as it provides stabilizing effects that reduce oscillations, particularly for systems with steep gradients {cite}`Brezzi2006`.
While DG has some disadvantages compared to CG, such as a larger state vector due to the discontinuous cell boundaries, these are outweighed by its stabilizing properties and the simpler integration of boundary conditions.
Recent studies have demonstrated that DG can achieve high computational performance, making it a promising area of ongoing research {cite}`Meyer2020, Breuer2023, Frandsen2025`.
The DG method is not employed in this work; the WENO-FVM scheme implemented in CADET-Core was found sufficient for the problems considered here.

(time_integration)=
### Time integration

As previously discussed, the spatial semi-discretization of the underlying equations transforms them into a system of coupled ODEs or differential-algebraic equations (DAEs) in time.
For time integration, both explicit and implicit schemes are available, each with distinct advantages and limitations.

Explicit methods provide a formulation for the future state of the system that depends only on its current state and known derivatives.
This makes explicit schemes computationally efficient per time step.
The most straightforward example is the explicit Euler method, which projects the system into the future using the current state and its derivative, stepping forward by a small time increment.
The explicit Euler method is a first-order method, but higher-order methods such as the Runge-Kutta (RK) family can be applied {cite}`Carpenter1994`.
However, explicit methods are limited by stability constraints on the step size, especially for stiff problems.
In chromatography, stiffness arises from steep gradients caused by discontinuous injections or self-sharpening effects of nonlinear isotherms.
To ensure stability and accuracy, explicit methods require very small time steps for such problems, significantly increasing computational costs.
As a result, explicit methods are generally less suitable for chromatographic models, and implicit methods are usually preferred in these cases.

Implicit methods, unlike explicit ones, allow for larger time step sizes even for stiff problems.
This is because their stability depends on accuracy rather than being constrained by the step size.
At each time step, implicit methods result in an algebraic system of equations that must be solved, making them computationally more expensive per step.
However, due to the inherent stiffness in chromatographic separation models, the ability to use larger time steps typically outweighs this computational cost, leading to greater overall efficiency.
A widely used family of implicit methods is the backward differentiation formula (BDF) methods, which approximate the solution using polynomials based on the current state and several past time steps {cite}`Atkinson2011`.
Higher-order BDF methods can improve computational efficiency by reducing the number of time steps required to achieve a given level of accuracy.

Additionally, adaptive time stepping can be applied with both Runge-Kutta and BDF methods.
This technique dynamically adjusts the time step size based on the stiffness of the problem, thereby enhancing both the accuracy and efficiency of the simulation.

In CADET-Core, time integration is performed using the SUNDIALS IDAS solver, which implements BDF combined with adaptive time stepping {cite}`Hindmarsh2005`.

(unit_operation_networks)=
## Solution of the system of unit operations

Before the model equations of a unit operation can be solved, the inlet concentration profiles, which serve as inputs to the boundary conditions of downstream units, must first be determined from the outputs of upstream units.
In systems with acyclic connections, these profiles can be calculated sequentially by starting from the system inlets and solving each unit operation downstream in order.
In contrast, systems with internal recycles require simultaneous solution of the system because the outlet of one unit can directly affect its own input.
This type of system is typically solved using a Newton iteration, which requires the Jacobians of the unit operations as well as the connectivity configuration that couples the units together.
In this approach, the procedure begins by computing the outlets for each unit operation based on an initial guess for the inlet profiles.
These outlet values are then used to update the inlet profiles, and the unit operations are solved again.
This procedure is repeated iteratively until the system converges and the solution is fully determined.
This iterative approach is directly relevant to the advanced operating modes considered in this work, many of which involve internal recycling streams that couple unit operation inlets and outlets.
With the model equations and their solution established, the following chapter addresses how to formulate and evaluate the performance of chromatographic processes.
