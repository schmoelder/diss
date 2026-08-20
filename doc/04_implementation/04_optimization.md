---
jupytext:
  text_representation:
    format_name: myst
kernelspec:
  display_name: Python 3
  name: python3
execution:
  timeout: 600
---

```{code-cell} ipython3
:tags: [remove-cell]

from myst_nb import glue
%config InlineBackend.figure_format = 'retina'
```

(optimization)=
# Optimization

Model-based engineering tasks in chromatography, including model calibration, experimental design, process optimization, and process control, all involve solving optimization problems (see {numref}`optimization_algorithms`).
These problems are typically high-dimensional, involve multiple objectives and constraints, and the feasible region is often non-convex.

A wide range of optimization software is available, from libraries that expose individual solver algorithms to more comprehensive frameworks that include preprocessing utilities or surrogate modeling.
Choosing an appropriate solver is non-trivial: some are tailored for single-objective problems, others lack support for complex constraints, and few are suited for global optimization of expensive black-box functions.
Beyond the choice of solver, applying these tools to chromatographic simulation requires additional infrastructure: variables often span multiple orders of magnitude and benefit from normalization, objectives depend on model parameters nested deep in the process configuration, and multiple processing steps separate the decision variables from the computed metric.
CADET-Process provides a unified layer on top of established external optimizers that handles these challenges and supports two key workflows: process optimization, where operating parameters are adjusted to maximize performance indicators, and parameter estimation, where model parameters are determined from experimental data.
Applications are presented in {numref}`characterization` and {numref}`operating_modes`.

In the simplest case, an optimization problem consists of minimizing a function $f(x)$ by systematically varying the input values $x$:

```{math}
:label: objective

\min_x f(x).
```

In practice, many variables are subject to optimization simultaneously, multiple criteria must be balanced, and additional constraints need to be considered:

```{math}
:label: optimization_problem_eq

\min_x \quad f(x) \\
\textrm{s.t.} \quad &g(x) \le 0, \\
              \quad &h(x) = 0, \\
              \quad &x \in \mathbb{R}^n, \\
```

where $g$ summarizes all inequality constraint functions, and $h$ equality constraints.

To decouple the problem formulation from the problem solution, two classes are provided:
An {class}`~CADETProcess.optimization.OptimizationProblem` class to specify optimization variables, objectives and constraints.
And an {class}`~CADETProcess.optimization.OptimizerBase` class which allows interfacing different external optimizers to solve the problem.
In the following, the {mod}`~CADETProcess.optimization` module of CADET-Process is introduced and core features are discussed.

(optimization_problem)=
## Optimization problem

The {class}`~CADETProcess.optimization.OptimizationProblem` class is designed for defining optimization variables, objectives, and constraints.
It allows the addition of any number of variables, each with optional lower and upper bounds.

(variable_normalization)=
### Variable normalization

Optimization algorithms often struggle when variables span multiple orders of magnitude, as large differences in scale distort the relative influence of each parameter on the objective function {cite}`Heymann2022`.
Without normalization, the optimizer effectively treats all parameters as if they operate on the same scale, leading to biased exploration and an increased risk of missing optimal regions at the lower end of wide-ranging variables.
CADET-Process addresses this by supporting both linear and logarithmic normalization, mapping each variable to a consistent $[0, 1]$ domain while handling the inverse transformation back to physical units transparently.
The linear normalization is defined as

```{math}
:label: linear_normalization

x^\prime = \frac{x - x_{lb}}{x_{ub} - x_{lb}}.
```

The logarithmic normalization is defined as

```{math}
:label: log_normalization

x^\prime = \frac{log \left( \frac{x}{x_{lb}} \right) }{log \left( \frac{x_{ub} }{x_{lb}} \right) }.
```

```{raw} latex
\needspace{6\baselineskip}
```
Consider the characterization of a chromatographic column (refer also to {numref}`characterization`), where two parameters are optimized:

- **Bed porosity**, ranging from $0.1$ to $0.8$
- **Axial dispersion**, ranging from $1 \times 10^{-9}$ to $1 \times 10^{-4}~\text{m}^2~\text{s}^{-1}$.

