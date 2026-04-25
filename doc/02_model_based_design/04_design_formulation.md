---
jupytext:
  text_representation:
    format_name: myst
kernelspec:
  display_name: Python 3
  name: python3
---

(design_formulation)=
# Formulation of chromatographic design problems

The formulation of chromatographic design problems typically involves determining various parameters {cite}`SchmidtTraub2020`:

*Model parameters* are inherent to the chosen chromatographic system and describe its physical and chemical properties.
These include parameters related to thermodynamics, fluid dynamics, dispersion effects, and mass transfer resistances.
Model parameters can often be measured directly, obtained through correlations, or determined using inverse methods, where they are adjusted to align with experimental data or other sources of information (see {numref}`model_calibration` and {numref}`characterization`).
The accurate determination of model parameters is essential for developing precise chromatographic process models.

*Design parameters* define the overall setup and operational configuration of a chromatographic plant, which remain fixed during operation.
These parameters include decisions about operating modes (e.g., batch-elution or recycling techniques), column geometry (length and diameter), adsorbent type, and, for SMB systems: zone configurations such as the number of columns per zone.
The selection of the operating mode itself is an important design parameter, which can be systematically addressed using superstructure optimization with discrete decision variables to evaluate various configurations.
While selecting the most suitable operating mode is a critical aspect of chromatographic process design, this work focuses primarily on optimizing processes for a given configuration, rather than identifying the optimal operating mode.

*Operating parameters* refer to variables that can be adjusted during the operation of a chromatographic plant.
These include flow rates, concentrations, and valve switch times, which are critical for fine-tuning the process to achieve optimal performance.
The investigation and optimization of these operating parameters form the primary focus of this work.
Detailed case studies demonstrating their application and impact in real-world scenarios are presented in {numref}`operating_modes`.

The following sections introduce key performance indicators (KPIs) commonly used to evaluate process performance, which serve as objectives or constraints in the optimization problems formulated in {numref}`design_solution`.
This chapter concludes with a discussion of the merits of multi-objective over single-objective optimization approaches.

(model_calibration)=
## Model calibration

It is generally recommended to choose the simplest model possible, but as detailed as necessary to accurately describe the specific separation problem.
Simpler models help prevent overfitting, which occurs when an overly complex model captures noise or spurious correlations rather than the underlying physical trends, resulting in non-predictive or unrealistic parameter values.
They also enhance interpretability, allowing users to better understand the relationships between parameters and physical phenomena.
This ensures that attention is focused on the most relevant factors driving chromatographic separation while avoiding unnecessary complexity.
More complex models often involve a larger number of parameters, such as transport coefficients, dispersion values, or detailed adsorption kinetics, which can be difficult to measure or estimate accurately and are often experimentally inaccessible or prone to large uncertainties {cite}`Heymann2022`.

Model calibration involves determining all parameters required for an accurate model, whether through direct measurement, peak analysis, or inverse methods based on experimental data.
Simple geometric parameters like column length and diameter can be measured directly, while others, such as equilibrium constants or mass transfer coefficients, may be obtained through peak analysis or other targeted measurements.
For parameters that cannot be determined directly, the calibration can be formulated as an optimization problem where a comparison function (e.g., normalized root-mean-square error, NRMSE)

```{math}
:label: nrmse
\text{NRMSE} = \frac{\sqrt{\sum_{t=1}^{T} (y_t - \hat{y}_t)^2}}{y_{\text{max}} - y_{\text{min}}}
```

computes residuals between model predictions $\hat{y}_t$ and experimental data $y_t$.
For an example characterization procedure of a typical chromatographic laboratory system, refer to {numref}`characterization`.

Parameter estimation alone, however, does not account for uncertainty in the estimates.
Quantifying uncertainty is important, as chromatographic systems often exhibit nonlinear dynamics, non-Gaussian distributions, and correlated errors.
In such cases, Markov Chain Monte Carlo (MCMC) methods are typically required {cite}`Heymann2022`.
While this work focuses on parameter estimation rather than uncertainty quantification, the modular architecture of CADET-Process provides a foundation for future extensions in this direction.

