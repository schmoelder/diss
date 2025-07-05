---
jupytext:
  formats: md:myst,py:percent
  main_language: python
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.5
kernelspec:
  display_name: Python 3
  name: python3
execution:
  timeout: 600
---

```{code-cell} ipython3
:tags: [remove-cell]

from pathlib import Path
import sys

from IPython.display import display, Markdown
from git import Repo
from myst_nb import glue

# Get the root directory of the Git repository
diss_root = Path(Repo(search_parent_directories=True).working_dir)

# Import the study module
studies_root = diss_root / "studies"
sys.path.insert(0, str(studies_root))
from run_all import (
    setup_study,
    setup_cases,
    load_optimization_config,
    load_optimization_results,
    simulate_results,
    simulate_and_plot,
    fractionate_results,
    embed_table_in_directive,
    setup_so_results_table,
)

study = setup_study(studies_root, "serial_columns")
cases = setup_cases(study)
```

(serial_columns)=
# Serial columns

In situations where one of the components exhibits very strong interaction with the stationary phase, the use of a short pre-column can be advantageous.
By adding such a column, the strongly adsorbing component can be retained before entering the main column, thus avoiding excessively long elution times and reducing the risk of irreversible binding.
As soon as breakthrough of the bound impurity is imminent, the pre-column can be regenerated, replaced, or repacked {cite}`SchmidtTraub2020`.
Alternatively, the output of the pre-column can be dynamically directed either to waste or to the second column, depending on the component currently eluting.

(serial_columns_process)=
## Process Model

{ref}`serial_columns_flow_sheet` shows the flow sheet for a process with columns connected in series.
To prevent periods where no flow occurs through a column, a second eluent {class}`~CADETProcess.processModel.Inlet` is added to the system.
This inlet becomes active whenever flow is directed from the first column to the outlet.

This case also illustrates that multiple chromatograms can be fractionated simultaneously to evaluate process performance.
One strategy to increase productivity is to "shave off" sufficiently separated fractions of the mixture and allow only the unresolved portion to migrate through an additional column.

```{figure} ./figures/flow_sheet.png
:name: serial_columns_flow_sheet

Flow sheet for the serial columns process.
```

To model the injection, {class}`Events <CADETProcess.dynamicEvents.Event>` are introduced to modify the {attr}`~CADETProcess.processModel.Inlet.flow_rate` attribute of the {class}`~CADETProcess.processModel.Inlet` unit operations.
To reduce the number of event times that need to be specified, event dependencies are defined to ensure that either feed or eluent is always flowing through the column.

```{figure} ./figures/event_dependencies.png
Events of serial columns process with event dependencies.
```

```{code-cell} ipython3
:tags: [remove-cell]

from CADETProcess.simulator import Cadet

from process import setup_process, plot_results

process = setup_process()

process.flow_sheet.column_1.length = 0.2
process.flow_sheet.column_2.length = 0.4

process.cycle_time = 600
process.feed_duration.time = 60
process.serial_off.time = 200
process.serial_on.time = 420

process_simulator = Cadet()
process_simulator.evaluate_stationarity = False

simulation_results = process_simulator.simulate(process)

fig, axs = plot_results(simulation_results)

glue("serial_columns", fig, display=False)
```

```{glue:figure} serial_columns
:name: serial_columns_chromatogram
:figwidth: 300px

**Left:** Concentration profile at outlet of first column.
**Center:** Concentration profile at first system outlet.
**Right:** Concentration profile at the second column outlet.
```

(serial_columns_evaluation)=
## Process evaluation

After simulation, the {class}`~CADETProcess.simulationResults.SimulationResults` can be analyzed to determine optimal fractionation times using the {mod}`~CADETProcess.fractionation` module.

(serial_columns_optimization)=
## Process optimization

- Feed duration
- serial_on
- serial_off
- cycle time
- column_1.length
- column_2.length

For this purpose, an {class}`~CADETProcess.optimization.OptimizationProblem` is formulated to maximize process performance.

(serial_columns_single)=
### Single-objective optimization

Here we do some single-objective optimization.

```{code-cell} ipython3
:tags: [remove-cell]

so = cases["single-objective"]
so_problem, _ = load_optimization_config(so)
so_results = load_optimization_results(so)

simulation_results = simulate_results(so_problem, so_results.x[0])
fractionator = fractionate_results(so_problem, simulation_results)
so_serial_columns_fig, axs = plot_results(simulation_results)
glue("so_serial_columns_fig", so_serial_columns_fig, display=False)

so_serial_columns_table = setup_so_results_table(so_results, fractionator)
```

```{glue:figure} so_serial_columns_fig
:name: so_serial_columns_chromatogram
:figwidth: 300px

Optimal chromatogram of single-objective optimization of serial columns process.
```

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
display(Markdown(so_serial_columns_table))
```

{numref}`so_serial_columns_kpi` shows some values.
