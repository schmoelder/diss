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
sys.path.insert(0, str(diss_root / "doc" / "_ext"))
from thesis_submodules import restore_pinned_submodule

restore_pinned_submodule(diss_root, "studies/operating_modes")
sys.path.insert(0, str(study_root))

# Setup cases for operating mode
from operating_modes.main import setup_process
from operating_modes.post_processing import (
    get_cases_by_operating_mode,
    process_soo_results,
    process_moo_results,
    setup_overview,
)
from operating_mode_figures import (
    create_figure_directives,
    plot_moo_chromatogram_figures,
    plot_moo_objective_figures,
    resize_chromatogram_figure,
    resize_sparse_chromatogram_figure,
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
restore_pinned_submodule(diss_root, "studies/operating_modes")
```

(clr)=
# Closed-loop recycling

In closed-loop recycling, the mixture is pumped through the column several times until the desired purity is achieved {cite}`Bombaugh1969,Heuer1995`.
The general structure of a CLR is shown in {numref}`clr_flow_sheet`.
To realize the recycling, the flow sheet's output states are reconfigured between injection, recycling, and elution phases via {class}`Events <CADETProcess.dynamicEvents.Event>`.
To reduce the number of explicitly defined event times, event dependencies are introduced:
Recycling starts immediately after injection ends, and elution begins once recycling concludes.
For this demonstration, a difficult separation problem in the linear range is considered (see {numref}`model_parameters`).
The components have similar binding affinities, creating a significant elution overlap that makes separation challenging for conventional methods.
{numref}`fig_clr_demo` shows the concentration profiles of a CLR process at the column outlet and system outlet, respectively.
The profiles illustrate that the recycled material does not fully exit the system before the end of the recycling phase.

```{figure} ./figures/clr_flow_sheet.png
:name: clr_flow_sheet

Flow sheet for closed-loop recycling process.
```

```{figure} ./figures/clr_events.png
:name: clr_events

Events for closed-loop recycling process.
```

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
resize_sparse_chromatogram_figure(fig_clr_demo, ncols=2)
glue("fig_clr_demo", fig_clr_demo, display=False)
```

```{glue:figure} fig_clr_demo
:name: fig_clr_demo
:scale: 100%

**Left:** Concentration at column outlet.
**Right:** Concentration at system outlet.
```

(clr_validation)=
## Process validation (Closed-Loop Recycling)

{numref}`fig_clr_validation` compares the simulation against the equilibrium theory solution, following the approach described in {numref}`analytical_solutions`.
Good agreement confirms the correctness of the process configuration.

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
resize_sparse_chromatogram_figure(fig_clr_validation)
glue("fig_clr_validation", fig_clr_validation, display=False)
```

```{glue:figure} fig_clr_validation
:name: fig_clr_validation
:scale: 100%

Comparison of the CLR simulation chromatogram (solid line) with the analytical equilibrium theory solution (dashed line), assuming a linear binding model and neglecting axial dispersion and other transport-limiting effects.
```

(clr_optimization)=
## Process optimization (Closed-Loop Recycling)

The CLR process requires optimization of both feed duration and the recycling end time.
The key trade-off is between longer recycling periods, which improve resolution of nearly-identical components, and shorter cycle times, which preserve productivity.
A linear constraint ensures recycling concludes only after the injection is complete.
The optimization problem is summarized in {numref}`clr_difficult_linear_auto-cycle_moo-pc_overview`.
{numref}`clr_difficult_linear_auto-cycle_moo-pc_fig_obj` shows the objective function values as a function of both feed duration and the recycling end time.
Clear optima are found for all key performance indicators.
The optimal variable values and corresponding KPIs for all Pareto edge points are summarized in {numref}`clr_difficult_linear_auto-cycle_moo-pc_kpi`, with the associated chromatograms provided in {numref}`clr_difficult_linear_auto-cycle_moo-pc_fig_chrom`.

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
    return_results=True,
)

moo_fig_obj_parts, _, moo_fig_obj_groups = plot_moo_objective_figures(case, moo_results)
moo_fig_chrom_parts, _, moo_fig_chrom_groups = plot_moo_chromatogram_figures(
    case,
    moo_results,
    simulation_results,
    fractionators,
)
plt.close(moo_fig_obj)
plt.close(moo_fig_chrom)

for i, fig in enumerate(moo_fig_obj_parts, start=1):
    glue(f"moo_fig_obj_{i}", fig, display=False)
for i, fig in enumerate(moo_fig_chrom_parts, start=1):
    glue(f"moo_fig_chrom_{i}", fig, display=False)
glue("moo_fig_obj_caption", moo_fig_obj_caption)
glue("moo_fig_chrom_caption", moo_fig_chrom_caption)
moo_fig_obj_directives = create_figure_directives(
    "moo_fig_obj",
    "clr_difficult_linear_auto-cycle_moo-pc_fig_obj",
    moo_fig_obj_caption,
    moo_fig_obj_groups,
)
moo_fig_chrom_directives = create_figure_directives(
    "moo_fig_chrom",
    "clr_difficult_linear_auto-cycle_moo-pc_fig_chrom",
    moo_fig_chrom_caption,
    moo_fig_chrom_groups,
    column_label="chromatograms",
)
```

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
display(Markdown(overview))
```
To further analyze the results, {numref}`clr_moo-pc_fig_outlet` presents the concentration profiles at the column outlet for processes (a) and (c).
In process (a), components complete 10 full column cycles before the pure B fraction is collected.
The remaining mixture then undergoes one final pass.
Process (c) shows 16.5 column cycles, demonstrating the optimizer's use of extended recycling for challenging separations.
This recycling process is also limited by dispersion effects.
As shown in the profiles, the front of component $A$ begins to overlap with the tail of component $B$ from the previous cycle.
Additional recycling beyond this point would not improve separation; the longer time on column increases axial dispersion, causing peak broadening and eventually remixing the components.

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
display(Markdown(moo_fig_obj_directives))
```

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
display(Markdown(moo_table))
```

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
display(Markdown(moo_fig_chrom_directives))
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

Concentration profiles at column outlets for Pareto edge points (a) and (c) of CLR process with difficult separation problem.
```

{raw-latex}`\FloatBarrier`

**Summary**

While this case study successfully demonstrates how CLR processes are capable of purifying challenging separation problems, the operating mode has inherent limitations.
Multiple passes through the column, pump, and additional piping increase dispersion, degrading the separation quality.
Peak shaving is often employed to mitigate this by removing pure regions from chromatogram edges during each cycle, reducing the number of required recycling cycles.
However, peak shaving often proves to be non-robust in practice due to high sensitivity to process disturbances.
Additionally, the complexity introduced by multiple optimization variables makes the implementation of model-based design challenging.
While combining the process with model predictive control might improve its robustness, this approach is not considered in this work.
Moreover, the closed-loop configuration inherently limits productivity since fresh feed cannot be injected during recycling periods.
This constraint makes injection stacking impractical for CLR processes.