Due to this disparity in scales, porosity is normalized linearly while axial dispersion uses logarithmic normalization.
As shown in {numref}`fig_initial_values`, sampling without normalization clusters near the upper end of the $D_{\text{ax}}$ range, leaving the lower orders of magnitude nearly unexplored.
With normalization ({numref}`fig_initial_values_normalized`), samples are distributed near-uniformly across the full five orders of magnitude, which is essential for generating effective initial values and ensuring the optimizer explores the relevant parameter space (see {numref}`initial_values`).

```{code-cell} ipython3
:tags: [remove-cell]

from CADETProcess.optimization import OptimizationProblem
from CADETProcess import plotting

#: 2x2 grids come out at 90 mm tall, which keeps them under 48 % of the text
#: height including the caption and therefore lets two share a page.
DEMO_PANEL_IN = 45/25.4
#: Wider than DEMO_PANEL_IN for the pairwise initial-value demos specifically:
#: those panels were reading as cramped, and widening only the width (not the
#: shared square panel_in) keeps the page-height budget above unchanged.
DEMO_PANEL_WIDTH_IN = 52/25.4
#: The 1x2 convergence plot is only half as tall and is sized on its own.
CONVERGENCE_PANEL_IN = 65/25.4
DEMO_MARKER_SIZE = 4.0


def setup_demo_axes(nrows=2, ncols=2, share=True, panel_in=DEMO_PANEL_IN, panel_width_in=None):
    """Create a grid of demo panels at a fixed physical size.

    The optimization demos are sized by panel rather than by figure, so that
    the 2x2 grids come out identical. `share` mirrors what the plot method
    would set up on its own: the pairwise plots share axes per column and row,
    `plot_objectives` and `plot_convergence` do not. `panel_width_in` overrides
    the panel width alone, independent of its height.
    """
    if panel_width_in is None:
        panel_width_in = panel_in
    sharing = {"sharex": "col", "sharey": "row"} if share else {}
    return plotting.setup_figure(
        nrows=nrows,
        ncols=ncols,
        figsize=(ncols*panel_width_in, nrows*panel_in),
        squeeze=False,
        **sharing,
    )


def set_demo_marker_size(axes, marker_size=DEMO_MARKER_SIZE):
    for axis in axes.flat:
        for collection in axis.collections:
            if hasattr(collection, "set_sizes"):
                collection.set_sizes([marker_size])


def set_demo_limits(axes, bounds):
    """Force the same axis limits on both pairwise demo figures.

    Autoscaling fits each panel to its own sampled points, so a clustered
    sample and a spread-out sample can end up looking similarly distributed
    once each is scaled to fill its panel. Fixing both figures to the true
    variable bounds keeps the comparison honest.
    """
    for col, (lb, ub) in enumerate(bounds):
        axes[-1, col].set_xlim(lb, ub)
    for row, (lb, ub) in enumerate(bounds):
        axes[row, 0].set_ylim(lb, ub)


DEMO_VARIABLE_BOUNDS = [(0.1, 0.8), (1e-9, 1e-4)]

optimization_problem = OptimizationProblem('no_transform_demo')
optimization_problem.add_variable(r'$\varepsilon_{\text{bed}}$', lb=0.1, ub=0.8)
optimization_problem.add_variable(r'$D_{\text{ax}}$', lb=1e-9, ub=1e-4)

x0 = optimization_problem.create_initial_values(2*64)
pop = optimization_problem.create_population(x0)

fig, axs = setup_demo_axes(panel_width_in=DEMO_PANEL_WIDTH_IN)
pop.plot_pairwise(autoscale=True, ax=axs)
set_demo_marker_size(axs)
set_demo_limits(axs, DEMO_VARIABLE_BOUNDS)
fig.tight_layout()
glue("fig_initial_values", fig, display=False)

optimization_problem = OptimizationProblem('transform_demo')
optimization_problem.add_variable(r'$\varepsilon_{\text{bed}}$', lb=0.1, ub=0.8, transform="linear")
optimization_problem.add_variable(r'$D_{\text{ax}}$', lb=1e-9, ub=1e-4, transform="log")

x0 = optimization_problem.create_initial_values(2*64)
pop = optimization_problem.create_population(x0)

fig, axs = setup_demo_axes(panel_width_in=DEMO_PANEL_WIDTH_IN)
pop.plot_pairwise(autoscale=True, ax=axs)
set_demo_marker_size(axs)
set_demo_limits(axs, DEMO_VARIABLE_BOUNDS)
fig.tight_layout()
glue("fig_initial_values_normalized", fig, display=False)
```

