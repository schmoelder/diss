---
jupytext:
  text_representation:
    format_name: myst
kernelspec:
  display_name: Python 3
  name: python3
execution:
  timeout: 300
---

```{code-cell} ipython3
:tags: [remove-cell]

from myst_nb import glue
%config InlineBackend.figure_format = 'retina'
```

(process_simulation)=
# Process Simulation

Once a {class}`~CADETProcess.processModel.Process` is configured, it can be passed to a simulator to solve the underlying model equations numerically.
The chromatographic models introduced in {numref}`model_formulation` are solved using the methods described in {numref}`model_solution`.
Following the Adapter pattern introduced in {numref}`design_patterns`, CADET-Process defines a {class}`~CADETProcess.simulator.SimulatorBase` interface, while the concrete {class}`~CADETProcess.simulator.Cadet` implementation translates the internal process representation into the input format of CADET-Core and invokes it.
Currently, CADET-Core is the only supported backend, although the adapter interface is designed to accommodate other solvers.
CADET-Core must be installed separately via *conda*:

```bash
conda install -c conda-forge cadet
```

Further details are provided in the {ref}`CADET-Core Documentation <cadet:contents>` {cite}`CADET-Core_documentation`.

This chapter covers three aspects of process simulation.
First, the solver configuration parameters are described, including tolerance settings that control the accuracy of the adaptive time stepping scheme.
Second, the structure of the {class}`~CADETProcess.simulationResults.SimulationResults` object returned after a successful simulation is introduced.
Third, the cyclic stationarity detection mechanism is presented, which allows the simulator to automatically run a process until a periodic steady state is reached.

## Solver configuration

The simulator exposes several configuration parameters that control numerical accuracy and performance.
While reasonable defaults are set for all parameters, adjustments may be necessary for specific use cases.
CADET-Core employs adaptive time stepping, dynamically adjusting the step size based on an error estimate (see {numref}`time_integration`): the step size decreases when the error exceeds a specified tolerance and increases when it is smaller.
Adjusting the absolute and relative tolerances is therefore the most common configuration change, balancing accuracy against computational cost.
A full reference of available parameters is provided in the CADET-Process documentation {cite}`CADET-Process_documentation`.

(simulation_results)=
## Simulation results

To run the simulation, the {class}`~CADETProcess.processModel.Process` needs to be passed to the {meth}`~CADETProcess.simulator.Cadet.simulate` method which then internally calls CADET-Core.
After the simulation is completed, a {class}`~CADETProcess.simulationResults.SimulationResults` object is returned, which contains the results of the simulation.
This includes:

- `exit_code`: Information about the solver termination.
- `exit_message`: Additional information about the solver status.
- `time_elapsed`: Execution time of simulation.
- `n_cycles`: Number of cycles that were simulated.
- `solution`: Complete solution of all cycles.
- `solution_cycles`: Solution of individual cycles.

Concentration profiles for each unit operation are stored as instances of the {attr}`~CADETProcess.solution.SolutionBase` class.
This class provides methods for interpolating, plotting, and integrating the solution.
By default, it stores only the inlet and outlet profiles of each unit.
The unit's {mod}`~CADETProcess.processModel.solutionRecorder` can be adjusted to store additional solution types, such as bulk or solid phase concentrations.
For instance, {numref}`chromatogram` was generated using the plot method of the {class}`~CADETProcess.solution.SolutionIO` class.
In addition, the results object stores meta-information such as the volumes of eluent and solid phase ($V_{\text{eluent}}$, $V_{\text{solid}}$) and the number of feed injections ($n_{\text{feed}}$), which are required for calculating key performance indicators (see {numref}`fractionation`).

(stationarity)=
## Cyclic stationarity

Preparative chromatographic separations are often operated in a repetitive fashion.
In particular, processes that incorporate the recycling of streams, like MR-SSR or SMB, have a distinct startup behavior that takes multiple cycles until a periodic steady state is reached {cite}`SchmidtTraub2020`.
In conventional batch chromatography as well, several cycles are needed to attain stationarity in optimized situations where there is a cycle-to-cycle overlap of the elution profiles of consecutive injections.
For this reason, the simulator is capable of simulating a process either for a fixed number of cycles or until cyclic stationarity has been reached.

To automatically simulate until stationarity is reached, a {class}`~CADETProcess.stationarity.StationarityEvaluator` can be configured and added to the process simulator (see {numref}`framework_overview`).
As the simulation continues over multiple cycles, the final state of one cycle serves as the initial state for the next, until the differences fall below a predefined threshold.
Criteria such as the maximum absolute deviation in concentration profiles or the peak areas between consecutive cycles can be specified {cite}`Holmqvist2015`.
For process performance evaluation, only the last cycle is analyzed, as it provides representative key performance indicators of the process's behavior in subsequent cycles (see also {numref}`fractionation`).

To illustrate this concept, consider an MR-SSR process (see {numref}`mrssr` for the complete process configuration).
In this example, the stationarity criterion evaluates the relative change in the integrated concentration profile areas and NRMSEs between successive cycles, using data from all unit operation inlets and outlets.
The metric classes for this purpose are provided by the {mod}`~CADETProcess.comparison` module, which offers a unified set of reusable metrics for quantifying differences between chromatographic profiles {cite}`Heymann2022`.
The simulation terminates when both the relative change in area and NRMSE fall below $0.1~\%$, or when a maximum number of cycles is reached as a safety limit.
{numref}`chromatogram_stationarity` displays the concentration profile at the column outlet across all cycles.
The initial startup behavior is visible on the left side of the profile, while later cycles show no significant visual differences, indicating cyclic stationarity.
In this scenario, the evaluator stopped the simulator after {glue:text}`n_cycles` cycles.

```{code-cell} ipython3
:tags: [remove-cell]

from examples.recycling.mrssr_process import process

process.flow_sheet.tank.c = [0, 0]

from CADETProcess.stationarity import StationarityEvaluator
evaluator = StationarityEvaluator()

from CADETProcess.stationarity import RelativeArea
criterion = RelativeArea()
criterion.threshold = 1e-3

evaluator.add_criterion(criterion)

from CADETProcess.simulator import Cadet
process_simulator = Cadet()

process_simulator.stationarity_evaluator = evaluator
process_simulator.evaluate_stationarity = True
process_simulator.n_cycles_min = 10
process_simulator.n_cycles_max = 100

simulation_results = process_simulator.simulate(process)

glue("n_cycles", simulation_results.n_cycles)

fig, ax = simulation_results.solution.column.outlet.plot()
glue("chromatogram_stationarity", fig, display=False)
```

```{glue:figure} chromatogram_stationarity
:name: chromatogram_stationarity
:scale: 100%

Concentration profile at the column outlet across {glue:text}`n_cycles` simulated cycles, showing the startup transient and convergence to cyclic stationarity.
```
