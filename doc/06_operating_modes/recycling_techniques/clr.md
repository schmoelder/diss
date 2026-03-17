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

```{code-cell} ipython3
:tags: [remove-cell]

print("update 4")

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
print(diss_root)
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

operating_mode = "CLR"
case_module = importlib.import_module(
    f"operating_modes.{operating_mode.lower().replace('-', '_')}"
)
cases = get_cases_by_operating_mode(
    operating_mode,
    index_by_name=True,
    work_dir=study_root,
)
```

(clr)=
# Closed-loop recycling

In closed-loop recycling (CLR), the mixture is pumped through the column several times until the desired purity is achieved.
The general structure of a CLR is shown in {numref}`clr_flow_sheet`.

```{figure} ./figures/clr_flow_sheet.png
:name: clr_flow_sheet

Flow sheet for closed-loop recycling process.
```

The {attr}`~CADETProcess.processModel.FlowSheet.output_states` attribute of the flow sheet, which controls the flow of unit operations downstream of the column, must be modified to realize the recycling.

```{figure} ./figures/clr_events.png
:name: clr_events

Events for closed-loop recycling process.
```

To minimize the number of explicitly defined event times, event dependencies are introduced:
Recycling starts immediately after injection ends, and elution begins only after recycling concludes.
{numref}`fig_clr_demo` depict the concentration profiles of a closed-loop recycling (CLR) process at the column outlet and system outlet, respectively.
The profiles showcase how the recycled material does not fully exit the system before the end of the recycling phase.

```{code-cell} ipython3
:tags: [remove-cell]

# Setup process
process_demo = setup_process(
    case_module=case_module,
    separation_problem="difficult",
    convert_to_linear=True,
    t_recycle_off=16*60,
    cycle_time=25*60,
)

from CADETProcess.simulator import Cadet
process_simulator = Cadet()

simulation_results = process_simulator.simulate(process_demo)
fig_clr_demo, _ = case_module.plot_results(simulation_results)
glue("fig_clr_demo", fig_clr_demo, display=False)
```

```{glue:figure} fig_clr_demo
:name: fig_clr_demo
:scale: 100%

**Left:** Concentration at column outlet.
**Right:** Concentration at system outlet.
```

(clr_validation)=
## Process validation

{numref}`fig_clr_validation` compares the concentration profile of the ideal model at the column outlet, demonstrating good agreement between the simulation results and equilibrium theory.

```{code-cell} ipython3
:tags: [remove-cell]

# Setup process
process_validation = setup_process(
    case_module=case_module,
    separation_problem="difficult",
    apply_et_assumptions=True,
    t_recycle_off=16*60,
    cycle_time=25*60,
)

# Import tools
from operating_modes.et_simulator import compare_cadet_with_et

fig_clr_validation, ax = compare_cadet_with_et(process_validation)
glue("fig_clr_validation", fig_clr_validation, display=False)
```

```{glue:figure} fig_clr_validation
:name: fig_clr_validation
:scale: 100%

Comparison of the CLR simulation chromatogram (solid line) with the analytical equilibrium theory solution (dashed line), assuming a linear binding model and neglecting axial dispersion and other transport-limiting effects.
```

(clr_optimization)=
## Process optimization

To optimize the CLR process, in addition to the feed duration, the time at which the recycling is switched off, i.e., the time at which elution starts, needs to be optimized.
A linear constraint is introduced that ensures that recycling can only end after the end of the injection.
The ideal cycle time is again automatically determined *post hoc* by analyzing the concentration profiles.
The problem is summarized in {numref}`clr_difficult_linear_auto-cycle_moo-pc_overview`.

```{code-cell} ipython3
:tags: [remove-cell]

case = cases.get(f"{operating_mode}_difficult_linear_auto-cycle-time_multi-objective-per-component")
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

{numref}`clr_difficult_linear_auto-cycle_moo-pc_fig_obj` depicts the evaluated objective function values as a function of both feed duration and the recycle-off time.
Generally, clear optimia could be found for all KPIs.
The optimal variable values and KPIs for all Pareto edge points are summarized in {numref}`clr_difficult_linear_auto-cycle_moo-pc_kpi`, with the corresponding chromatograms provided in {numref}`clr_difficult_linear_auto-cycle_moo-pc_fig_chrom`.
The extermely high values for the eluent consumption can be explained by the feed duration

@TODO: Check if calculation of cycle time is correct: Eluent must flow *at least* for the amount of (full width - feed_duration), could this be handled via linear constraints or do we need to change the post-processing?

To better understand, the concentration profiles at the column outlet of (a) and (c) are depiced in {numref}`clr_moo-pc_fig_outlet`.
For process (a), the components passed 10 times fully over the column.
After the tenth cycle, the pure fraction of component $B$ was already "shaved off" while the rest of the mixture would pass one final time over the column.
For process (c), the components passed 16 "and a half" times over the column.

@TODO: Discuss stacked injection
Note, because of the internal closed-loop, stacking multiple injections is less feasible / relevant.

```{glue:figure} moo_fig_obj
:name: clr_difficult_linear_auto-cycle_moo-pc_fig_obj
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
:name: clr_difficult_linear_auto-cycle_moo-pc_fig_chrom
:scale: 100%

{glue:text}`moo_fig_chrom_caption`
```

```{code-cell} ipython3
:tags: [remove-cell]

from CADETProcess import plotting
from operating_modes.post_processing import (
    convert_mm_ss_to_s,
    get_best_individual,
    simulate_and_plot,
    slice_population
)

fig_column_outlet, axs = plotting.setup_figure(nrows=2, ncols=1, scale_with_subplots=True)

simulation_results[0].solution.column.outlet.plot(ax=axs[0], end=55*60)
plotting.add_text(axs[0], r"(a)")

simulation_results[2].solution.column.outlet.plot(ax=axs[1], end=85*60)
plotting.add_text(axs[1], r"(c)")

glue("moo_fig_outlets", fig_column_outlet, display=False)
```

```{glue:figure} moo_fig_outlets
:name: clr_moo-pc_fig_outlet
:scale: 100%

Concentration profiles at column outlets for Pareto edge points (a) and (c)
```

**Summary**

@TODO: Success!

However, the CLR process has the disadvantage of increased dispersion due to multiple passes through the pump and additional piping.
To improve overall process performance, it is often combined with peak shaving, where the initial and final regions of the chromatogram with sufficient purity are "shaved off" during each cycle.
This approach reduces the number of recycling cycles required, as a decreasing amount of components needs to be pumped across the column.
However, peak shaving is not robust in practice, as it is highly sensitive to disturbances.
Additionally, the complexity introduced by multiple optimization variables makes implementation challenging.
While combining the process with model predictive control might improve robustness, this approach is not considered in this work.
