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
  timeout: 1200
---

```{code-cell} ipython3
:tags: [remove-cell]

%matplotlib inline
%config InlineBackend.figure_format = 'retina'

import importlib
from pathlib import Path
import sys

from IPython.display import display, Markdown
from git import Repo
import matplotlib.pyplot as plt
from myst_nb import glue

# Import the study module
diss_root = Path(Repo(search_parent_directories=True).working_dir)
study_root = diss_root / "studies" / "operating_modes"
sys.path.insert(0, str(study_root))

# Setup cases for operating mode
from operating_modes.main import setup_process
from operating_modes.post_processing import (
    get_cases_by_operating_mode,
    process_soo_results,
    process_moo_results,
    setup_overview,
)
```

```{code-cell} ipython3
:tags: [remove-cell]

operating_mode = "flip-flop"
case_module = importlib.import_module(
    f"operating_modes.{operating_mode.lower().replace('-', '_')}"
)
cases = get_cases_by_operating_mode(
    operating_mode,
    index_by_name=True,
    work_dir=study_root,
)
```

(flip_flop)=
# Flip-flop chromatography

Flip-flop chromatography, also known as flip-flow or two-way chromatography, refers to an operation mode in which the flow direction through the column is periodically reversed during the separation process.
The operating mode was first proposed by {cite:t}`Martin1979` as a method suitable for separating mixtures containing both highly adsorptive and fast-eluting components.
{cite:t}`Bailly1981` later highlighted its effectiveness in improving resolution while reducing peak tailing and eluent consumption.
Further development was carried out by Colin et al. {cite}`Colin1991`.

The fundamental principle is to inject the feed mixture at one end of the column and allow the early-eluting components to exit at the opposite end.
The flow reversal occurs when fast-eluting components have cleared the column, typically detected by UV monitoring.
Once reversed, the more strongly retained components are eluted in the opposite direction.
As illustrated in {numref}`flip_flop_bulk`, this cycle repeats with each injection, creating the characteristic alternating product collection pattern.
This approach particularly benefits separations of components with large differences in binding affinity {cite}`SchmidtTraub2020`.
Consequently, the simple separation problem with parameters listed in {numref}`model_parameters` is used for this study.

To model the flip-flop operating mode in CADET-Process, two {class}`Inlets <CADETProcess.processModel.Inlet>`, a column model (e.g., {class}`~CADETProcess.processModel.LumpedRateModelWithPores`), and an {class}`~CADETProcess.processModel.Outlet` are connected (see {numref}`flip_flop_flow_sheet`).

```{figure} ./figures/flow_sheet.png
:name: flip_flop_flow_sheet

Flow sheet for the flip-flop process.
```

To model injection and elution, {class}`Events <CADETProcess.dynamicEvents.Event>` are introduced to modify the {attr}`~CADETProcess.processModel.Inlet.flow_rate` attribute of the {class}`~CADETProcess.processModel.Inlet` unit operations.
To reduce the number of event times that need to be specified, event dependencies are defined to ensure that either feed or eluent is always flowing through the column.
Moreover, after a given $\Delta t_{reversal}$, the {attr}`~CADETProcess.processModel.LumpedRateModelWithPores.flow_direction` attribute of the {class}`~CADETProcess.processModel.LumpedRateModelWithPores` is set to $-1$, indicating a flow reversal.
It is important to note that, by convention, in CADET-Process a full cycle requires that all parameters repeat.
Consequently, a second injection is then executed, while the flow is still reversed.
To ensure full elution of the strongly bound component, the injection is delayed by $\Delta t_{delay}$.
The process events are depicted in {numref}`flip_flop_flow_events`.

```{figure} ./figures/event_dependencies.png
:name: flip_flop_flow_events

Events of flip-flop process with event dependencies.
```

```{code-cell} ipython3
:tags: [remove-cell]

# Setup process
feed_duration = 60
delay_flip = 325
delay_injection = 190
cycle_time = 2*(feed_duration + delay_flip + delay_injection)

process_demo = setup_process(
    case_module=case_module,
    separation_problem="simple",
    convert_to_linear=True,
    feed_duration=feed_duration,
    delay_flip=delay_flip,
    delay_injection=delay_injection,
    cycle_time=cycle_time,
)
process_demo.flow_sheet.column.solution_recorder.write_solution_bulk = True

from CADETProcess.simulator import Cadet
process_simulator = Cadet()

simulation_results = process_simulator.simulate(process_demo)
fig_flip_flop_bulk, _ = case_module.plot_results(simulation_results, n_times=12)
glue("flip_flop_bulk", fig_flip_flop_bulk, display=False)
```

