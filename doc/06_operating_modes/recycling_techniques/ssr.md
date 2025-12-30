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

%matplotlib inline
%config InlineBackend.figure_format = 'retina'

from pathlib import Path
import sys

from IPython.display import display, Markdown
from git import Repo
import matplotlib.pyplot as plt
from myst_nb import glue

# Import the study module
diss_root = Path(Repo(search_parent_directories=True).working_dir)
studies_root = diss_root / "studies" / "operating_modes"
sys.path.insert(0, str(studies_root))

from run_all import create_figure_and_table, setup_study
study = setup_study(studies_root, "ssr")

variable_units={
    r"\Delta t_{\text{cycle}}": r"\text{s}",
    r"\Delta t_{\text{feed}}": r"\text{s}",
    r"t_{\text{recycle,on}}": r"\text{s}",
    r"t_{\text{recycle,off}}": r"\text{s}",
}
```

(ssr)=
# Steady-state recycling

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
:scale: 50%

Example SSR process in mixed-recycle operation for the separation of two components (blue and red) reaching cyclic steady state after 35 cycles.
**Left:** Concentration profiles at the column’s outlet.
**Right:** Concentration profile at the system outlet.
```

Since the process shows a startup behavior before reaching steady state, multiple cycles need to be simulated.
For this purpose, a {class}`~CADETProcess.stationarity.StationarityEvaluator` is used (see section {numref}`stationarity`).

```{glue:figure} ssr_overlay
:name: ssr_overlay
:scale: 50%

Overlay of concentration profiles of all cycles, showing the transient towards stationarity.
```

(ssr_single)=
## Single-objective optimization

Here we do some single-objective optimization.

```{code-cell} ipython3
:tags: [remove-cell]

soo_chrom, ax, soo_table, soo_obj = create_figure_and_table(
    studies_root,
    "ssr",
    "single-objective",
    variable_units=variable_units,
)
glue("ssr_soo_chrom", soo_chrom, display=False)
```

{numref}`ssr_soo_objectives` shows objective function values.

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
display(Markdown(soo_obj))
```

{numref}`ssr_soo_kpi` summarizes results.

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
display(Markdown(soo_table))
```

{numref}`ssr_soo_chrom` shows chromatogram of best value.

```{glue:figure} ssr_soo_chrom
:name: ssr_soo_chrom
:scale: 100%

Optimal chromatogram of single-objective optimization of SSR process.
```

(ssr_multi)=
## Multi-objective optimization

Here we do some multi-objective optimization.

```{code-cell} ipython3
:tags: [remove-cell]

moo_chrom, ax, moo_table, moo_obj = create_figure_and_table(
    studies_root,
    "ssr",
    "multi-objective",
    variable_units=variable_units,
)
glue("ssr_moo_chrom", moo_chrom, display=False)
```

{numref}`ssr_moo_objectives` shows objective function values.

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
display(Markdown(moo_obj))
```

{numref}`ssr_moo_kpi` summarizes results.

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
display(Markdown(moo_table))
```

{numref}`ssr_moo_chrom` shows optimal chromatograms.

```{glue:figure} ssr_moo_chrom
:name: ssr_moo_chrom
:scale: 100%

Optimal chromatogram of multi-objective optimization of SSR process.
```
