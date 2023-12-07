(overview)=
# Implementation of the CADET-Process framework

The software built for this work was released under the name **CADET-Process**.
The source code is freely available on [*GitHub*](https://github.com/fau-advanced-separations/CADET-Process), and a scientific paper was published in [*MDPI Processes*](https://doi.org/10.3390/pr8010065) {cite}`Schmoelder2020`.
The framework is written in Python, a free and open-source programming language that gained a lot of popularity in the scientific community in recent years.
One of the main advantages of Python is the easy integration of other scientific and numerical packages.
This makes it especially useful for a modular approach such as the one presented.
The following figure gives a general overview of the program structure and workflow.

The [**CADET**](https://cadet.github.io) core simulator is a very powerful numerical engine that can simulate a large variety of physico-chemical models used in chromatography and other biochemical processes {cite}`Leweke2018`.
However, the configuration files of **CADET** can be complex and difficult to work with.
This is especially relevant when multiple unit operations are involved which is often the case for complex integrated processes.
Moreover, the structure of the configuration file may change during process optimization, for example when the order of dynamic events changes, making the direct use of **CADET** impossible without another layer of abstraction.

In this context [**CADET-Process**](https://cadet-process.readthedocs.io/en/latest/) was developed.
The package facilitates modeling processes using an object oriented model builder.
This interface layer provides convenient access to all model parameters in the system.
It automatically checks validity of the parameter values and sets reasonable default values where possible.
This simplifies the setup of **CADET** simulations and reduces the risk of ill-defined configurations files.

```{figure} ./figures/framework_overview.png
:name: framework_overview

Overview of the framework modules and their relations.
White boxes represent input configurations and solution objects, blue boxes internal tools and procedures, and green boxes external tools.
For a detailed explanation, see text.
```

An overview of the framework's modules and their relations is depicted in {numref}`framework_overview`.
The {class}`~CADETProcess.processModel.Process` is an abstract representation of the chromatographic process configuration including the operational and design parameters.
Processes can be simulated using a {class}`Simulator <CADETProcess.simulator.SimulatorBase>` which solves the underlying equations.
The {class}`Simulator <CADETProcess.simulator.SimulatorBase>` adapter acts as an abstract interface to external solvers (e.g. **CADET**) and translates the internal configuration to the corresponding format of the solver.
After the computation is finished, the {class}`~CADETProcess.simulationResults.SimulationResults` are returned and can be further evaluated (see {numref}`simulation_guide`).
If a {class}`~CADETProcess.stationarity.StationarityEvaluator` is configured to test for cyclic stationarity, more chromatographic cycles are be simulated until stationarity is reached (see {numref}`stationarity_guide`).

For processing the {class}`~CADETProcess.simulationResults.SimulationResults`, different modules are provided.
For example, they can be compared to experimental data (or other simulations) using a {class}`~CADETProcess.comparison.Comparator` which computes residuals such as the sum of squared errors (see also {numref}`comparison_guide`).
Moreover, the {class}`~CADETProcess.fractionation.Fractionator` module automatically determines fractionation times of the simulated chromatograms and determines process performance indicators such as purity, yield, and productivity (see {numref}`fractionation_guide`).

These metrics can be used as objectives in an {class}`~CADETProcess.optimization.OptimizationProblem` class which serves to configure optimization studies.
Here, any process parameter can be added as optimization variable and the evaluation methods can be used to construct objectives and constraint functions.
This enables many different scenarios such as process optimization and parameter estimation.
Again, an abstract {class}`Optimizer <CADETProcess.optimization.OptimizerBase>` provides an interface to external optimization algorithms such as {class}`U-NSGA-3 <CADETProcess.optimization.U_NSGA3>` (see {numref}`optimization_guide`).
