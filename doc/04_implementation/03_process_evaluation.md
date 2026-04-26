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

(process_evaluation)=
# Process Evaluation

Simulation results alone are not sufficient to assess whether a chromatographic process meets its design goals: raw concentration profiles do not directly yield performance indicators such as purity or yield, nor do they quantify agreement with experimental data.
A dedicated evaluation step is therefore needed to extract the performance indicators defined in {numref}`kpi` and to quantify the agreement with experimental data required for model calibration (see {numref}`model_calibration`), before those metrics can later be used in optimization.
CADET-Process provides two main tools for this purpose.
The {mod}`~CADETProcess.fractionation` module determines optimal cut times and calculates KPIs such as purity, yield, and productivity from simulated chromatograms.
The {mod}`~CADETProcess.comparison` module quantifies the difference between simulation results and reference data, enabling the formulation of inverse problems for parameter estimation.

(fractionation)=
## Product fractionation

As discussed in {numref}`kpi`, the performance of a chromatographic process is assessed from the amounts of target components collected in the product fractions.
The {mod}`~CADETProcess.fractionation` module provides the {class}`~CADETProcess.fractionation.Fractionator` class for this purpose, as well as a method for automatically determining optimal fractionation times.

### Fractionator

The {class}`~CADETProcess.fractionation.Fractionator` class collects the solution into fraction pools for each component.
It supports the evaluation of multiple chromatograms simultaneously and allows multiple fractions per component within a chromatogram.
To enable calculation of process KPIs, the user specifies which inlets are considered for feed and eluent consumption, and which outlet(s) are used for evaluation.
The simplest approach is to set all fractionation times manually.
Fractionation is controlled through fractionation events, which share the same {class}`~CADETProcess.dynamicEvents.EventHandler` base class as process events (see {numref}`process`).
Each fractionation event marks the point at which the system switches to collecting into a different pool, and requires the following information:

- `event_name`: Name of the event.
- `target`: Index of the component pool into which material is collected from this time onward. `-1` indicates a waste fraction.
- `time`: Time of the event.
- `chromatogram`: Name of the chromatogram. Optional if only one outlet is set as `product_outlet`.

Any number of fractionation events can be added to the {class}`~CADETProcess.fractionation.Fractionator`.
Once all events are set, the Fractionator integrates the concentration profiles over each collection interval to compute molar amounts (see eq. {eq}`molar_amount`), then aggregates the results into a {class}`~CADETProcess.performance.Performance` object containing KPIs such as purity, recovery yield, productivity, and eluent consumption (see {numref}`kpi`).
The chromatogram can be plotted with the fraction times overlaid (see {numref}`chromatogram_fractionation`).

### Optimization of fractionation times

Automatically determining optimal fractionation times is an important step in process optimization.
Due to the diverse shapes that concentration profiles can exhibit, the approach must be flexible enough to handle a broad range of scenarios.
The {mod}`~CADETProcess.fractionation` module provides a convenience method that internally formulates an {class}`~CADETProcess.optimization.OptimizationProblem` (see {numref}`optimization`) to identify optimal cut times automatically.
Objective and constraint functions consider the fractions pooled from all chromatograms of the system.
For every component, different purity requirements can be specified, and different objective functions may be applied.
As initial values for the optimization, areas of the chromatogram with sufficient local purity are identified, i.e., intervals where $PU_i(t)=c_i(t)/\sum_j c_j(t)\geq PU_{\text{min},i}$ {cite}`Shan2004` (see also {numref}`fig_purity`).

```{code-cell} ipython3
:tags: [remove-cell]

import importlib
from pathlib import Path
import sys

from git import Repo
from myst_nb import glue

# Import the study module
diss_root = Path(Repo(search_parent_directories=True).working_dir)
study_root = diss_root / "studies" / "operating_modes"
sys.path.insert(0, str(study_root))

# Setup cases for operating mode
from operating_modes.main import setup_process

operating_mode = "batch-elution"
case_module = importlib.import_module(
    f"operating_modes.{operating_mode.lower().replace('-', '_')}"
)

process_purity = setup_process(
    case_module=case_module,
    separation_problem="standard",
    feed_duration=60,
    cycle_time=600,
)

from CADETProcess.simulator import Cadet
process_simulator = Cadet()

simulation_results = process_simulator.simulate(process_purity)

from CADETProcess.fractionation import Fractionator
from CADETProcess import plotting

fig_purity, axs = plotting.setup_figure(
    nrows=2,
    scale_with_subplots=True,
    sharex=True,
)

frac = Fractionator(simulation_results)
frac.initial_values(0.95)
chrom = frac.chromatograms[0]

chrom.plot(ax=axs[0])
chrom.plot_purity(ax=axs[1])

start = frac.time[0]
end = frac.time[-1]

y_max = 0.95*100

ax = axs[1]
frac._fill_fraction_overlay(
    ax,
    chrom,
    y_max,
    x_axis_in_minutes=True,
    start=frac.time[0],
    end=frac.time[-1]
)

# Purity required
offset = 24
ax.hlines(y_max, start/60, end/60, "k")
plotting.annotate(ax, r"$Pur_{\text{min}}$", xytext=(0, offset), xy=(0, 95))

# A
t = frac.event_times[0]/60
plotting.annotate(
    ax, r"$t_{A,\text{start}}$", xytext=(-1.5*offset, 1*offset), xy=(t, 95)
)
t = frac.event_times[1]/60
plotting.annotate(
    ax, r"$t_{A,\text{end}}$", xytext=(-offset, 1*offset), xy=(t, 95)
)
# A
t = frac.event_times[2]/60
plotting.annotate(
    ax, r"$t_{B,\text{start}}$", xytext=(0, 1*offset), xy=(t, 95)
)
t = frac.event_times[3]/60
plotting.annotate(
    ax, r"$t_{B,\text{end}}$", xytext=(0, 1*offset), xy=(t, 95)
)

fig_purity.tight_layout()
glue("fig_purity", fig_purity, display=False)
```