`````{grid}

````{grid-item}
:columns: 6

```{glue:figure} fig_initial_values
:name: fig_initial_values

Sampling without normalization: $D_{\text{ax}}$ values cluster near the upper bound, leaving the lower orders of magnitude nearly unexplored.
```
````

````{grid-item}
:columns: 6

```{glue:figure} fig_initial_values_normalized
:name: fig_initial_values_normalized

Sampling with log-normalization applied to $D_{\text{ax}}$ (logarithmic scale): coverage is near-uniform across the full five orders of magnitude.
```
````

`````

(variable_dependencies)=
### Variable dependencies

Variable dependencies allow complex interdependencies between parameters to be made explicit, enabling a more effective problem formulation.
Rather than optimizing in the original parameter space, it is often advantageous to reparametrize in terms of quantities that are more physically independent and better-conditioned for the optimizer.
Consider, for example, the adsorption rate constant $k_a$ and the desorption rate constant $k_d$: these two parameters are not independent, as the equilibrium behavior is governed by their ratio $K_{eq} = k_a / k_d$.
Optimizing $K_{eq}$ and a kinetic parameter such as $k_a$ directly is therefore more efficient than estimating $k_a$ and $k_d$ separately, since the two original parameters are strongly correlated {cite}`Heymann2022`.
CADET-Process supports such reparametrizations through user-defined dependency functions, which map the optimizer's variables to the physical parameters used during evaluation (see also {numref}`adsorption_parameters`).

(linear_constraints)=
### Linear constraints

Linear constraints restrict the feasible region through linear relationships between variables.
CADET-Process supports both inequality and equality linear constraints.
Inequality constraints take the form

```{math}
:label: linear_constraints_ineq

A_{\leq} \cdot x \leq b_{\leq},
```

and equality constraints take the form

```{math}
:label: linear_constraints_eq

A_{=} \cdot x = b_{=},
```

where $A$ is an $m \times n$ coefficient matrix whose entries define the linear combinations of variables involved in each constraint, $b$ is an $m$-dimensional vector specifying the corresponding bounds or target values, $m$ denotes the number of constraints, and $n$ the number of variables.
Inequality constraints are useful for enforcing ordering or proportionality relationships between variables.
Equality constraints fix specific linear relationships and can sharpen the feasible region considerably, but many optimizers, particularly evolutionary algorithms, encounter difficulties handling them {cite}`BarkatUllah2012`.
In practice, variable dependencies (see above) are often a more robust alternative: by explicitly encoding the constraint into the parametrization, the number of free variables is reduced and the constraint is satisfied by construction, with no need for slack variables or penalty handling.

(objectives_and_nonlinear_constraints)=
### Objectives and nonlinear constraints

Any callable function that accepts an input $x$ and returns objectives $f$ can be added to the {class}`~CADETProcess.optimization.OptimizationProblem`.
These functions often utilize process evaluation methods, such as product fractionation (see {numref}`fractionation`) or comparison with experimental data (see {numref}`comparison`).
As detailed in {numref}`multi_objective_optimization`, CADET-Process can also handle multi-objective optimization problems.
Additionally, any number of nonlinear constraint functions can be incorporated into the problem.

(evaluation_toolchains)=
### Evaluation toolchains

In many complex optimization cases, optimization variables cannot be passed directly into an objective or nonlinear constraint function.
Instead, a sequence of processing steps is required to derive the metrics computed by those functions.
Take, for example, the fitting of adsorption parameters (see {numref}`adsorption_parameters`): the optimization variables must first be mapped to the corresponding parameters of the binding model, which are deeply nested within the {class}`~CADETProcess.processModel.Process` object.
The process is then simulated, and the results are passed to the {class}`~CADETProcess.comparison.Comparator`, which computes difference metrics against experimental reference data (see {numref}`comparison`).
{numref}`evaluation_example_comparator` shows the steps typically required for this calculation.

```{figure} ./figures/evaluation_example_comparator.png
:name: evaluation_example_comparator
:width: 100%

Steps required for calculating difference metrics in a parameter estimation problem.
```

