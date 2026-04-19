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

To simulate a {class}`~CADETProcess.processModel.Process`, a simulator must be configured.
This simulator converts the {class}`~CADETProcess.processModel.Process` configuration into the API of the corresponding external simulator.
Currently, only CADET-Core is adapted, although other simulators can potentially be implemented.
CADET-Core needs to be installed separately from CADET-Process. This can be done, for example, using [mamba](https://mamba.readthedocs.io/en/latest/).

```bash
mamba install -c conda-forge cadet
```

For more information on CADET-Core, refer to the {ref}`CADET Documentation <cadet:contents>` {cite}`CADET-Core_documentation`.

## Solver configuration

Before a simulation can be run, the simulator must be configured.
While reasonable default values are set for all simulator parameters, there are cases where adjustments are necessary.
For instance, CADET-Core employs adaptive time stepping, dynamically adjusting the time step size.
This approach balances simulation accuracy with computational efficiency by varying the time step size: it decreases when the error estimate exceeds a specified tolerance and increases when the error is smaller (see {numref}`time_integration`).
Consequently, adjusting the absolute and relative tolerances may be required in scenarios demanding high accuracy or fast computation times.

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
For instance, {numref}`chromatogram` was generated using the {meth}`~CADETProcess.solution.SolutionIO.plot` method of the {class}`~CADETProcess.solution.SolutionIO` class, which is used to store the inlet and outlet profiles of unit operations and provides utility methods such as plot methods.

(stationarity)=
## Cyclic stationarity

Preparative chromatographic separations are often operated in a repetitive fashion.
In particular, processes that incorporate the recycling of streams, like SSR or SMB, have a distinct startup behavior that takes multiple cycles until a periodic steady state is reached {cite}`SchmidtTraub2020`.
In conventional batch chromatography as well, several cycles are needed to attain stationarity in optimized situations where there is a cycle-to-cycle overlap of the elution profiles of consecutive injections.
For this reason, the simulator is capable of simulating a process either for a fixed number of cycles or until cyclic stationarity has been reached.

To automatically simulate until stationarity is reached, a {class}`~CADETProcess.stationarity.StationarityEvaluator` must be configured and added to the process simulator (see {numref}`framework_overview`).
As the simulation continues over multiple cycles, the final state of one cycle serves as the initial state for the next, until the differences fall below a predefined threshold.
Criteria such as the maximum absolute deviation in concentration profiles or the peak areas between consecutive cycles can be specified {cite}`Holmqvist2015`.
For process performance evaluation, only the last cycle is analyzed, as it provides representative key performance indicators of the process's behavior in subsequent cycles (see also {numref}`fractionation`).

To illustrate this concept, consider an SSR process (see {numref}`ssr` for the complete process configuration).
In this example, the relative change in the integral of the chromatogram (area under the chromatogram) between successive cycles is compared.
The simulation continues until the relative change in area is less than $0.1~\%$, or until a maximum number of cycles is reached as a safety limit.
{numref}`chromatogram_stationarity` shows the concentration profile at the column outlet across all cycles.
The distinct startup behavior is noticeable on the left side of the profile, while later cycles exhibit no significant visual difference, indicating cyclic stationarity.
In this scenario, the evaluator stopped the simulator after {glue:text}`n_cycles` cycles.

```{code-cell} ipython3
:tags: [remove-cell]

from examples.recycling.mrssr_process import process

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