```{glue:figure} fig_purity
:name: fig_purity
:figwidth: 300px

**Top:** Chromatogram of binary separation.
**Bottom:** Local purity profile of the chromatogram with initial fraction start and end times indicated; color regions highlight intervals where local purity exceeds the minimum required threshold.
```

These initial intervals are then expanded by the optimizer towards regions of lower purity while meeting the cumulative purity constraints.
By default, the mass of the components is maximized under purity constraints, although alternative objective functions are equally viable.
Currently, {class}`~CADETProcess.optimization.COBYLA` {cite}`Powell1994` from the *SciPy* library {cite}`SciPyContributors2020` is used as the optimizer, although the interface supports other optimizers as well.
To the best of the author's knowledge, the generalized formulation of product amounts accommodating multiple chromatograms, multiple fractions, and time-varying flow rates (eq. {eq}`molar_amount`), together with the automatic determination of optimal fractionation times for this general case, have not been previously described in the literature.


(comparison)=
## Comparison of simulation results with reference data

Many research and design problems in chromatography can effectively be approached by formulating them as inverse problems.
These problems involve determining system parameters by comparing simulation results with observed experimental data.
The {mod}`~CADETProcess.comparison` module provides a unified set of metrics for quantifying such differences {cite}`Heymann2022`.
While parameter estimation is the primary use case, the same metric classes are used in other contexts as well, such as detecting cyclic stationarity (see {numref}`stationarity`), ensuring consistent behavior across the framework.

The {class}`~CADETProcess.comparison.Comparator` class compares simulation results against experimental data or against results from a second simulation.
Differences can be visualized and quantified using a range of metrics, including point-wise errors such as NRMSE, as well as peak-shape and peak-area metrics (see {numref}`model_calibration`).
To add a difference metric, the following information must be provided:

- `difference_metric`: The type of the metric.
- `reference`: The reference data which should be used for the metric.
- `solution_path`: The path to the corresponding solution in the simulation results.

Optionally, a start and end time can be specified to only evaluate the difference metric over that time interval.
This is particularly useful if system noise (e.g. injection peaks) should be ignored or if prior knowledge is available about which peaks correspond to which components.
The simulation model used for comparison must be configured to accurately represent the experimental system, including peripheral components such as tubing and valves.

To demonstrate this module, consider a simple tracer pulse injection onto a chromatographic column.
For a more detailed study, refer to {numref}`characterization`.
As an initial guess, the bed porosity is set to $0.5$, and the axial dispersion to $1.0 \times 10^{-7} \text{m}^2 \text{s}^{-1}$.
After simulation, the {class}`~CADETProcess.simulationResults.SimulationResults` is passed to the {meth}`~CADETProcess.comparison.Comparator.evaluate` method, here with an NRMSE metric over the interval from $3$ to $6~\text{min}$.
The resulting comparison is shown in {numref}`chromatogram_comparison`, where a large discrepancy between simulation and experiment is still visible.
Rather than adjusting these parameters manually, an {class}`~CADETProcess.optimization.OptimizationProblem` can be formulated to determine them automatically (see {numref}`optimization`).

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
    'NRMSE', reference, 'column.outlet', start=3*60, end=6*60
)

from CADETProcess.simulator import Cadet
simulator = Cadet()

from examples.characterize_chromatographic_system.column_transport_parameters import process

process.flow_sheet.column.bed_porosity = 0.5
process.flow_sheet.column.axial_dispersion = 1e-7

simulation_results = simulator.simulate(process)
metrics = comparator.evaluate(simulation_results)

fig, ax = comparator.plot_comparison(simulation_results)
glue("chromatogram_comparison", fig, display=False)
```

```{glue:figure} chromatogram_comparison
:name: chromatogram_comparison
:scale: 100%

Comparison between (experimental) reference data (dashed) and simulation results (solid).
```
