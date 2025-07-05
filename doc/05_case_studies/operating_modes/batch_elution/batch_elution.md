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

# Import the study module
diss_root = Path(Repo(search_parent_directories=True).working_dir)
studies_root = diss_root / "studies"
sys.path.insert(0, str(studies_root))

from run_all import (
    setup_study,
    setup_cases,
    load_optimization_config,
    load_optimization_results,
    simulate_results,
    fractionate_results,
    process_so_results,
    setup_so_results_table,
)

study = setup_study(studies_root, "batch_elution")
cases = setup_cases(study)
```

(batch_elution_study)=
# Batch Elution Chromatography

A basic chromatographic batch-elution setup consists of `feed` and `eluent` reservoirs, a pump to deliver the necessary flow rate against the column's pressure drop, a valve to select whether feed or eluent is pumped into the column, the column itself, and one or more valves for fraction collection.

(batch_elution_process)=
## Process Model

In **CADET-Process**, this setup is modeled by connecting two {class}`Inlets <CADETProcess.processModel.Inlet>`, a column model (e.g., {class}`~CADETProcess.processModel.LumpedRateModelWithPores`).
Since in a model-based simulation framework the determination of optimal fractionation times can be done by analyzing the chromatograms {ref}`fractionation`, here only an {class}`~CADETProcess.processModel.Outlet` is added to the {class}`~CADETProcess.processModel.FlowSheet`.

```{figure} ./figures/flow_sheet.png
:name: batch_elution_flow_sheet

Flow sheet for the batch elution process.
```

To model the injection valve, {class}`Events <CADETProcess.dymamicEvents.Event>` are introduced to modify the {attr}`~CADETProcess.processModel.Inlet.flow_rate` attribute of the {class}`~CADETProcess.processModel.Inlet` unit operations.
To reduce the degrees of freedom that need to be explicitly specified, event dependencies are added to ensure that either feed or eluent is always flowing through the column.

```{figure} ./figures/event_dependencies.png
Events of batch elution process with event dependencies.
```

(batch_elution_evaluation)=
## Process evaluation

After simulation, the {class}`~CADETProcess.simulationResults.SimulationResults` can be analyzed to determine optimal fractionation times using the {mod}`~CADETProcess.fractionation` module.

(batch_elution_optimization)=
## Process optimization

By selecting appropriate operating conditions, such as injection volume and flow rate, an efficient operating scenario can be achieved where the stationary phase is utilized optimally.
The highest product recovery is obtained through baseline separation, where component peaks from the same injection do not overlap at the column outlet.
Additionally, minimizing the time between injections improves productivity.
By allowing waste fractions to be collected between product fractions or between peaks of consecutive injections, productivity and eluent consumption can be further optimized at the cost of lower recovery.

These operating conditions can be adjusted using model-based design.
For this purpose, an {class}`~CADETProcess.optimization.OptimizationProblem` is formulated to maximize process performance.
This can be achieved either by combining multiple parameters into a single objective (see {numref}`batch_elution_single`) or by setting up a multi-objective optimization problem (see {numref}`batch_elution_multi`).

(batch_elution_single)=
### Single-objective optimization

Here we do some single-objective optimization.

```{code-cell} ipython3
:tags: [remove-cell]

so = cases["single-objective"]
so_problem, _ = load_optimization_config(so)
so_results = load_optimization_results(so)

simulation_results = simulate_results(so_problem, so_results.x[0])
fractionator = fractionate_results(so_problem, simulation_results)
abc_so_batch_elution_fig, ax = fractionator.plot_fraction_signal()

glue("abc_so_batch_elution_fig", abc_so_batch_elution_fig, display=False)

so_batch_elution_table = setup_so_results_table(so_results, fractionator)
```

```{glue:figure} abc_so_batch_elution_fig
:name: abc_so_batch_elution_chromatogram
:figwidth: 300px

Optimal chromatogram of single-objective optimization of batch elution process.
```

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
display(Markdown(so_batch_elution_table))
```

{numref}`so_batch_elution_kpi` shows some values.

(batch_elution_multi)=
## Multi-objective optimization

Here we do some multi-objective optimization.

<!-- ```{figure} ./results_multi/multi-objective/figures/objectives.png -->
<!-- :name: batch_elution_multi_objectives -->

<!-- Objective space; each dot represents an evaluation. -->
<!-- ``` -->

<!-- ```{figure} ./results_multi/multi-objective/figures/pareto.png -->
<!-- :name: batch_elution_multi_pareto -->

<!-- Pareto Front -->
<!-- ``` -->
