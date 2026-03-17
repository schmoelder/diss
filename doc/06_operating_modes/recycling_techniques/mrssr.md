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
  timeout: 1200
---

% Create custom role for inserting raw latex
```{role} raw-latex(raw)
:format: latex
```

```{code-cell} ipython3
:tags: [remove-cell]

%matplotlib inline
%config InlineBackend.figure_format = 'retina'

print("update 1")

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

operating_mode = "MRSSR"
case_module = importlib.import_module(
    f"operating_modes.{operating_mode.lower().replace('-', '_')}"
)
cases = get_cases_by_operating_mode(
    operating_mode,
    index_by_name=True,
    work_dir=study_root,
)
```

(ssr)=
# Steady-state recycling

In addition to the recycled fraction, fresh feed can also be injected in each cycle, resulting in the formation of a cyclic steady-state.
This process, called closed-loop steady-state recycling (CL-SSR), can achieve higher productivity compared to mixed-recycle steady state recycling. @todo: check/cite
However, due to additional dispersion in the system periphery, maintaining the separation of components generated during the passage of the column is difficult to realize.
Hence, determining the optimal time at which to add new feed is therefore complex.
To overcome this problem, a tank can be inserted in which the recycling fraction and new feed are mixed.
The recycling fraction and new feed are then injected together in a process called mixed-recycle steady-state recycling (MR-SSR).
A schematic flow diagram of the MR-SSR process is shown below.

```{figure} ./figures/mrssr_flow_sheet.png
:name: mrssr_flow_sheet

Flow sheet for mixed-recycle steady-state recycling process.
```

To implement recycling, the {attr}`~CADETProcess.processModel.FlowSheet.output_states` attribute of the flow sheet that controls the flow of unit operations downstream of the column must be modified.
To minimize the number of explicitly defined event times, event dependencies are introduced:
- Fresh feed is pumped into the mixing tank only after injection completes.
- The eluent flow is automatically disabled at the start of injection and re-enabled upon its completion.
- Additionally, the injection duration is determined as a function of both the feed duration and the recycling duration.


```{figure} ./figures/mrssr_events.png
:name: mrssr_events

Events for mixed-recycle steady-state recycling process with event dependencies.
```

For this demonstration, consider a two-component system with a Langmuir isotherm.
@TODO: Add reference / description of chromatogram.

```{code-cell} ipython3
:tags: [remove-cell]

process_demo = setup_process(
    case_module=case_module,
    separation_problem="standard",
    feed_duration=60,
    t_recycle_on=360,
    t_recycle_off=420,
    cycle_time=600,
)

from CADETProcess.simulator import Cadet
process_simulator = Cadet()
process_simulator.evaluate_stationarity = True

simulation_results = process_simulator.simulate(process_demo)

fig_last, _ = case_module.plot_last_cycle(simulation_results)
glue("ssr_last", fig_last, display=False)
fig_all, _ = simulation_results.solution.outlet.outlet.plot()
glue("ssr_all", fig_all, display=False)
fig_overlay, _ = case_module.plot_overlay(simulation_results)
glue("ssr_overlay", fig_overlay, display=False)
```

```{glue:figure} ssr_last
:name: ssr_last
:scale: 50%

Example SSR process in mixed-recycle operation for the separation of two components (blue and red) reaching cyclic steady state after 35 cycles.
**Left:** Concentration profiles at the column’s outlet.
**Right:** Concentration profile at the system outlet.
```

Due to recycling, the concentration in the mixing tank evolves over successive cycles, introducing a transient startup phase.
This behavior necessitates simulating multiple cycles to reach cyclic steady state.
To detect convergence, a {class}`~CADETProcess.stationarity.StationarityEvaluator` is used (see {numref}`stationarity`).
The initial concentration of the tank is another key degree of freedom.
Here, it is set to fresh feed conditions, causing a concentration drop during early cycles.
{numref}`ssr_overlay` illustrates this startup dynamics by overlaying the concentration profiles at the column outlet across all cycles until cyclic stationarity is reached.

```{glue:figure} ssr_overlay
:name: ssr_overlay
:scale: 50%

Overlay of concentration profiles of all cycles, showing the transient towards stationarity.
```

(mrssr_validation)=
## Process validation
{numref}`fig_mrssr_validation` compares the concentration profile of the ideal model at the column outlet, demonstrating good agreement between the simulation results and equilibrium theory.

```{code-cell} ipython3
:tags: [remove-cell]

# Setup process
process_validation = setup_process(
    case_module=case_module,
    separation_problem="standard",
    apply_et_assumptions=True,
    feed_duration=1.2*60,
    t_recycle_on=7.0*60,
    t_recycle_off=7.65*60,
    cycle_time=600,
)

# Import tools
from operating_modes.et_simulator import compare_cadet_with_et

fig_mrssr_validation, ax = compare_cadet_with_et(process_validation)
glue("fig_mrssr_validation", fig_mrssr_validation, display=False)
```

```{glue:figure} fig_mrssr_validation
:name: fig_mrssr_validation
:scale: 100%

Comparison of the MR-SSR simulation chromatogram (solid line) with the analytical equilibrium theory solution (dashed line), assuming a linear binding model and neglecting axial dispersion and other transport-limiting effects.
```


(mrssr_optimization)=
## Process optimization

To optimize the MR-SSR process, in addition to the feed duration, the times at which the recycling is switched on and off need to be optimized.
Additionally, the linear constraints and variable dependencies are imposed to guarantee recycling happens within one cycle time.
The problem is summarized in {numref}`mrssr_auto-cycle_moo-pc_overview`.

```{code-cell} ipython3
:tags: [remove-cell]

case = cases.get(f"{operating_mode}_standard_auto-cycle-time_multi-objective-per-component")
overview = setup_overview(case)

(
    (moo_fig_obj, _, moo_fig_obj_caption),
    (moo_fig_chrom, _, moo_fig_chrom_caption),
    moo_table,
) = process_moo_results(
    case,
    load_kwargs={"allow_commit_hash_mismatch": True},
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

{numref}`mrssr_moo_fig_obj` shows objective function values.

```{glue:figure} moo_fig_obj
:name: mrssr_moo_fig_obj
:scale: 100%

{glue:text}`moo_fig_obj_caption`
```

{numref}`mrssr_auto-cycle_moo-pc_kpi` summarizes results.

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
display(Markdown(moo_table))
```

{numref}`mrssr_moo_fig_chrom` shows chromatogram of best value.

```{glue:figure} moo_fig_chrom
:name: mrssr_moo_fig_chrom
:scale: 100%

{glue:text}`moo_fig_chrom_caption`
```

**Summary**

@TODO: Success!
