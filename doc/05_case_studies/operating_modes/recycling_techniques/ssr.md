---
jupytext:
  formats: md:myst,py:percent
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.5
kernelspec:
  display_name: Python 3
  language: python
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
    simulate_and_plot,
    fractionate_results,
    embed_table_in_directive,
    setup_so_results_table,
)

study = setup_study(studies_root, "ssr")
cases = setup_cases(study)
```

(ssr)=
## Steady-State Recycling

In addition to the recycled fraction, fresh feed can also be injected in each cycle, resulting in the formation of a cyclic steady-state.
This process, called closed-loop steady-state recycling (CL-SSR), can achieve higher productivity compared to CLR.
However, due to additional dispersion in the system periphery, maintaining the separation of components generated during the passage of the column is difficult to realize.
Hence, determining the optimal time at which to add new feed is therefore complex.
To overcome this problem, a tank can be inserted in which the recycling fraction and new feed are mixed.
The recycling fraction and new feed are then injected together in a process called mixed-recycle steady-state recycling (MR-SSR).
A schematic flow diagram of the MR-SSR process is shown below.

```{figure} ./figures/mrssr_flow_sheet.png
:name: mrssr_flow_sheet

Flow sheet for mixed-recycle steady-state recycling process.
```

For this demonstration, consider a two-component system with a Langmuir isotherm.

To realize the recycling, the {attr}`~CADETProcess.processModel.FlowSheet.output_state` of the column needs to be modified.
To reduce the number of event times that need to be specified, event dependencies are specified which enforce that always either feed or eluent are being pumped through the column.

```{figure} ./figures/mrssr_events.png
:name: mrssr_events

Events for mixed-recycle steady-state recycling process with event dependencies.
```

Now, the cycle time is set to $10~min$ and the `feed_duration` to $1~min$ and the recycling times are specified.

```{code-cell} ipython3
:tags: [remove-cell]

from CADETProcess.simulator import Cadet

from process import setup_process, plot_overlay, plot_last_cycle

process = setup_process()
process.cycle_time = 600
process.feed_duration.time = 60
process.recycle_on.time = 360
process.recycle_off.time = 420

process_simulator = Cadet()
process_simulator.evaluate_stationarity = True

simulation_results = process_simulator.simulate(process)

fig_last, _ = plot_last_cycle(simulation_results)
glue("ssr_last", fig_last, display=False)
fig_all, _ = simulation_results.solution.outlet.outlet.plot()
glue("ssr_all", fig_all, display=False)
fig_overlay, _ = plot_overlay(simulation_results)
glue("ssr_overlay", fig_overlay, display=False)

```

```{glue:figure} ssr_last
:name: ssr_last
:figwidth: 300px

Example SSR process in mixed-recycle operation for the separation of two components (blue and red) reaching cyclic steady state after 35 cycles.
**Left:** Concentration profiles at the column’s outlet.
**Right:** Concentration profile at the system outlet.
```

Since the process shows a startup behavior before reaching steady state, multiple cycles need to be simulated.
For this purpose, a {class}`~CADETProcess.stationarity.StationarityEvaluator` is used (see {ref}`stationarity_guide`).

```{glue:figure} ssr_overlay
:name: ssr_overlay
:figwidth: 300px

Overlay of concentration profiles of all cycles, showing the transient towards stationarity.
```

### Optimization of SSR

(ssr_single)=
### Single-objective optimization

Here we do some single-objective optimization.

```{code-cell} ipython3
:tags: [remove-cell]

so = cases["single-objective"]
so_problem, _ = load_optimization_config(so)
so_results = load_optimization_results(so)

simulation_results = simulate_results(so_problem, so_results.x[0])
fractionator = fractionate_results(so_problem, simulation_results)
so_ssr_fig, ax = fractionator.plot_fraction_signal()

glue("so_ssr_fig", so_ssr_fig, display=False)

so_ssr_table = setup_so_results_table(so_results, fractionator)
```

```{glue:figure} so_ssr_fig
:name: so_ssr_chromatogram
:figwidth: 300px

Optimal chromatogram of single-objective optimization of ssr process.
```

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
display(Markdown(so_ssr_table))
```

{numref}`so_ssr_kpi` shows some values.
