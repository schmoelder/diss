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
```

(optimization)=
# Optimization

One of the main applications of **CADET-Process** is performing optimization studies.
Optimization refers to the selection of a solution with regard to some criterion.
In the simplest case, an optimization problem consists of minimizing some function $f(x)$ by systematically varying the input values $x$ and computing the value of that function.

$$
\min_x f(x)
$$

Examples for the application of optimization studies in the context of physico-chemical processes include process optimization and parameter estimation.
Here, often many variables are subject to optimization, multiple criteria have to be balanced, and additional linear and nonlinear constraints need to be considered.

$$
\min_x \quad f(x) \\
\textrm{s.t.} \quad &g(x) \le 0, \\
              \quad &h(x) = 0, \\
              \quad &x \in \mathbb{R}^n, \\
$$

where $g$ summarizes all inequality constraint functions, and $h$ equality constraints.

To decouple the problem formulation from the problem solution, two classes are provided:
An {class}`~CADETProcess.optimization.OptimizationProblem` class to specify optimization variables, objectives and constraints.
And an {class}`~CADETProcess.optimization.OptimizerBase` class which allows interfacing different external optimizers to solve the problem.
In the following, the {mod}`~CADETProcess.optimization` module of **CADET-Process** is introduced and core features are discussed.

(optimization_problem)=
## Optimization Problem

The {class}`~CADETProcess.optimization.OptimizationProblem` class is designed for defining optimization variables, objectives, and constraints.
It allows the addition of any number of variables, each with optional lower and upper bounds.

### Variable normalization

Optimization algorithms often face challenges when variables vary across multiple orders of magnitude, as this variability affects the relative importance of each parameter{cite}`Heymann2022`.
Consequently, normalizing parameters is crucial for improving the efficiency and accuracy of the optimization process, ensuring more reliable outcomes.
Normalization aids in equalizing the influence of each parameter on the objective function, leading to a more balanced search in the solution space.
This also reduces the risk of overlooking optimal solutions due to scale-induced biases.
For this purpose, **CADET-Process** allows the specification of linear and logarithmic variable normalization.

To illustrate this feature, consider the characterization of a chromatographic column (refer to {numref}`fit_column_transport`).
In this scenario, two parameters are being optimized: the bed porosity, which is expected to range between $0.1$ and $0.6$, and the axial dispersion, which ranges between $1 \cdot 10^{-10}$ and $1 \cdot 10^{-6}~m^2 \cdot s^{-1}$.
Given the large difference in their scales, the porosity can be normalized linearly, whereas the axial dispersion is more suitably normalized on a logarithmic scale.
This approach allows the optimizer to operate as if it was optimizing two variables that both range from $0$ and $1$.
Meanwhile, CADET-Process handles the back-transformation to their original scales for evaluation purposes.

@TODO: Add figure.

### Variable dependencies

Handling a large number of variables simultaneously can lead to high complexity, as the volume of the variable space grows exponentially with the number of variables.
Reducing the degrees of freedom simplifies the optimization process, leading to faster convergence and improved results.
One method to achieve this is by defining dependencies between individual variables, which can be done using different mechanisms such as linear combinations or custom functions.
For instance, when the same parameter is applied across multiple unit operations, the problem's variable count can be decreased by introducing a single variable.
This variable is then applied to the processes during pre-processing.
In other scenarios, the ratio between model parameters might be critical.
Consider the equilibrium constant $k_{eq} = k_a / k_d$ in an adsorption model, with $k_a$ as the adsorption rate and $k_d$ as the desorption rate.
Optimizing both $k_a$ and $k_d$ separately is less efficient than optimizing $k_a$ and $k_{eq}$ {cite}`Heymann2022`.
This method allows for the independent determination of equilibrium and kinetic parameters of the reaction (see also {numref}`fit_binding_parameters`).

### Linear constraints

Linear constraints are a common way to restrict the feasible region of an optimization problem.
They are typically defined using linear functions of the optimization:

$$
A \cdot x \leq b,
$$

where $A$ is an $m \times n$ coefficient matrix and $b$ is an $m$-dimensional vector and $m$ denotes the number of constraints, and $n$ the number of variables, respectively.
This method is especially useful for enforcing certain relationships between variables, like order or proportionality, ensuring solutions are mathematically optimal and practically viable.

Equality constraints are useful for setting specific solution conditions, thereby refining the feasible solution space.
However, many optimizers, particularly evolutionary algorithms, encounter difficulties with linear equality constraints {cite}`BarkatUllah2012`.
Therefore, it is often more practical to reduce the number of variables and manage equality constraints through variable dependencies, as previously discussed.

### Objectives and nonlinear constraints

Any callable function that accepts an input $x$ and returns objectives $f$ can be added to the {class}`~CADETProcess.optimization.OptimizationProblem`.
These functions often utilize process evaluation methods, such as product fractionation (see {numref}`fractionation`) or comparison with experimental data (see {numref}`comparison`).
As detailed in {numref}`multi_objective_optimization`, **CADET-Process** can also handle multi-objective optimization problems.
Additionally, any number of nonlinear constraint functions can be incorporated into the problem.

(evaluation_toolchains)=
### Evaluation toolchains

In many complex optimization cases, optimization variables cannot be directly inputted into an objective or nonlinear constraint function.
Instead, a sequence of processing steps is required to derive the final values or metrics computed by these functions.
Take, for example, the fitting of adsorption parameters (see {numref}`fit_binding_parameters`).
Here, the parameters are deeply nested within the {class}`~CADETProcess.processModel.Process` object, specifically as part of the binding model in one of the unit operations of the process flow sheet.
Consequently, the optimization variable must be mapped to the corresponding parameter.
Before calculating objectives, the process needs to be simulated, and the simulation results have to be passed to the {class}`~CADETProcess.comparison.Comparator` to compute the residual by comparing the output with experimental reference data (refer to {numref}`comparison`).
{numref}`evaluation_example_comparator` shows the steps required for calculating the difference metrics.

```{figure} ./figures/evaluation_example_comparator.png
:name: evaluation_example_comparator

