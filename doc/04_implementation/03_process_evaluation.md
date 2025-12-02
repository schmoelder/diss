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
```

(process_evaluation)=
# Process Evaluation

**CADET-Process** offers multiple tools for evaluating simulation results.
This chapter provides an overview of selected evaluation methods available in **CADET-Process**.

(fractionation)=
## Product fractionation

To effectively quantify the performance of a chromatographic process, it is crucial to calculate KPIs such as purity or recovery yield from the chromatograms.
As highlighted in {numref}`chapter %s <kpi>`, the key information for assessing the separation performance of a chromatographic process is derived from the amounts of target components in the collected product fractions.
For this purpose, the {mod}`~CADETProcess.fractionation` module provides the {class}`~CADETProcess.fractionation.Fractionator` class.
Moreover, a method for the automatic determination (or optimization?) of fractionation times is included in the software.

### Fractionator

The {class}`~CADETProcess.fractionation.Fractionator` class facilitates slicing the solution into fraction pools for each component.
It allows for the evaluation of multiple chromatograms simultaneously and supports multiple fractions for each component within a chromatogram.
To enable the calculation of the process parameters, it is necessary to specify which of the inlets should be considered for the feed and eluent consumption, as well as which outlet(s) are to be used for the evaluation.
The simplest approach involves manually setting all fractionation times.

To add a fractionation event, the following information needs to be provided:

- `event_name`: Name of the event.
- `target`: Pool to which fraction is added. `-1` indicates a waste fraction.
- `time`: Time of the event
- `chromatogram`: Name of the chromatogram. Optional if only one outlet is set as `product_outlet`.

Any number of fractions can be added to the {class}`~CADETProcess.fractionation.Fractionator`.
The resulting {class}`~CADETProcess.performance.Performance` object then contains information about key performance indicators such as mass, volume, purity, concentration, productivity, recovery yield, as well as eluent consumption (refer to eq {eq}`mass` to {eq}`purity`).
The chromatogram can be plotted with the fraction times overlaid (see {numref}`chromatogram_fractionation`).

### Optimization of fractionation times

Automatically determining KPIs from chromatograms is an important step in process optimization.
Due to the diverse shapes and forms that concentration profiles can exhibit, a tool is required that is both flexible and capable of handling a broad range of scenarios.
To address this need, the {mod}`~CADETProcess.fractionation` module provides a method to set up an {class}`~CADETProcess.optimization.OptimizationProblem`, which automatically identifies optimal cut times.
Objective and constraint functions consider the fractions pooled from all chromatograms of the system.
For every component, different purity requirements can be specified, and different objective functions may be applied.
As initial values for the optimization, areas of the chromatogram with sufficient local purity are identified, i.e., intervals where $PU_i(t)=c_i(t)/\sum_j c_j(t)\geq PU_{\text{min},i}$ {cite}`Shan2004`.
These initial intervals are then expanded by the optimizer towards regions of lower purity while meeting the cumulative purity constraints.
By default, the mass of the components is maximized under purity constraints, although alternative objective functions are equally viable.
Currently, {class}`~CADETProcess.optimization.COBYLA`{cite}`Powell1994`from the *SciPy* library {cite}`SciPyContributors2020` is used as the optimizer, but other optimizers or heuristic algorithms may also be employed.

To the best of the author's knowledge, this flexible automatic approach for determining fractionation times is a novel contribution that has not been previously discussed in literature.
This method addresses an important gap in the toolchain necessary for the analysis and optimization of advanced chromatographic processes.

@TODO: Add figure here

(comparison)=
## Comparison of simulation results with reference data

Many research and design problems in chromatography can effectively be approached by formulating them as inverse problems.
These problems involve determining system parameters by comparing simulation results with observed experimental data.
For this purpose, the {mod}`~CADETProcess.comparison` module in **CADET-Process** provides tools to quantify the differences between simulation outputs and reference data, such as experimental data or prior simulation results.

The {class}`~CADETProcess.comparison.Comparator` class facilitates the comparison of results from two simulations or between simulation results and experimental data.
It includes several methods for both visualizing and analyzing the differences between datasets.
Users can select from a range of metrics, like sum squared errors or peak shape similarity, to accurately quantify the differences between the datasets.
To add a difference metric, the following information must be provided:

- `difference_metric`: The type of the metric.
- `reference`: The reference data which should be used for the metric.
- `solution_path`: The path to the corresponding solution in the simulation results.

Optionally, a start and end time can be specified to only evaluate the difference metric over that time interval.
This is particularly useful if system noise (e.g. injection peaks) should be ignored or if prior knowledge is available about which peaks correspond to which components.

Next to the experimental data, a reference model needs to be configured, *i.e.* a {class}`~CADETProcess.processModel.Process`.
It must include relevant details so that it is capable of accurately predicting the experimental system (e.g. tubing, valves etc.).

To demonstrate this module, consider a simple tracer pulse injection onto a chromatographic column.
For this example, the full process configuration can be found {ref}`here <fit_column_transport>`.
@TODO: Update reference
As an initial guess, the bed porosity is set to $0.5$, and the axial dispersion to $1.0 \times 10^{-7} \text{m}^2 \text{s}^{-1}$.
After process simulation, the {class}`~CADETProcess.simulationResults.SimulationResults` needs to be passed to the {meth}`~CADETProcess.comparison.Comparator.evaluate` method of the {class}`~CADETProcess.comparison.Comparator`.
Here, an SSE metric has been added for the interval $3 \to 6~\text{min}$.
The difference is visualized in {numref}`chromatogram_comparison`.
The comparison shows that there is still a large discrepancy between simulation and experiment.
Instead of manually adjusting these parameters, an {class}`~CADETProcess.optimization.OptimizationProblem` can be set up, which automatically determines the parameter values.

```{code-cell} ipython3
:tags: [remove-cell]

import numpy as np
data = np.loadtxt('./experimental_data/non_pore_penetrating_tracer.csv', delimiter=',')
time_experiment = data[:, 0]
dextran_experiment = data[:, 1]

from CADETProcess.reference import ReferenceIO
reference = ReferenceIO('dextran experiment', time_experiment, dextran_experiment)

from CADETProcess.comparison import Comparator
comparator = Comparator()
comparator.add_reference(reference)

comparator.add_difference_metric(
    'SSE', reference, 'column.outlet', start=3*60, end=6*60
)

from CADETProcess.simulator import Cadet
simulator = Cadet()

from examples.characterize_chromatographic_system.column_transport_parameters import process

process.flow_sheet.column.bed_porosity = 0.5
process.flow_sheet.column.axial_dispersion = 1e-7

simulation_results = simulator.simulate(process)
metrics = comparator.evaluate(simulation_results)

figs, ax = comparator.plot_comparison(simulation_results)
glue("chromatogram_comparison", figs[0], display=False)
```

```{glue:figure} chromatogram_comparison
:name: chromatogram_comparison
:scale: 100%

Comparison between (experimental) reference data (dashed) and simulation results (solid).
```