To manage the definition of such complex problems, CADET-Process introduces *Evaluation Toolchains*.
This concept refers to a sequence of processing steps that are executed at each optimizer call to compute the values of objective or nonlinear constraint functions.
These toolchains involve two main components: evaluation objects and evaluators.

An *Evaluation Object* wraps a model, such as a {class}`~CADETProcess.processModel.Process`, and is responsible for receiving the current optimization variable values and updating the corresponding model parameters before evaluation.
In the adsorption parameter fitting example, the {class}`~CADETProcess.processModel.Process` is registered as an evaluation object, and the path to each parameter to be updated is specified.
Multiple evaluation objects can be added for simultaneous optimization of different operating conditions.
Furthermore, a given optimization variable can be linked to either a single evaluation object or multiple evaluation objects, as detailed in {numref}`multiple_evaluation_objects`.

```{figure} ./figures/evalobj_multiple_variables.png
:name: multiple_evaluation_objects
:width: 30%

Relationship between optimization variables and evaluation objects.
Here, optimization variable $1$ is associated with both evaluation objects, while variable $2$ is specific to evaluation object $2$.
```

*Evaluators* form the processing chain between evaluation objects and the objective or constraint functions.
Any callable function can be used as an evaluator, provided it accepts the result of the previous step as its first argument and returns a single result object for subsequent processing.
To minimize redundant computations when multiple objectives or constraints share evaluation steps, CADET-Process internally caches intermediate results.
The full toolchain is illustrated in {numref}`evaluation_steps`.

```{figure} ./figures/evaluation_steps.png
:name: evaluation_steps
:width: 100%

Evaluation toolchain in CADET-Process.
Optimization variables $v$ are mapped to parameters of evaluation objects $e$ (e.g., a {class}`~CADETProcess.processModel.Process`), each of which is then passed through a chain of $s$ evaluators.
The final results are handed to the objective and nonlinear constraint functions $f$ and $g$, which return the metrics $m$.
The total number of metrics depends on the number of evaluation objects, objectives and nonlinear constraint functions, and metrics per function.
```

Callback functions can also be incorporated into the optimization problem to monitor progress.
A callback is a user-defined function invoked by the optimizer at the end of each generation, allowing intermediate results to be inspected, logged, or visualized.
Any function can serve as a callback, for instance to plot chromatograms or log intermediate results.
In single-objective optimization, the callback is called with the best individual found so far; in multi-objective optimization, it is called for every member of the current Pareto front.
Like objective and nonlinear constraint functions, callbacks are typically implemented using an evaluation toolchain (see {numref}`evaluation_steps` and {numref}`callbacks`).

```{figure} ./figures/callbacks_evaluation.png
:name: callbacks
:width: 100%

Evaluation of user-defined callbacks $c$ for each member $p$ of the Pareto front $X_{\text{Pareto}}$ in multi-objective optimization.
```

(meta_scores)=
### Meta scores and multi-criteria decision functions

In multi-objective optimization, the result is a set of Pareto-optimal solutions rather than a single optimum.
Selecting a preferred solution from this set is itself a decision problem, addressed by multi-criteria decision making (MCDM) methods.
To support this, CADET-Process allows additional metrics to be registered as *meta scores*.
Unlike objectives, meta scores are not passed to the optimizer and therefore do not influence the search; they are computed for each candidate alongside the objectives and stored in the results.
This is particularly useful when individual metrics, such as the NRMSE for each experimental dataset, are informative on their own but would inflate the objective space if used directly.
Instead, they can be aggregated into a single meta score and used to inform the MCDM step.

Once the Pareto front has been identified, multi-criteria decision functions can be applied to its members based on the objectives and any available meta scores.
CADET-Process provides several MCDM methods for this purpose, including weighted sum aggregation (see {numref}`multi_criteria_decision_function`).
These methods serve two related purposes: they can reduce a large Pareto front to a smaller representative subset, or, in the limit, collapse it to a single preferred solution.
The latter is equivalent to single-objective optimization, but with an important advantage: the weights are chosen after the full trade-off landscape has been explored, rather than committing to them before the optimization runs.