Steps required for calculating difference metrics, used as residual in an optimization problem.
```

To simplify the definition of such complex problems, **CADET-Process** introduces *Evaluation Toolchains*.
This concept refers to a sequence of preprocessing steps that are essential for calculating the values of objective or nonlinear constraint functions.
These toolchains involve two main components: evaluation objects and evaluators.

An evaluation object is responsible for managing an optimization variable's value within an optimization problem.
In the example provided, before incorporating optimization variables into the {class}`~CADETProcess.optimization.OptimizationProblem`, it is essential to register the {class}`~CADETProcess.processModel.Process` as an evaluation object and specify the path to the parameter to be updated during optimization.
Multiple evaluation objects can be added for simultaneous optimization of different operating conditions.
Furthermore, a given optimization variable can be linked to either a single evaluation object or multiple evaluation objects, as detailed in {numref}`multiple_evaluation_objects`.

```{figure} ./figures/evalobj_multiple_variables.png
:name: multiple_evaluation_objects
:height: 100px

Relationship between optimization variables and evaluation objects.
Here, optimization variable $1$ is associated with both evaluation objects, while variable $2$ is specific to evaluation object $2$.
```

Before integrating the objective and nonlinear constraint functions into the {class}`~CADETProcess.optimization.OptimizationProblem,` it is necessary to add further processing steps as evaluators.
Any callable function can be used as an evaluator, provided it takes the result of the previous step as its first argument and returns a single result object for subsequent processing.
To enhance efficiency, CADET-Process internally caches intermediate results.
This approach minimizes redundant computations in other objectives or constraints that involve similar evaluation steps.
The application of this approach is illustrated in {numref}`evaluation_steps`.

```{figure} ./figures/evaluation_steps.png
:name: evaluation_steps

Evaluation toolchain in **CADET-Process**.
Optimization variables $v$ are associated with parameters of an evaluation object $e$, (e.g., a {class}`~CADETProcess.processModel.Process`).
The evaluation objects are then passed to a chain of evaluators $s$ which process the input and return results.
This procedure is repeated until the last results of the toolchain are handed to the objective / nonlinear constraint function(s) $f$ / $g$ which determine the final metrics $m$ of the corresponding objective or nonlinear constraint function.
Note that the total number of metrics depends on the number of evaluation objects, number of objectives / nonlinear constraint functions, as well as the number of metrics per objective / nonlinear constraint function.
```

To facilitate monitoring of the optimization progress, callback functions can be incorporated into the optimization problem.
These functions enable direct user interaction with the optimization process, allowing for additional reporting or manual interventions.
For instance, a simple callback function might be employed for plotting chromatograms.
In single-objective optimization, the function is called with the best individual, whereas in multi-objective optimization, it is executed for every member of the Pareto front.
Similar to objective and nonlinear constraint functions, callbacks usually involve the implementation of an evaluation toolchain (see {numref}`evaluation_steps`).

```{figure} ./figures/callbacks_evaluation.png
:name: callbacks

Evaluation of user-defined callbacks $c$.
The evalution toolchain is performed for every element in the Pareto front $p$.
```

(optimizer)=
## Optimizer

The {class}`~CADETProcess.optimization.OptimizerBase` offers a unified interface for utilizing external optimization libraries.
It converts the {class}`~CADETProcess.optimization.OptimizationProblem` configuration into the specific API of the chosen external optimizer.
Currently, adapters for {class}`Pymoo <CADETProcess.optimization.PymooInterface>` {cite}`pymoo2020` and {class}`Scipy's <CADETProcess.optimization.SciPyInterface>` optimization suite {cite}`SciPyContributors2020` are available, both of which are released under open source licenses permitting academic and commercial use.

