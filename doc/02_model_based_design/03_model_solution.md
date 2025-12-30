(model_solution)=
# Solution of chromatographic process models
The chromatographic models introduced in {numref}`section %s<model_formulation>` consist of systems of partial differential equations (PDEs) or partial differential-algebraic equations (PDAEs) in space and time.
While highly detailed models that account for numerous transport effects can provide highly accurate approximations of chromatographic separation, they often require substantial computational resources, even with modern software and hardware {cite}`Puettmann2015`.
However, it is often possible to achieve accurate results with simpler models, which focus on capturing only the essential transport and interaction phenomena necessary to describe the process accurately.
For example, simplified models may neglect minor effects that have minimal influence on the outcome, reducing complexity while retaining predictive power.
This approach is particularly advantageous in scenarios requiring multiple simulations, such as parameter estimation or process optimization, where computational efficiency is critical.

To guide model selection, it is generally recommended to choose the simplest model possible, but as detailed as necessary to accurately describe the specific separation problem.
Simpler models help prevent overfitting, which occurs when an overly complex model fits meaningless patterns or noise in the data, resulting in non-predictive or unrealistic parameter values.
They also enhance interpretability, allowing users to better understand the relationships between parameters and physical phenomena.
This ensures that attention is focused on the most relevant factors driving chromatographic separation while avoiding unnecessary complexity.
It is important to note that more complex models often involve a larger number of parameters, such as transport coefficients, dispersion values, or detailed adsorption kinetics.
These parameters can be difficult to measure or estimate accurately and are often experimentally inaccessible or prone to large uncertainties {cite}`Heymann2022`.

In this work, the aim is to provide a modular and general-purpose modeling tool that is capable of handling a wide range of chromatography models, from simplified to highly detailed.
This flexibility allows users to choose the most appropriate model for their specific problem, balancing computational efficiency with the level of detail required for accurate predictions.
By offering this modular approach, the tool supports a broad range of applications, from rapid optimization using reduced models to in-depth analysis using detailed, high-definition models.


(analytical_solutions)=
## Analytical solutions

For calculating concentration profiles in chromatographic processes, closed-form analytical solutions are highly desirable because they allow for accurate and fast computations.
However, such analytical solutions are limited to specific models and rely on restrictive simplifying assumptions.
For example, the equilibrium model can be solved analytically for the linear isotherm, as well as for the multicomponent Langmuir isotherm {cite}`SchmidtTraub2020`.
Moreover, Fechtner et al. have demonstrated a semi-analytical approach applicable any implicit isotherm model in the equilibrium model {cite}`Fechtner2017`.

Additionally, even more complex models can be solved analytically when a linear adsorption isotherm is assumed {cite}`Qamar2014,Leweke2021`.
However, the restrictive assumptions required for these solutions limit their utility as general-purpose modeling tools.

While earlier sections emphasized the benefits of simplified models for computational efficiency, analytical solutions alone are often insufficient to address the complexity of practical chromatographic processes.
As a result, numerical approaches are commonly employed to approximate the solutions of chromatographic models.

