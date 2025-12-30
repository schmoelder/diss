(operating_modes)=
# Optimization of advanced operating concepts

@TODO: Improve transition from previous study

Here, more synthetic cases.
We assume, model parameters are known, models is characterized / parametrized.

This chapter demonstrates the flexibility of the framework to model and optimize a range of chromatographic operating modes.
These studies focus on preparative separations of binary and ternary mixtures using operating modes of varying complexity and optimization variables.
The goal is to showcase the flexibility of the framework in modeling and optimizing different chromatographic operating modes, including batch elution, recycling techniques, flip-flop chromatography, and serial columns.
In all cases, a lumped rate model with pores ({numref}`lumped_rate_model_with_pores`) and a competitive Langmuir binding model in rapid equilibrium ({numref}`langmuir_model`) are employed.
All processes operate in flow-through mode, assuming the solvent has no impact on binding.
The parameters used are summarized in {numref}`model_parameters`.

```{table} Parameters of column geometry, mass transport and binding of the model molecules ($i \in \{A, B\}$).
:name: model_parameters
:align: center

| Catalog       | Symbol          | Description               | Value                | Unit                                   |
| ------------- | --------------- | ------------------------- | -------------------- | -------------------------------------- |
| **Geometry**  | $L$             | Column length             | $0.6$                | $\text{m}$                             |
|               | $d$             | Column diameter           | $0.024$              | $\text{m}$                             |
|               | $d_r$           | Particle radius           | $1.0 \times 10^{-5}$ | $\text{m}$                             |
|               | $\varepsilon_b$ | Bed porosity              | $0.3$                | –                                      |
|               | $\varepsilon_p$ | Particle porosity         | $0.6$                | –                                      |
| **Transport** | $D_{ax,i}$      | Axial dispersion coeff.   | $1.0 \times 10^{-6}$ | $\text{m}^{2}~\text{s}^{-1}$           |
|               | $k_{f,i}$       | Film mass transfer coeff. | $1.0 \times 10^{-3}$ | $\text{m}~\text{s}^{-1}$               |
| **Binding**   | $k_{eq,i}$      | Equilibrium constant      | $[0.02, 0.03]$       | $\text{m}^{3}~\text{mol}^{-1}$         |
|               | $q_{max,i}$     | Saturation capacities     | $[100, 100]$         | $\text{mol}~\text{m}_{\text{sp}}^{-1}$ |
| **Process**   | $Q$             | Flow rate                 | $[0.01, 0.05]$       | $\text{m}^{3}~\text{s}^{-1}$           |
```

Given the moderately nonlinear conditions and an axial dispersion coefficient corresponding to approximately 2000 theoretical stages, the separation difficulty of these examples is considered modest.
By selecting appropriate operating conditions, such as injection volume and flow rate, the stationary phase can be utilized optimally for efficient separation.

For each operating mode, the process configuration is presented using a {class}`~CADETProcess.processModel.FlowSheet` and various dynamic {class}`Events <CADETProcess.dymamicEvents.Event>`, which are then simulated using **CADET-Core** (see {numref}`process_model` and {numref}`process_simulation`).
To validate the configuration, simulation results from an ideal model are compared with equilibrium theory predictions under simplified conditions, assuming a linear isotherm with an equivalent Henry coefficient and negligible axial dispersion and transport-limiting effects.
These assumptions allow direct comparison with analytical solutions, confirming the correct implementation of the process configuration (see {numref}`analytical_solutions`).

In all cases, the following key performance indicators (KPIs) were evaluated after automatically determining optimal fractionation times using the {mod}`~CADETProcess.fractionation` module, ensuring a minimum purity requirement of $95\%$ (eq. {eq}`purity`):
- Productivity (eq. {eq}`productivity`)
- Yield (eq. {eq}`yield`)
- Eluent consumption (eq. {eq}`eluent_consumption`)

These metrics were either combined into a weighted objective (eq. {eq}`weighted_objective`) or addressed through multi-objective optimization.
To achieve this, process-specific operating parameters, typically the timing of valve switches (i.e., the {class}`Events <CADETProcess.dymamicEvents.Event>` times), were added as optimization variables (see {numref}`optimization`.

The highest product recovery is usually achieved through baseline separation, where component peaks from the same injection do not overlap at the column outlet.
Minimizing the time between injections also improves productivity.
Collecting waste fractions between product fractions or between peaks of consecutive injections can further optimize productivity and eluent consumption, though this may reduce recovery.
These operating conditions can be adjusted using model-based design.
By allowing waste fractions to be collected between product fractions or between peaks of consecutive injections, productivity and eluent consumption can be further optimized at the cost of lower recovery.

All optimization problems were solved using the *pymoo* package with a non-dominated sorting genetic algorithm {cite}`pymoo2020`.
Scripts to recreate the simulations and optimizations are available in the supplementary material and online (@TODO: add links).