```{glue:figure} flip_flop_bulk
:name: flip_flop_bulk
:scale: 100%

**Left:** Concentration profile at the inlet of the column. **Center**: Bulk concentration at different times. The flow direction is indicated by the arrow. **Right:** Concentration profile at the system outlet.
```

(flip_flop_validation)=
## Process validation

{numref}`fig_flip_flop_validation` compares the concentration profile of the ideal model at the column outlet, demonstrating good agreement between the simulation results and equilibrium theory.

```{code-cell} ipython3
:tags: [remove-cell]

# Setup process
process_validation = setup_process(
    case_module=case_module,
    separation_problem="simple",
    convert_to_linear=True,
    apply_et_assumptions=True,
    cycle_time=40*60,
)

# Import tools
from operating_modes.et_simulator import compare_cadet_with_et

fig_flip_flop_validation, ax = compare_cadet_with_et(process_validation)
glue("fig_flip_flop_validation", fig_flip_flop_validation, display=False)
```

```{glue:figure} fig_flip_flop_validation
:name: fig_flip_flop_validation
:scale: 100%

Comparison of the flip-flop simulation chromatogram (solid line) with the analytical equilibrium theory solution (dashed line), assuming a linear binding model and neglecting axial dispersion and other transport-limiting effects.
```

(flip-flop_multi)=
## Multi-objective optimization of a simple linear separation problem

To optimize the flip-flop process, three variables need to be determined: the feed duration, the delay after which the flow direction is reversed, and the delay before the next injection is made at the opposite end of the column.
The problem is summarized in {numref}`flip-flop_simple_linear_auto-cycle_moo-pc_overview`.

```{code-cell} ipython3
:tags: [remove-cell]

case = cases.get(f"{operating_mode}_simple_linear_auto-cycle-time_multi-objective-per-component")
overview = setup_overview(case)

(
    (moo_fig_obj, _, moo_fig_obj_caption),
    (moo_fig_chrom, _, moo_fig_chrom_caption),
    moo_table,
    moo_results,
    simulation_results,
    fractionators,
) = process_moo_results(
    case,
    load_kwargs={"allow_commit_hash_mismatch": True},
    return_results=True,
)

glue("moo_fig_obj", moo_fig_obj, display=False)
glue("moo_fig_obj_caption", moo_fig_obj_caption)

glue("moo_fig_chrom", moo_fig_chrom, display=False)
glue("moo_fig_chrom_caption", moo_fig_chrom_caption)
```

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
display(Markdown(overview))
```

{numref}`flip-flop_simple_linear_auto-cycle_moo-pc_fig_obj` depicts the evaluated objective function values as a function of both feed duration and the flip-flop delay times.
The optimal solutions and corresponding KPIs for all Pareto points are summarized in {numref}`flip-flop_simple_linear_auto-cycle_moo-pc_kpi`.
The corresponding chromatograms are provided in {numref}`flip-flop_simple_linear_auto-cycle_moo-pc_fig_chrom`.

The optimization results reveal well-defined optima for all performance indicators.
When focusing on productivity maximization, the analysis identifies several characteristic operational behaviors.
The process achieves extreme overloading conditions by operating at high feed volumes to maximize throughput.
A touching band separation emerges where fast-eluting components exit the column first.
Flow reversal then occurs before the slow components reach the original outlet.
This causes the components to elute at what was originally the inlet (now functioning as the outlet), with minimal but non-zero waste fractions.
However, the current linear isotherm system may not fully capture realistic non-linear adsorption behaviors.
This suggests that revisiting the component system choice could improve practical applicability.

```{glue:figure} moo_fig_obj
:name: flip-flop_simple_linear_auto-cycle_moo-pc_fig_obj
:scale: 100%

{glue:text}`moo_fig_obj_caption`
```

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
display(Markdown(moo_table))
```

```{glue:figure} moo_fig_chrom
:name: flip-flop_simple_linear_auto-cycle_moo-pc_fig_chrom
:scale: 100%

{glue:text}`moo_fig_chrom_caption`
```

## Summary

Despite its potential, the flip-flop mode has seen limited adoption, possibly due to concerns about column design, complexity, or the mechanical stability of packing materials under repeated flow reversals.
Alternatives worth considering include the use of pre-columns (see {numref}`serial_columns`), or gradient elution processes where one of the buffer components (e.g. a salt) modulates the binding strength.