Despite their limitations, analytical solutions remain valuable in the context of numerical simulations.
They can serve as benchmark and test cases to validate the implementation of numerical schemes (see also {numref}`software_tests`).
For instance, the [CADET-Semi-analytic](https://github.com/modsim/CADET-semi-analytic) framework computes reference solutions for the general rate model with proven error bounds using analytical solutions in the Laplace domain combined with numerical inversion {cite}`Leweke2016`.
Although this method is restricted to the linear isotherm, it is particularly useful due to the modular nature of the **CADET-Core** code.
In **CADET-Core**, binding models represent only a small fraction of the overall source code.
As such, analytical solutions can still validate critical aspects of the code, including convection, diffusion, and networks of unit operations.

To validate the connectivity and dynamic events of the operating modes described later in this work, equilibrium theory for single columns is applied (see {numref}`equilibrium_model`) to determine propagation velocities and corresponding elution times {cite}`SchmidtTraub2020`.
By accounting for additional events such as recycling times, switching flow direction, virtually extending the column length, or re-injecting recycled fractions, simple chromatograms for advanced operating modes can be calculated.
These are then compared to the numerical solutions obtained from **CADET-Core**.

Using the chain rule, the time derivative of the solid phase concentration can be expressed in terms of the isotherm slope and the liquid phase time derivative:

```{math}
:label: solid_phase_derivative_chain_rule

\frac{\partial q_i}{\partial t} = \left. \frac{\text{d} q_i}{\text{d} c_i} \right|_{c_i^+} \cdot \frac{\partial c_i}{\partial t}.
```

Rearranging eq. {eq}`mass_balance_em` and substituting eq. {eq}`solid_phase_derivative_chain_rule` yields the propagation velocity $w(c_i^+)$
of a concentration front $c_i^+$:

```{math}
:label: propagation_velocity

w(c_i^+) = \frac{u}{1 + F \cdot \left. \frac{\text{d} q_i}{\text{d} c_i} \right|_{c_i^+}}.
```

By considering the column length $L_c$, the retention time for a concentration $t_{\text{R},i}(c_i^+)$ can be derived as:

```{math}
:label: retention_time

t_{\text{R},i}(c_i^+) = \frac{L_c}{w(c_i^+)} = t_{0,t} \cdot \left( 1 + F \cdot \left. \frac{\text{d} q_i}{\text{d} c_i} \right|_{c_i^+} \right),
```

where $t_{0,t} = L_c / u$ is the column dead time.
For a linear isotherm, where $\frac{\text{d} q_i}{\text{d} c_i} = a_i$ (Henry coefficient), this simplifies to:

```{math}
:label: retention_time_linear

t_{\text{R,lin},i} = t_{0,t} \cdot \left( 1 + F \cdot a_i \right).
```

(numerical_solutions)=
## Numerical solution

To numerically approximate the solution of the model equations, the method of lines is commonly applied.
In this approach, the spatial coordinates are first discretized, resulting in a system of ordinary differential equations (ODEs) or differential-algebraic equations (DAEs), depending on the isotherm being used.
This step is often referred to as spatial semi-discretization because only the spatial dimensions are discretized, leaving time as a continuous variable.
Next, the resulting system of equations is discretized in time using either explicit or implicit methods.

Generally, the finer the grid used to discretize the continuous space-time domain, the closer the numerical approximation will be to the exact solution.
However, this comes at the cost of increased computational effort.
The performance of a numerical solution method is often evaluated by examining its order of convergence, which measures how quickly the numerical solution approaches the exact solution as the grid is refined.
Higher convergence orders generally lead to faster and more accurate solutions, but they may also require more computational resources per grid point.
It is important to note that the expected convergence order is typically only achieved asymptotically, meaning that sufficient degrees of freedom (DOFs) are needed for the method to realize its full accuracy potential.
Despite these trade-offs, numerical methods with high convergence orders are recommended for solving chromatographic models, as they often provide a good balance between accuracy and computational efficiency.
Additionally, higher-order methods tend to exhibit other advantageous properties, such as improved stability {cite}`Atkinson2011`.

Several numerical methods have been successfully applied to solve chromatographic models.
The following sections provide an overview of selected methods commonly used in state-of-the-art simulation software.
First, different approaches for spatial semi-discretization are discussed, followed by an overview of methods for time integration.


(spatial_discretization)=
### Spatial discretiation

% Finite Difference
The finite difference method (FDM) is based on Taylor's theorem, where a Taylor series is used to replace spatial derivatives with discrete difference quotients.
For example, the spatial first-order forward finite difference is derived by approximating the derivative at a point $z_i$ as:

```{math}
:label: finite_difference_scheme

\frac{\partial c(z_i)}{\partial z} \approx \frac{c(z_i+\Delta z) - c(z_i)}{\Delta z}
```

where $\Delta z$ is the grid spacing.

FDM is widely used due to its simplicity and computational efficiency, especially for problems with smooth solutions.
To achieve higher accuracy, higher-order schemes can incorporate additional neighboring points.

A well-known first-order FDM scheme is the forward-backward method by Rouchon et al. {cite}`Rouchon1987`.
This method solves the equilibrium-dispersive model (EDM) equations by neglecting the dispersion term in the FDM formulation and using the second-order truncation error to approximate the apparent dispersion.
While straightforward, this approach can result in large ODE systems, as a fine grid is often required for accurate approximations when dispersion is low {cite}`SchmidtTraub2020`.

However, FDM has several limitations that can affect its accuracy and applicability.
One key challenge is numerical dispersion, which is an artifact introduced by the discretization process.
Numerical dispersion can distort sharp gradients or high-frequency oscillations in the solution, leading to inaccuracies.
In some cases, methods like the forward-backward method attempt to approximate physical dispersion using this numerical artifact, but this approach may compromise accuracy in systems with steep concentration profiles and for low values of the axial dispersion coefficient.
Additionally, FDM is not inherently mass-conservative, meaning the total mass in the system may not be preserved.
This issue can become significant in scenarios where conservation laws play a critical role, such as in multicomponent systems or when performing long-term simulations.
Despite these drawbacks, FDM remains widely used, as its simplicity and efficiency make it a practical choice for many applications.


% Finite Volume
Unlike FDM, which computes solutions at discrete points, the finite volume method (FVM) defines a grid of cells and computes spatially averaged values within each cell.
For chromatographic models, interstitial concentrations are averaged over $j \in { 0, \dots, N_z - 1 }$ uniform cells with a grid spacing $\Delta z = L_c / N_z$.
This creates a staircase function representation of the solution and defines a local Riemann problem at each cell interface {cite}`Guiochon2006`.
The flux across these interfaces is approximated using a numerical flux function $F$, leading to the following semi-discretized formulation in 1D:

```{math}
\frac{d c_j(t)}{d t} \approx \frac{1}{\Delta z} (F(c_{j-1}, c_j) - F(c_j, c_{j+1}))
```

for each control volume $j \in \{ 0, \dots, N_{z} - 1 \}$, with c_{-1}, c_{N_z} given by boundary conditions.

FVM offers key advantages over FDM, particularly due to its intrinsic conservation properties, ensuring that mass is preserved across cell interfaces.
This property is especially important in chromatographic models, where conservation of mass is critical for obtaining accurate results.
Additionally, FVM is monotonicity-preserving, which prevents unphysical oscillations in the solution, making it well-suited for problems involving sharp concentration gradients {cite}`Blazek2015,Koren1993`.

To achieve higher accuracy, the finite volume method (FVM) can employ polynomial reconstructions to approximate values within each control volume using information from neighboring cells.
This stencil-based reconstruction enables high-order schemes that preserve mass conservation.
However, as described by Godunov's theorem, linear high-order schemes cannot maintain monotonicity, resulting in oscillations near steep gradients {cite}`Godunov1959`.
To address this issue, nonlinear reconstruction techniques are commonly applied, such as slope limiters {cite}`Blazek2015` or weighted essentially non-oscillatory (WENO) schemes {cite}`Lieres2010`.
The WENO scheme is particularly suitable for chromatographic systems with sharp concentration gradients, as it balances accuracy, stability, and robustness.
For these reasons, the WENO scheme is implemented in **CADET-Core** and used in this work {cite}`Leweke2018`.

% Finite Elements Method
The finite element method (FEM) divides the spatial domain into cells, similar to the FVM.
However, FEM introduces a polynomial of arbitrary order for each cell, enabling high accuracy with a relatively low number of cells, provided the solution is sufficiently smooth {cite}`SchmidtTraub2020`.

The classical FEM approach, known as the continuous Galerkin (CG) method, enforces continuity across cell interfaces, resulting in a tightly coupled system of ODEs.
This method, however, has several drawbacks.
FEM is not inherently conservative, making it challenging to ensure mass conservation.
Additionally, retaining high-order accuracy at boundaries can be difficult, and the implementation is generally more complex compared to FVM.
Nonetheless, CG is currently implemented in Cytiva's commercial GoSilico™ Chromatography Modeling Software, where a streamline-upwind Petrov-Galerkin stabilization (SUPG) technique is applied to improve numerical stability {cite}`Hahn2015`.

In contrast, the discontinuous Galerkin (DG) method allows for discontinuities at cell interfaces, combining elements of FVM and FEM.
This flexibility permits the use of numerical fluxes to solve the local Riemann problem, introducing artificial numerical dispersion into the scheme.
Unlike in FDM, this artificial dispersion is considered beneficial in DG, as it provides stabilizing effects that reduce oscillations, particularly for systems with steep gradients {cite}`Brezzi2006`.
While DG has some disadvantages compared to CG, such as a larger state vector due to the discontinuous cell boundaries, these are outweighed by its stabilizing properties and the simpler integration of boundary conditions.

Recent studies have demonstrated that DG can achieve high computational performance, making it a promising area of ongoing research {cite}`Meyer2020, Breuer2023, Frandsen2025`.

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

In **CADET-Core**, time integration is performed using the **SUNDIALS IDAS** solver which implements BDF combined with adaptive time stepping {cite}`Hindmarsh2005`.

(unit_operation_networks)=
## Solution of the system of unit operations

Before the model equations of a unit operation can be solved, the inlet profiles, which act as boundary conditions, must first be determined from the outputs of upstream units.
In systems with acyclic connections, these profiles can be calculated sequentially by starting from the system inlets and solving each unit operation downstream in order.
In contrast, systems with internal recycles require simultaneous solving because the outlet of one unit can directly affect its own input.
This type of system is typically solved using a Newton iteration, which requires the Jacobians of the unit operations as well as the connectivity configuration that couples the units together.
In this approach, the procedure begins by computing the outlets for each unit operation based on an initial guess for the inlet profiles.
These outlet values are then used to update the inlet profiles, and the unit operations are solved again.
This procedure is repeated iteratively until the system converges and the solution is fully determined.
