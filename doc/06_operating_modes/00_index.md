(operating_modes)=
# Optimization of advanced operating concepts

This chapter presents a set of synthetic case studies to demonstrate the flexibility of CADET-Process for modeling and optimizing advanced chromatographic operating modes, including batch elution, recycling strategies, flip-flop chromatography, and serial-column configurations.
In contrast to {numref}`characterization`, the emphasis shifts from parameter estimation to process design and optimization of preparative separations of binary and ternary mixtures, assuming that parameter estimation has been performed previously.
Each case study follows a consistent structure: first, the process model is validated; then, optimization is explored with an increasing number of decision variables.

In all cases, simulations are based on a lumped-rate model with pores (see {numref}`lumped_rate_model_with_pores`) coupled with either a competitive Langmuir binding model or a linear model with equivalent equilibrium coefficients, both under rapid-equilibrium assumptions (see {numref}`langmuir_model`).
All processes operate in flow-through mode, assuming negligible solvent effects on binding.
To simplify the analysis, system periphery effects are neglected.
The scenarios considered include a standard binary separation, an easily separable system with a high separation factor, a challenging system with a low separation factor, and a ternary separation problem.
The corresponding model parameters are summarized in {numref}`model_parameters`.

```{table} Parameters of column geometry, mass transport and binding of the model molecules ($i \in \{A, B\}$).
:name: model_parameters
:align: center
| Catalog                 | Symbol               | Description               | Value                 | Unit                                   |
| ----------------------- | -------------------- | ------------------------- | --------------------- | -------------------------------------- |
| **Geometry**            | $L$                  | Column length             | $0.6$                 | $\text{m}$                             |
|                         | $D_c$                  | Column diameter           | $0.024$               | $\text{m}$                             |
|                         | $r^p$                | Particle radius           | $1.0 \times 10^{-5}$  | $\text{m}$                             |
|                         | $\varepsilon^b$      | Bed porosity              | $0.3$                 | -                                      |
|                         | $\varepsilon^p$      | Particle porosity         | $0.6$                 | -                                      |
| **Transport**           | $D_{ax,i}$           | Axial dispersion coeff.   | $1.0 \times 10^{-6}$  | $\text{m}^{2}~\text{s}^{-1}$           |
|                         | $k_{f,i}$            | Film mass transfer coeff. | $1.0 \times 10^{-3}$  | $\text{m}~\text{s}^{-1}$               |
| **Binding (standard)**  | $K_{\text{eq},i}$    | Equilibrium constant      | $[0.02, 0.03]$        | $\text{m}^{3}~\text{mol}^{-1}$         |
|                         | $c^s_{\text{max},i}$ | Saturation capacities     | $[100, 100]$          | $\text{mol}~\text{m}_{\text{sp}}^{-1}$ |
| **Binding (ternary)**   | $K_{\text{eq},i}$    | Equilibrium constant      | $[0.01, 0.015, 0.03]$ | $\text{m}^{3}~\text{mol}^{-1}$         |
|                         | $c^s_{\text{max},i}$ | Saturation capacities     | $[100, 100, 200]$     | $\text{mol}~\text{m}_{\text{sp}}^{-1}$ |
| **Binding (simple)**    | $K_{\text{eq},i}$    | Equilibrium constant      | $[0.01, 0.20]$        | $\text{m}^{3}~\text{mol}^{-1}$         |
|                         | $c^s_{\text{max},i}$ | Saturation capacities     | $[100, 100]$          | $\text{mol}~\text{m}_{\text{sp}}^{-1}$ |
| **Binding (difficult)** | $K_{\text{eq},i}$    | Equilibrium constant      | $[0.01, 0.015]$       | $\text{m}^{3}~\text{mol}^{-1}$         |
|                         | $c^s_{\text{max},i}$ | Saturation capacities     | $[100, 100]$          | $\text{mol}~\text{m}_{\text{sp}}^{-1}$ |
| **Process**             | $Q$                  | Flow rate                 | $[0.01, 0.05]$        | $\text{m}^{3}~\text{s}^{-1}$           |
|                         | $c_{\text{feed}}$    | Concentration             | $[10.0, 10.0, 10.0]$  | $\text{mol}~\text{m}^{-3}$             |
```

For each operating mode, the process configuration is defined via a {class}`~CADETProcess.processModel.FlowSheet` in combination with dynamic {class}`Events <CADETProcess.dynamicEvents.Event>` that specify time-dependent boundary conditions, parameters, and valve switches.
Simulations are carried out with CADET-Core (see {numref}`process_model`, {numref}`process_simulation`).
To verify the correctness of the configuration, results obtained from an idealized model variant are compared against equilibrium theory predictions under simplified assumptions: a linear isotherm with an identical Henry coefficient, negligible axial dispersion, and the absence of mass-transfer limitations.
Under these conditions, analytical solutions are available, enabling a direct consistency check of the implemented process setup ({numref}`analytical_solutions`).

Efficient utilization of the stationary phase and maximized separation performance can be achieved by selecting appropriate operating conditions, such as injection volume and valve switching times.
Separation performance is evaluated using the following key performance indicators (KPIs):
- Productivity (eq. {eq}`productivity`)
- Yield (eq. {eq}`yield`)
- Eluent consumption (eq. {eq}`eluent_consumption`)

These KPIs typically involve trade-offs.
For instance, maximum recovery yield is usually obtained under baseline separation, where component peaks do not overlap at the column outlet.
However, productivity can be increased and eluent consumption reduced by minimizing the cycle time, particularly through stacked injections (injecting before the previous injection peaks have fully eluted).
Allowing intermediate waste fractions between product fractions or between peaks of successive injections can further improve productivity and reduce eluent consumption, though this may lower yield.

These trade-offs are systematically explored using model-based process design by formulating an {class}`~CADETProcess.optimization.OptimizationProblem`, where the KPIs serve as objectives.
The KPIs are either aggregated into a single-objective function ({eq}`weighted_objective`) or treated as separate objectives in a multi-objective optimization problem.

Optimal fractionation windows, determined automatically after each simulation using the {mod}`~CADETProcess.fractionation` module, ensure a minimum purity constraint of $95\%$ ({eq}`purity`, {numref}`fractionation`).
The decision variables include process-specific operating parameters, such as valve switching times (i.e., the time points of {class}`Events <CADETProcess.dynamicEvents.Event>`; {numref}`optimization`), as well as process parameters like column length.

All optimization problems were solved using the *pymoo* framework with a non-dominated sorting genetic algorithm {cite}`pymoo2020`.
Scripts to reproduce the simulations and optimization studies are provided in the supplementary material and are publicly available at: [https://github.com/schmoelder/diss_operating_modes](https://github.com/schmoelder/diss_operating_modes).
Figures showing optimization landscapes across multiple decision variables are scaled to fit the page format; the digital version of this thesis provides full-resolution figures.