```{figure} ./figures/multi_criteria_decision_function.png
:name: multi_criteria_decision_function
:width: 100%

Processing of Pareto front $X_{\text{Pareto}}$ with meta scores and multi-criteria decision function to generate reduced Pareto front $X_{\text{Pareto}}^\prime$.
```

(optimizer)=
## Optimizer

The {class}`~CADETProcess.optimization.OptimizerBase` offers a unified interface for utilizing external optimization libraries.
It converts the {class}`~CADETProcess.optimization.OptimizationProblem` configuration into the specific API of the chosen external optimizer.
Currently, adapters for {class}`Pymoo <CADETProcess.optimization.PymooInterface>` {cite}`pymoo2020` and {class}`Scipy's <CADETProcess.optimization.SciPyInterface>` optimization suite {cite}`SciPyContributors2020` are available, both of which are released under open source licenses permitting academic and commercial use.

All optimizers share a common set of configuration options, including convergence criteria and tolerances for constraint violations.
CADET-Process also supports the parallel evaluation of candidates; in this case, the number of cores must be specified when the optimizer supports it.
Each optimizer implementation offers additional configuration options, such as the population size for a genetic algorithm.
The following example illustrates these features using a generic multi-objective optimization problem solved with {class}`~CADETProcess.optimization.U_NSGA3`, a genetic algorithm {cite}`Seada2016`.

```{math}
:label: optimization_problem_example

\min f(x) &= \begin{bmatrix}x_0^2 + x_1^2, (x_0-1)^2 + x_1^2\end{bmatrix} \\
\textrm{s.t.}
\quad -5 \leq &x_0 \leq 5, \\
\quad -5 \leq &x_1 \leq 5, \\
\quad x_1 &> x_0.
```

```{code-cell} ipython3
:tags: [remove-cell]

from CADETProcess.optimization import OptimizationProblem
from CADETProcess.optimization import U_NSGA3

def multi_objective_func(x):
    f1 = x[0]**2 + x[1]**2
    f2 = (x[0] - 1)**2 + x[1]**2
    return f1, f2

optimization_problem = OptimizationProblem('moo')

# Names double as axis labels, so they are written the way eq.
# `optimization_problem_example` writes them.
optimization_problem.add_variable(r'$x_0$', lb=-5, ub=5)
optimization_problem.add_variable(r'$x_1$', lb=-5, ub=5)

optimization_problem.add_linear_constraint([r'$x_0$', r'$x_1$'], [-1, 1], 0)

optimization_problem.add_objective(
    multi_objective_func,
    n_objectives=2,
    labels=[r'$f_0$', r'$f_1$'],
)

```

(initial_values)=
### Initial Values

Most optimization approaches are iterative in nature and require well-defined starting points for initiation.
The choice of initial values significantly impacts optimization success, with poor choices potentially leading to suboptimal solutions or convergence failure.
Ideally, initial values should be close to the true optimal values, respecting any constraints or bounds on the decision variables.
The {class}`~CADETProcess.optimization.OptimizationProblem` provides a method to generate initial values that accounts for variable normalization (see {numref}`variable_normalization`) and variable dependencies (see {numref}`variable_dependencies`).
For this purpose, **hopsy** {cite}`Paul2024` is used to uniformly sample the parameter space (see {numref}`uniform_samples`).
However, this method is effective only if all optimization variables have defined lower and upper bounds and primarily ensures that linear constraints are met.
Nonlinear constraints might not be satisfied by the generated samples, and incorporating nonlinear parameter dependencies can be challenging.
In such scenarios, users can input their own starting points, building on prior knowledge or results from other preprocessing steps like shortcut methods (refer to {numref}`shortcut_methods`).

```{code-cell} ipython3
:tags: [remove-cell]

import matplotlib.pyplot as plt

x0 = optimization_problem.create_initial_values(n_samples=1000)
pop = optimization_problem.create_population(x0)

fig, axs = setup_demo_axes(panel_width_in=DEMO_PANEL_WIDTH_IN)
pop.plot_pairwise(autoscale=True, ax=axs)
set_demo_marker_size(axs)
fig.tight_layout()
glue("uniform_samples", fig, display=False)
```

```{glue:figure} uniform_samples
:name: uniform_samples

Example for uniform sampling of parameter space with linear inequality constraints, used for initial values.
```