Before starting the optimization, the optimizer must be initialized and configured.
Some options are universal across all optimizers, including convergence criteria and tolerances for constraint violations.
**CADET-Process** also facilitates the parallel evaluation of candidates; in this case, the number of cores to be used must be specified, i.e., if the optimizer supports parallel evaluation.
Each optimizer implementation offers additional configuration options, such as the population size for a genetic algorithm.

To highlight some of the optimizer's features, consider the following (generic) multi-objective optimization problem which is solved using {class}`~CADETProcess.optimization.U_NSGA3`, a genetic algorithm {cite}`Seada2016`.

$$
\min f(x) &= \begin{bmatrix}x_0^2 + x_1^2, (x_0-1)^2 + x_1^2\end{bmatrix} \\
\textrm{s.t.}
\quad -5 \leq &x_0 \leq 5, \\
\quad -5 \leq &x_1 \leq 5, \\
\quad x_1 &> x_0.
$$

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

### Initial Values

Most optimization approaches are iterative in nature and require well-defined starting points for initiation.
The choice of initial values significantly impacts optimization success, with poor choices potentially leading to suboptimal solutions or convergence failure.
Ideally, initial values should closely approximate the true optimal values, considering any constraints or bounds on the decision variables.
To facilitate the definition of starting points, the {class}`~CADETProcess.optimization.OptimizationProblem` provides a method to generate initial values.
For this purpose, **hopsy** {cite}`Paul2024` is used to efficiently (uniformly) sample the parameter space (see {numref}`uniform_samples`).
However, this method is effective only if all optimization variables have defined lower and upper bounds and primarily ensures that linear constraints are met.
Nonlinear constraints might not be satisfied by the generated samples, and incorporating nonlinear parameter dependencies can be challenging.
In such scenarios, users can input their own starting points, building on prior knowledge or results from other preprocessing steps like shortcut methods (refer to {numref}`shortcut_methods`).

```{code-cell} ipython3
:tags: [remove-cell]

import matplotlib.pyplot as plt

x = optimization_problem.create_initial_values(n_samples=1000)

fig, ax = plt.subplots()
ax.scatter(x[:, 0], x[:, 1])
ax.set_xlabel(r'$x_0$')
ax.set_ylabel(r'$x_1$')
fig.tight_layout()

glue("uniform_samples", fig, display=False)
```

```{glue:figure} uniform_samples
:name: uniform_samples
:figwidth: 200px

Example for uniform sampling of parameter space with linear inequality constraints, used for initial values.
```

### Optimization results

To start the optimization, the {class}`~CADETProcess.optimization.OptimizationProblem` needs to be passed to the {class}`Optimizer's <CADETProcess.optimization.OptimizerBase>` {meth}`~CADETProcess.optimization.OptimizerBase.optimize()` method, which internally calls the external optimizer.
After optimization, a {class}`~CADETProcess.optimization.OptimizationResults` object contains the results of the optimization.
This includes:

- {attr}`~CADETProcess.optimization.OptimizationResults.exit_flag`: Information about the optimizer termination.
- {attr}`~CADETProcess.optimization.OptimizationResults.exit_message`: Additional information about the optimiz status.
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

figs, axs = optimization_results.plot_objectives()
glue("objectives", figs[0], display=False)
```

```{glue:figure} objectives
:name: objectives
:figwidth: 300px

Objective function values for all evaluated individuals.
Darker shades represent individuals evaluated in later generations.
The prominent minima indicative a successful converging towards the minima.
```

The {meth}`~CADETProcess.optimization.OptimizationResults.plot_pareto` method shows a pairwise Pareto plot, where each objective is plotted against every other objective in a scatter plot, allowing for a visualization of the trade-offs between the objectives (see {numref}`pareto`).

```{code-cell} ipython3
:tags: [remove-cell]

fig, ax = optimization_results.plot_pareto()
glue("pareto", fig, display=False)
```

```{glue:figure} pareto
:name: pareto
:figwidth: 150px

Pareto plot of all evaluated individuals.
```

The {meth}`~CADETProcess.optimization.OptimizationResults.plot_convergence` method is a tool for visualizing the convergence of the optimization over time, where the objective value is plotted against the number of function evaluations (see {numref}`convergence`).

```{code-cell} ipython3
:tags: [remove-cell]

figs, axs = optimization_results.plot_convergence()
glue("convergence", figs[0], display=False)
```

```{glue:figure} convergence
:name: convergence
:figwidth: 300px

Optimization algorithm progresses towards a solution over time.
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
