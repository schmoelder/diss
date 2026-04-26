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

\min_x f(x)
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

Optimization algorithms often struggle when variables span multiple orders of magnitude, as this variability affects the relative influence of each parameter on the objective function {cite}`Heymann2022`.
To address this, parameter normalization is essential.
It improves the efficiency and accuracy of the optimization process by ensuring a more balanced exploration of the solution space and reducing the risk of scale-induced biases.

Normalization helps equalize the contribution of each parameter, leading to a more uniform search and a greater likelihood of identifying optimal solutions.
To support this, CADET-Process allows for both linear and logarithmic normalization of variables.
The linear normalization maps the variable space from the lower and upper bound to a range between $0$ and $1$ by applying the following transformation:

```{math}
:label: linear_normalization

x^\prime = \frac{x - x_{lb}}{x_{ub} - x_{lb}}
```

The log normalization maps the variable space from the lower and upper bound to a range between $0$ and $1$ by applying the following transformation:

```{math}
:label: log_normalization

x^\prime = \frac{log \left( \frac{x}{x_{lb}} \right) }{log \left( \frac{x_{ub} }{x_{lb}} \right) }
```

Consider the characterization of a chromatographic column (refer also to {numref}`characterization`), where two parameters are optimized:

- **Bed porosity**, ranging from $0.1$ to $0.8$
- **Axial dispersion**, ranging from $1 \times 10^{-9}$ to $1 \times 10^{-4}~\text{m}^2~\text{s}^{-1}$.

Due to this disparity in scales, porosity is best normalized linearly, while axial dispersion benefits from logarithmic normalization.
As illustrated in {numref}`fig_initial_values`, sampling without normalization is biased toward the upper end of the axial dispersion range, with few samples drawn near the lower bound of $1 \times 10^{-9}~\text{m}^2~\text{s}^{-1}$.
In contrast, {numref}`fig_initial_values_normalized` shows that normalization results in more uniform coverage across the full parameter range, an important characteristic for generating effective initial values (see {numref}`initial_values`).
This normalization strategy allows the optimizer to work within a consistent domain, effectively optimizing two variables that both range from $0$ to $1$, while CADET-Process handles the inverse transformation back to the original scales for evaluation purposes.

```{code-cell} ipython3
:tags: [remove-cell]

from CADETProcess.optimization import OptimizationProblem

optimization_problem = OptimizationProblem('no_transform_demo')
optimization_problem.add_variable(r'$\varepsilon_{\text{bed}}$', lb=0.1, ub=0.8)
optimization_problem.add_variable(r'$D_{\text{ax}}$', lb=1e-9, ub=1e-4)

x0 = optimization_problem.create_initial_values(2*64)
pop = optimization_problem.create_population(x0)

fig, _ = pop.plot_pairwise(autoscale=True)
glue("fig_initial_values", fig, display=False)

optimization_problem = OptimizationProblem('transform_demo')
optimization_problem.add_variable(r'$\varepsilon_{\text{bed}}$', lb=0.1, ub=0.8, transform="linear")
optimization_problem.add_variable(r'$D_{\text{ax}}$', lb=1e-9, ub=1e-4, transform="log")

x0 = optimization_problem.create_initial_values(2*64)
pop = optimization_problem.create_population(x0)

fig, _ = pop.plot_pairwise(autoscale=True)
glue("fig_initial_values_normalized", fig, display=False)
```

`````{grid}

````{grid-item}
:columns: 6

```{glue:figure} fig_initial_values
:name: fig_initial_values
:scale: 50%

Uniform sampling of 128 parameter combinations in the unnormalized parameter space.
```
````

````{grid-item}
:columns: 6

```{glue:figure} fig_initial_values_normalized
:name: fig_initial_values_normalized
:scale: 50%

Uniform sampling of 128 parameter combinations in normalized parameter space.
```
````

`````

(variable_dependencies)=
### Variable dependencies

Handling a large number of variables simultaneously can lead to high complexity, as the volume of the variable space grows exponentially with the number of variables.
Reducing the degrees of freedom simplifies the optimization process, leading to faster convergence and improved results.
One method to achieve this is by defining dependencies between individual variables, which can be done using different mechanisms such as linear combinations or custom functions.
Consider, for example, the equilibrium constant $K_{eq} = k_a / k_d$ in an adsorption model, with $k_a$ as the adsorption rate and $k_d$ as the desorption rate.
Optimizing both $k_a$ and $k_d$ separately is less efficient than optimizing $k_a$ and $k_{eq}$ {cite}`Heymann2022`.
This method allows for the independent determination of equilibrium and kinetic parameters of the reaction (see also {numref}`adsorption_parameters`).

(linear_constraints)=
### Linear constraints

Linear constraints are a common way to restrict the feasible region of an optimization problem.
They are typically defined using linear functions of the optimization:

```{math}
:label: linear_constraints

A \cdot x \leq b,
```

where $A$ is an $m \times n$ coefficient matrix, $b$ is an $m$-dimensional vector, $m$ denotes the number of constraints, and $n$ the number of variables.
This method is especially useful for enforcing certain relationships between variables, like order or proportionality, ensuring solutions are mathematically optimal and practically viable.