(kpi)=
## Key performance indicators

Key performance indicators (KPIs) are metrics used to assess the performance of a system.
In chromatography, common KPIs include product purity, yield, productivity, eluent consumption, operating costs, and environmental impact.
KPIs are frequently employed in process optimization studies to identify areas for improvement and evaluate the effectiveness of different process scenarios.

A key measure of separation performance in chromatography is the amount of target components collected in the product fractions $f$ (see eq. {eq}`molar_amount`).
While a chromatogram is traditionally defined at the outlet of a single column, here the term is used more generally to describe concentration profiles $c_{i,k}(t)$ at the outlets $k$ of a process.
The start time, $t_{\text{start}, f}$, and end time, $t_{\text{end}, f}$, for each product fraction $f$ must be selected to ensure that product purity constraints are satisfied.
{numref}`chromatogram_fractionation` provides an example of a chromatogram from a batch-elution process, illustrating how suitable fractions are selected.

```{code-cell} ipython3
:tags: [remove-cell]

%config InlineBackend.figure_format = 'retina'

from myst_nb import glue
from examples.batch_elution.process import process

from CADETProcess.simulator import Cadet

simulator = Cadet()
simulation_results = simulator.simulate(process)

from CADETProcess.fractionation import Fractionator
fractionator = Fractionator(simulation_results)

fractionator.add_fractionation_event('start_A', 0, 5*60, 'outlet')
fractionator.add_fractionation_event('end_A', -1, 5.75*60)
fractionator.add_fractionation_event('start_B', 1, 6.5*60)
fractionator.add_fractionation_event('end_B', -1, 9*60)

from CADETProcess import plotting

fig, ax = fractionator.plot_fraction_signal(show=False)
glue("chromatogram_fractionation", fig, display=False)
```

```{glue:figure} chromatogram_fractionation
:name: "chromatogram_fractionation"
:scale: 100%

Fractionation of a chromatogram.
Blue: Target fraction of component $A$.
Red: Target fraction of component $B$.
Grey areas represent waste fractions.
```

It is important to note that in advanced chromatographic process configurations outlet chromatograms can be much more complex than the example shown in {numref}`chromatogram_fractionation` and that multiple sections of the chromatogram may represent suitable fractions $f$ for collecting one target component $i$.
Moreover, flow sheets can have multiple outlets $k$ that have to be fractionated simultaneously, and the volumetric flow rate $Q_k$ at the outlets may depend on time.
These aspects are considered by defining the total product amount of a component $i$ as:

```{math}
:label: molar_amount

n_{i} = \sum_{k=1}^{N_{\text{chrom}}} \sum_{f=1}^{N_{\text{frac}, k}^{i}}\int_{t_{\text{start}, f}}^{t_{\text{end}, f}} Q_k(t) \cdot c_{i,k}(t) \, dt, \\
```

where $N_{\text{frac}, k}^{i}$ is the number of fractions considered for component $i$ in chromatogram $k$, and $N_{\text{chrom}}$ is the total number of chromatograms evaluated.
In contrast to standard definitions, which consider a single chromatogram and one fraction per component, this formulation accounts for multiple outlets and multiple fractions, as required by advanced operating modes.

Further performance criteria frequently used for evaluating and optimizing chromatographic performance include specific productivity $PR_i$, recovery yield $Y_i$, and specific solvent consumption $EC_i$, all of which depend on the product amounts:

```{math}
:label: productivity
PR_{i} = \frac{n_i}{V^s \cdot \Delta t_{\text{cycle}}},\\
```

```{math}
:label: yield
Y_{i} = \frac{n_i}{n_{\text{feed}, i}},\\
```

```{math}
:label: eluent_consumption
EC_{i} = \frac{V_{\text{eluent}}}{n_i}.\\
```

Here, $V^s$ represents the volume of the stationary phase, $V_{\text{eluent}}$ denotes the solvent volume introduced during a cycle of duration $\Delta t_{\text{cycle}}$, and $n_{\text{feed}, i}$ is the injected amount of component $i$.
The amounts of consumed feed and solvent can be calculated from multiple sources as follows:

