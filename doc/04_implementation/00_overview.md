(overview)=
# Implementation of the CADET-Process framework

**CADET-Process** is a Python framework developed in this work for the modeling, simulation, and optimization of chromatographic processes.
The source code is freely available on [*GitHub*](https://github.com/fau-advanced-separations/CADET-Process) {cite}`CADET-Process_source`, and a scientific paper describing its design and application has been published in [*MDPI Processes*](https://doi.org/10.3390/pr8010065) {cite}`Schmoelder2020`.
*Python* was chosen as the implementation language due to its widespread adoption in the scientific community and the easy integration of numerical and scientific packages, making it well suited for the modular approach adopted in this work.
CADET-Process is available on the *Python Package Index* ([*PyPI*)](https://pypi.org/project/CADET-Process) and can be installed via `pip` {cite}`CADET-Process_pypi`.

```bash
pip install cadet-process
```

The [CADET-Core](https://cadet.github.io) simulator is a robust numerical engine that can simulate a wide range of physico-chemical models used in chromatography and other biochemical processes {cite}`Leweke2018`.
However, the configuration files of CADET-Core can be long and difficult to work with, particularly for integrated processes involving multiple unit operations.
Moreover, the structure of these files may change during process optimization, such as when the sequence of dynamic events is altered, making direct use of CADET-Core challenging without an additional layer of abstraction.
CADET-Process addresses this by providing an object-oriented model builder that simplifies process setup, gives convenient access to all model parameters, automatically validates their values, and sets defaults where appropriate, reducing the risk of ill-defined configuration files.

CADET-Process simplifies the modeling of complex chromatographic operations, including elaborate switching schemes, advanced gradients, recycling systems, and multi-column setups.
It facilitates the definition of dynamic changes in flow sheet connectivity or time-dependent parameters.
Additionally, the package includes routines for evaluating cyclic stationarity of processes and determining optimal fractionation times, aiding in the assessment of performance indicators such as yield, purity, and productivity.
Its ability to configure complex optimization problems, including the definition of multi-objective functions and the integration of nonlinear constraint functions, is crucial for a comprehensive optimization approach.

This chapter introduces the core software architecture of CADET-Process and provides practical demonstrations of setting up chromatographic processes, simulation techniques, and tools for the evaluation of results.
It also showcases how to configure optimization problems for the design of chromatographic processes.
For a more comprehensive documentation, please visit the [CADET-Process documentation website](https://cadet-process.readthedocs.io/) {cite}`CADET-Process_documentation`.

The framework follows a sequential workflow: a process is first configured, then simulated, the results evaluated, and finally an optimizer uses those evaluations to improve the process design.
An overview of the corresponding modules and their relations is given in {numref}`framework_overview`.

```{figure} ./figures/framework_overview.png
:name: framework_overview

Overview of the framework modules and their relations.
White boxes represent input configurations and solution objects, blue boxes represent internal tools and procedures, green boxes represent external tools, and the orange box represents the core process model.
```

The {class}`~CADETProcess.processModel.Process` class is an abstract representation of the chromatographic process configuration including the operational and design parameters.
Processes can be simulated using a {class}`Simulator <CADETProcess.simulator.SimulatorBase>` which solves the underlying equations.
The {class}`Simulator <CADETProcess.simulator.SimulatorBase>` adapter acts as an abstract interface to external solvers (e.g. CADET-Core) and translates the internal configuration to the corresponding format of the solver.
After the computation is finished, the {class}`~CADETProcess.simulationResults.SimulationResults` are returned and can be further evaluated (see {numref}`process_simulation`).
If a {class}`~CADETProcess.stationarity.StationarityEvaluator` is configured to test for cyclic stationarity, more chromatographic cycles are simulated until stationarity is reached (see {numref}`stationarity`).

Different modules are provided that process the {class}`~CADETProcess.simulationResults.SimulationResults`.
For example, {class}`~CADETProcess.simulationResults.SimulationResults` can be compared to experimental data or other simulation results using the {class}`~CADETProcess.comparison.Comparator` class, which computes residuals such as the sum of squared errors (see also {numref}`comparison`).
Additionally, key process performance indicators, including purity, yield, and productivity (see {numref}`fractionation`), can be calculated by the {mod}`~CADETProcess.fractionation` module, which automatically determines fractionation times of the simulated chromatograms.

These metrics can be used as objectives in an {class}`~CADETProcess.optimization.OptimizationProblem`, which serves to configure optimization studies.
Any process parameter can be added as an optimization variable and the provided evaluation methods can be used to construct objectives and constraint functions.
This enables many different scenarios such as process optimization and parameter estimation.
The abstract {class}`Optimizer <CADETProcess.optimization.OptimizerBase>` provides a unified interface to external optimization algorithms such as the genetic algorithm {class}`U-NSGA-3 <CADETProcess.optimization.U_NSGA3>` (see {numref}`optimization`).
