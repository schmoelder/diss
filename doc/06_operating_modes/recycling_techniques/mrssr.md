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
# Mixed-recycle steady-state recycling

In addition to recycling unresolved fractions, fresh feed can be injected into the interior of the circulating profile at the column outlet in each cycle, resulting in the formation of a cyclic steady-state.
This concept, known as closed-loop steady-state recycling (CL-SSR), can achieve higher productivities compared to the CLR process {cite}`Quinones2000`.
However, precise feed timing is challenging, and extra-column dispersion effects complicate the process operation.
To address this, mixed-recycle steady-state recycling (MR-SSR) introduces a tank where recycled fractions and fresh feed are combined before reinjection {cite}`Bailly1982,Sainio2009,Kaspereit2011`, effectively decoupling fresh feed injection from recycling times.
A schematic flow diagram of the MR-SSR process is shown below.

```{figure} ./figures/mrssr_flow_sheet.png
:name: mrssr_flow_sheet

Flow sheet for mixed-recycle steady-state recycling process.
```

To implement recycling, the {attr}`~CADETProcess.processModel.FlowSheet.output_states` attribute of the flow sheet that controls the flow of unit operations downstream of the column must be modified.
To realize the recycling, the {attr}`~CADETProcess.processModel.FlowSheet.output_states` attribute of flow sheet that controls the flow of unit operations downstream of the column must be modified.
To minimize the number of explicitly defined event times, event dependencies are introduced:
- Fresh feed is pumped into the mixing tank only after injection completes.
- The eluent flow is automatically disabled at the start of injection and re-enabled upon its completion.
- Additionally, the injection duration is determined as a function of both the feed duration and the recycling duration.

```{figure} ./figures/mrssr_events.png
:name: mrssr_events

Events for mixed-recycle steady-state recycling process with event dependencies.
```
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
For this demonstration, a standard two-component system with a Langmuir isotherm is used (see {numref}`model_parameters`).

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
To aid the optimizer with the optimization, a variable dependency is introduced to calculate $t_{recycle,off}$ from both $t_{recycle,on}$ and $\Delta t_{recycle}$.
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

{numref}`mrssr_auto-cycle_moo-pc_fig_obj` depicts the evaluated objective function values as a function of both feed duration and the recycling times.
Clear optima emerge when varying cycle time; the optimization landscape for recycling times shows less pronounced optima.
However, recycling duration exhibits well-defined extreme points.
This occurs because the recycling duration was added as an independent variable and $t_{recycle,off}$ depends on both $t_{recycle,on}$ and $\Delta t_{recycle}$.
This variable transformation creates a more favorable optimization landscape.
The optimal variable values and corresponding KPIs for all Pareto edge points are summarized in {numref}`mrssr_auto-cycle_moo-pc_kpi`.
The associated chromatograms are provided in {numref}`mrssr_auto-cycle_moo-pc_fig_chrom`.

When focusing on productivity maximization, optimal solutions consistently show recycling duration approaching zero.
This effectively results in a batch elution process, consistent with results from {cite}`Dienstbier2020`.
For product recovery optimization, the same pattern emerges with minimal recycling durations.
However, achieving $100\%$ recovery inherently produces $100\%$ purity, exceeding typical requirements.
For the specified $95\%$ purity target, any recycling duration can satisfy recovery constraints.
This is evident from the plateau at $95\%$ purity in the objective function plots.
These observations also align with previous findings {cite}`Dienstbier2020`.

Only when focusing on eluent consumption minimization, the analysis reveals distinct recycling behavior
By recycling partially resolved intermediate fractions, MR-SSR effectively reduces eluent requirements.
This can be explained by large feed volumes overloading the column.
The resulting unresolved fractions are then recycled rather than being discarded.
Since no fresh eluent is used during the injection phase, this approach minimizes overall solvent consumption {cite}`Dienstbier2020`.
While the optimization landscape shows less pronounced optima compared to productivity objectives, recycling effects remain clearly visible in the chromatograms.
The chromatograms clearly show the broader, overloaded peaks that enable this efficient solvent reuse.

The combined meta-objective optimization provides additional insights into the practical trade-offs.
Its optimal value effectively balances productivity and solvent consumption by employing a small but non-zero recycling fraction.
However, the optimal operating parameters depend strongly on the specific process priorities and economic constraints.
Incorporating comprehensive economic objectives, such as {eq}`total_cost`, could provide more realistic trade-off analysis.
This would better reflect actual operational decision-making where solvent costs, productivity requirements, and equipment utilization all factor into the optimal solution.

```{glue:figure} moo_fig_obj
:name: mrssr_auto-cycle_moo-pc_fig_obj
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
:name: mrssr_auto-cycle_moo-pc_fig_chrom
:scale: 100%

{glue:text}`moo_fig_chrom_caption`
```

**Summary**

This study demonstrates that the optimization framework can handle complex dynamic processes with internal recycling streams.
Results show clear optima for all objectives, with batch elution emerging as optimal for productivity.
However, MR-SSR mainly provides advantages for eluent consumption, suggesting process selection depends on priorities.

The ability to identify batch elution as a limiting case further confirms the framework's robustness.
This capability indicates potential for superstructure optimization in chromatographic processes.