```{math}
:label: solvent_in
V_{\text{eluent}} = \sum_{s=1}^{N_{\text{eluents}}} \int_{0}^{t_{\text{cycle}}} Q_s(t) dt,\\
```

```{math}
:label: feed_in
n_{\text{feed},i} = \sum_{f=1}^{N_{\text{feeds}}} \int_{0}^{t_{\text{cycle}}} Q_f(t) \cdot c_{f,i}(t) dt.\\
```

The cumulative product purity $PU_i$ is given by:

```{math}
:label: purity
PU_{i} = \frac{n_{i}^{i}}{\sum_{\ell=1}^{N_{\text{comp}}} n_{\ell}^{i}},\\
```

where $N_{\text{comp}}$ is the number of mixture components, and $n_{\ell}^{i}$ is the amount of component $\ell$ in the target fraction of component $i$.

Alongside process performance indicators, economic criteria play a crucial role in evaluating the performance of a chromatographic separation process.
The total separation costs depend on contributions from adsorbent, eluent, and feed materials, as well as fixed costs such as capital investment and labor, all of which are specific to the system configuration and production site.

The total separation costs for a given chromatographic process, $C_{i, \text{total}}$, are determined by summing the fixed and variable costs.
Fixed costs are company-specific and include operating costs, $C_{operating}$, which cover overhead expenses such as wages and maintenance, as well as depreciation costs, $C_{depreciation}$, which allocate investment costs over time.
In contrast, variable costs include the costs of operation such as eluent cost, feed cost, and adsorbent cost, which are dependent on the materials used in the chromatographic separation process.
This simple calculation provides a rough estimate of the total separation costs, offering a starting point for evaluating the economic performance of a chromatographic process {cite}`Nicoud2015`:

```{math}
:label: total_cost

C_{i,\text{total}} = C_{\text{operating}} + C_{\text{depreciation}} + C_{i,\text{ads}} + C_{i,\text{eluent}} + C_{i,\text{feed}}. \\
```

The cost associated with the eluent, $C_{i, \text{eluent}}$, which is the solvent used to elute the target product from the adsorbent, is calculated as:

```{math}
:label: eluent_cost
C_{i, \text{eluent}} = EC_{i} \cdot \dot{n}_{i, \text{annual}} \cdot p_{\text{eluent}}, \\
```

where $EC_{i}$ is the eluent consumption in $\text{m}^3$ per mol of product, $\dot{n}_{i, \text{annual}}$ is the annual production rate in mol per year, and $p_{\text{eluent}}$ is the eluent price in $\euro$ per $\text{m}^3$.
The feed cost, $C_{i, \text{feed}}$, which reflects the cost of the feed material processed in the separation, is given by:

```{math}
:label: feed_cost
C_{i, \text{feed}} = \frac{1 - Y_i}{Y_i} \cdot \dot{n}_{i, \text{annual}} \cdot p_{\text{feed}}, \\
```

where $Y_i$ is the product yield, and $p_{\text{feed}}$ is the feed price in $\euro$ per $\text{m}^3$.
The adsorbent cost, $C_{i, \text{ads}}$, which reflects the cost of the adsorbent material used in the separation, can be calculated as:

```{math}
:label: adsorbent_cost

C_{i,\text{ads}} = \frac{1}{PR_i} \cdot \dot{n}_{i,\text{annual}} \cdot \frac{p_{\text{ads}}}{\Delta t_{\text{life}}}, \\
```

where $PR_i$ is the productivity in mol per $\text{m}^3$ of adsorbent per unit time, $p_{\text{ads}}$ is the adsorbent price in $\euro$ per $\text{m}^3$, and $\Delta t_{\text{life}}$ is the lifetime of the adsorbent material.

## Objective functions