(optimization_results)=
### Optimization results

To start the optimization, the {class}`~CADETProcess.optimization.OptimizationProblem` is passed to the {meth}`~CADETProcess.optimization.OptimizerBase.optimize` method, which invokes the external optimizer and returns an {class}`~CADETProcess.optimization.OptimizationResults` object.
This includes:

- {attr}`~CADETProcess.optimization.OptimizationResults.exit_flag`: Information about the optimizer termination.
- {attr}`~CADETProcess.optimization.OptimizationResults.exit_message`: Additional information about the optimizer status.
- {attr}`~CADETProcess.optimization.OptimizationResults.n_evals`: Number of evaluations.
- {attr}`~CADETProcess.optimization.OptimizationResults.x`: Optimal points.
- {attr}`~CADETProcess.optimization.OptimizationResults.f`: Optimal objective values.
- {attr}`~CADETProcess.optimization.OptimizationResults.g`: Optimal nonlinear constraint values.

Moreover, multiple plot methods are provided to visualize the results.
{meth}`~CADETProcess.optimization.OptimizationResults.plot_objectives` shows the objective values as a function of the input variables (see {numref}`objectives`), {meth}`~CADETProcess.optimization.OptimizationResults.plot_pareto` provides a pairwise Pareto plot to visualize trade-offs between objectives (see {numref}`pareto`), and {meth}`~CADETProcess.optimization.OptimizationResults.plot_convergence` tracks the objective values against the number of function evaluations (see {numref}`convergence`).

```{code-cell} ipython3
:tags: [remove-cell]

optimizer = U_NSGA3()

optimization_results = optimizer.optimize(optimization_problem, save_results=False)

fig, axs = setup_demo_axes(share=False)
optimization_results.plot_objectives(autoscale=False, ax=axs)
set_demo_marker_size(axs)
fig.tight_layout()
glue("objectives", fig, display=False)
```

```{glue:figure} objectives
:name: objectives

Objective function values for all evaluated individuals.
Darker shades represent individuals evaluated in later generations.
The prominent minima are indicative of successful convergence.
```

```{code-cell} ipython3
:tags: [remove-cell]

fig, ax = setup_demo_axes()
optimization_results.plot_pareto(autoscale=False, ax=ax)
set_demo_marker_size(ax)
fig.tight_layout()
glue("pareto", fig, display=False)
```

```{raw} latex
% The chapter ends right after the convergence figure, with too little body text
% left to absorb two more floats. Left floating, the pair claims a whole float
% page and strands the outro on a near-empty page after it. Placing them inline
% instead lets the outro follow them on the same page.
\let\oldfigure\figure
\let\endoldfigure\endfigure
\renewenvironment{figure}[1][htbp]{\oldfigure[H]}{\endoldfigure}
```

```{glue:figure} pareto
:name: pareto

Pareto plot of all evaluated individuals.
```

```{code-cell} ipython3
:tags: [remove-cell]

fig, axs = setup_demo_axes(nrows=1, share=False, panel_in=CONVERGENCE_PANEL_IN)
# plot_convergence indexes a flat axes array, not a 2D grid.
optimization_results.plot_convergence(ax=axs[0])
# The default sets a multi-letter word in math italics.
for ax in axs[0]:
    ax.set_xlabel("Evaluations")
fig.tight_layout()
glue("convergence", fig, display=False)
```

```{glue:figure} convergence
:name: convergence

Convergence of the optimization algorithm: objective values plotted against the number of function evaluations.
```

```{raw} latex
\let\figure\oldfigure
\let\endfigure\endoldfigure
```

---

With the CADET-Process framework fully established, covering process configuration, simulation, performance evaluation, and optimization, the focus shifts to its practical application.
The following chapters demonstrate how these tools address real-world problems, starting with the characterization of a representative laboratory system (see {numref}`characterization`).
Subsequent optimization studies explore a range of advanced operating concepts (see {numref}`Chapter %s <operating_modes>`).

```{code-cell} ipython3
:tags: [remove-cell]

import os
from glob import glob
from shutil import rmtree

path = os.getcwd()
pattern = os.path.join(path, "results_*")

for item in glob(pattern):
    if not os.path.isdir(item):
        continue
    rmtree(item)
```