Equality constraints are useful for setting specific solution conditions, thereby refining the feasible solution space.
However, many optimizers, particularly evolutionary algorithms, encounter difficulties with linear equality constraints {cite}`BarkatUllah2012`.
Therefore, it is often more practical to reduce the number of variables and manage equality constraints through variable dependencies, as previously discussed.

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
Take, for example, the fitting of adsorption parameters (see {numref}`adsorption_parameters`).
Here, the parameters are deeply nested within the {class}`~CADETProcess.processModel.Process` object, specifically as part of the binding model in one of the unit operations of the process flow sheet.
There, each optimization variable must be mapped to the corresponding model parameter.
Before calculating objectives, the process needs to be simulated, and the simulation results have to be passed to the {class}`~CADETProcess.comparison.Comparator` to compute the difference metrics by comparing the output with experimental reference data (see {numref}`comparison`).
{numref}`evaluation_example_comparator` shows the steps typically required for this calculation.

```{figure} ./figures/evaluation_example_comparator.png
:name: evaluation_example_comparator
:scale: 50%

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
:scale: 25%

Relationship between optimization variables and evaluation objects.
Here, optimization variable $1$ is associated with both evaluation objects, while variable $2$ is specific to evaluation object $2$.
```

*Evaluators* form the processing chain between evaluation objects and the objective or constraint functions.
Any callable function can be used as an evaluator, provided it accepts the result of the previous step as its first argument and returns a single result object for subsequent processing.
To minimize redundant computations when multiple objectives or constraints share evaluation steps, CADET-Process internally caches intermediate results.
The full toolchain is illustrated in {numref}`evaluation_steps`.

```{figure} ./figures/evaluation_steps.png
:name: evaluation_steps
:scale: 25%

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
:scale: 25%

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

Processing of Pareto front $X_{\text{Pareto}}$ with meta scores and multi-criteria decision function to generate reduced Pareto front $X_{\text{Pareto}}^\prime$.
```

(optimizer)=
## Optimizer

The {class}`~CADETProcess.optimization.OptimizerBase` offers a unified interface for utilizing external optimization libraries.
It converts the {class}`~CADETProcess.optimization.OptimizationProblem` configuration into the specific API of the chosen external optimizer.
Currently, adapters for {class}`Pymoo <CADETProcess.optimization.PymooInterface>` {cite}`pymoo2020` and {class}`Scipy's <CADETProcess.optimization.SciPyInterface>` optimization suite {cite}`SciPyContributors2020` are available, both of which are released under open source licenses permitting academic and commercial use.

Before starting the optimization, the optimizer must be initialized and configured.
Some options are universal across all optimizers, including convergence criteria and tolerances for constraint violations.
CADET-Process also facilitates the parallel evaluation of candidates; in this case, the number of cores to be used must be specified, i.e., if the optimizer supports parallel evaluation.
Each optimizer implementation offers additional configuration options, such as the population size for a genetic algorithm.

To highlight some of the optimizer's features, consider the following (generic) multi-objective optimization problem which is solved using {class}`~CADETProcess.optimization.U_NSGA3`, a genetic algorithm {cite}`Seada2016`.

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

optimization_problem.add_variable('x_0', lb=-5, ub=5)
optimization_problem.add_variable('x_1', lb=-5, ub=5)

optimization_problem.add_linear_constraint(['x_0', 'x_1'], [-1, 1], 0)

optimization_problem.add_objective(multi_objective_func, n_objectives=2)

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

fig, _ = pop.plot_pairwise(autoscale=True)
glue("uniform_samples", fig, display=False)
```

```{glue:figure} uniform_samples
:name: uniform_samples
:scale: 50%

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
The {meth}`~CADETProcess.optimization.OptimizationResults.plot_objectives` method shows the values of all objectives as a function of the input variables (see {numref}`objectives`).

```{code-cell} ipython3
:tags: [remove-cell]

optimizer = U_NSGA3()

optimization_results = optimizer.optimize(optimization_problem, save_results=False)

fig, axs = optimization_results.plot_objectives(autoscale=False)
glue("objectives", fig, display=False)
```

```{glue:figure} objectives
:name: objectives
:scale: 50%

Objective function values for all evaluated individuals.
Darker shades represent individuals evaluated in later generations.
The prominent minima are indicative of successful convergence.
```

The {meth}`~CADETProcess.optimization.OptimizationResults.plot_pareto` method shows a pairwise Pareto plot, where each objective is plotted against every other objective in a scatter plot, allowing for a visualization of the trade-offs between the objectives (see {numref}`pareto`).

```{code-cell} ipython3
:tags: [remove-cell]

fig, ax = optimization_results.plot_pareto()
glue("pareto", fig, display=False)
```

```{glue:figure} pareto
:name: pareto
:scale: 50%

Pareto plot of all evaluated individuals.
```

The {meth}`~CADETProcess.optimization.OptimizationResults.plot_convergence` method visualizes the convergence of the optimization, plotting the objective value against the number of function evaluations (see {numref}`convergence`).

```{code-cell} ipython3
:tags: [remove-cell]

fig, axs = optimization_results.plot_convergence()
glue("convergence", fig, display=False)
```

```{glue:figure} convergence
:name: convergence
:scale: 50%

Convergence of the optimization algorithm: objective values plotted against the number of function evaluations.
```

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