Let $x$ denote the vector of optimization variables (e.g., feed duration, flow rates, switching times).
In optimization, an objective function quantifies the quality of a solution.
Simple objective functions often combine criteria, such as those introduced in {numref}`kpi`, to evaluate process performance.
However, more detailed cost functions can also be employed to directly maximize the profit of a separation process.
For a discussion of further objective functions, see {cite}`SchmidtTraub2020,Nicoud2015,Dienstbier2020`.

A commonly used objective function combines specific productivity, recovery yield, and eluent consumption into a single metric:

```{math}
:label: weighted_objective
f(x) = \frac{PR_{\text{weighted}}(x) \cdot Y_{\text{weighted}}(x)}{EC_{\text{weighted}}(x)}
```

Here, $PR_{\text{weighted}}(x)$, $Y_{\text{weighted}}(x)$, and $EC_{\text{weighted}}(x)$ represent the weighted values of productivity, yield, and eluent consumption, respectively.
The term "weighted" reflects the process of assigning weighting factors to individual components, allowing their relative importance to be incorporated into the overall objective.
When multiple target components are considered, their contributions to the objective function are combined using weighting factors $\omega_i$, which reflect the relative significance of each component.
Each weighted performance indicator $KPI_{\text{weighted}}$ is then calculated as:

```{math}
:label: ranked_performance
KPI_{\text{weighted}} = \frac{\sum_{i=1}^{N_{\text{comp}}} \omega_i \cdot KPI_i}{\sum_{i=1}^{N_{\text{comp}}} \omega_i}
```

By assigning appropriate weights, this approach enables optimization to reflect specific priorities or goals, such as emphasizing yield of one component in some situation, while prioritizing productivity for another.

(multi_objective_optimization)=
## Multi-objective optimization

In recent years, there has been growing interest in applying multi-objective optimization (MOO) instead of single-objective optimization (SOO) in various fields, including chromatography.
While SOO focuses on optimizing a single criterion, it can sometimes lead to information loss by overlooking other important factors.
In contrast, MOO simultaneously considers multiple objectives, providing a more comprehensive analysis of the design space {cite}`Knutson2015,Heymann2022`.

One of the main advantages of MOO in chromatography optimization is that it typically does not require significantly more computational power compared to SOO.
Most of the computational time is usually spent evaluating the underlying model rather than the optimization algorithm itself.
In fact, in many cases, the individual objective values are already calculated during an SOO process, where they are subsequently "reduced" to a single objective, essentially discarding valuable information.
By avoiding this reduction, MOO provides a more complete understanding of the solution space, though the additional overhead of exploring the Pareto front also introduces some additional computational cost compared to a single SOO run.

It is important to note, however, that not all optimization algorithms can be directly applied to MOO.
For instance, evolutionary algorithms such as genetic algorithms (GA) are well-suited for both SOO and MOO.
In contrast, gradient-based optimization methods, such as Gradient Descent, are generally designed for single-objective problems and may require adaptations to handle multiple objectives.
Nonetheless, MOO has shown great promise in improving the design of chromatographic processes, particularly when optimizing multiple objectives that are difficult to combine into a single metric.

Interestingly, MOO can also be beneficial even in situations where a single "best" solution is expected (e.g., parameter fitting).
In such cases, MOO can converge more efficiently to a solution by addressing different aspects of the problem simultaneously.
This capability allows the algorithm to explore the solution space more effectively, leading to faster convergence to the optimal solution {cite}`Deb2002`.
Moreover, MOO is especially advantageous when dealing with multiple datasets or complex optimization problems.
It can help identify conflicting datasets or reveal ill-posed optimization problems, such as those arising from overdetermined systems.
By considering multiple objectives, MOO can uncover inconsistencies in the data or problem formulation that may not be apparent in SOO.
This makes MOO particularly useful when dealing with multiple experimental datasets or when diagnosing ill-posed problems, as conflicting objectives can reveal inconsistencies that a single scalar metric would obscure.

<!-- 2.4.1. Was  wollen wir wissen -->
<!-- 2.4.2. Wie bewerten wie es -->
<!-- 2.4.3. Single objective vs multi objective? -->
