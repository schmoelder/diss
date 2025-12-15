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
study = setup_study(studies_root, "clr")

variable_units={
    r"\Delta t_{\text{cycle}}": r"\text{s}",
    r"\Delta t_{\text{feed}}": r"\text{s}",
    r"t_{\text{recycle, off}}": r"\text{s}",
}
```

(clr)=
# Closed-loop recycling

In closed-loop recycling (CLR), the stock mixture is pumped over the column several times until the desired purity is achieved.
The general structure of a CLR is shown in {numref}`clr_flow_sheet`.

```{figure} ./figures/clr_flow_sheet.png
:name: clr_flow_sheet

Flow sheet for closed-loop recycling process.
```

To realize the recycling, the {attr}`~CADETProcess.processModel.FlowSheet.output_state` attribute of the column needs to be modified, leading to the following event structure:

```{figure} ./figures/clr_events.png
:name: clr_events

Events for closed-loop recycling process.
```

To reduce the number of event times that need to be specified, event dependencies are specified which enforce that always either feed or eluent are being pumped through the column.

Now, the cycle time is set to $10~min$ and the `feed_duration` to $1~min$.
{numref}`clr_outlet` shows the concentration profiles at the column and system outlets, respectively.

```{code-cell} ipython3
:tags: [remove-cell]

from CADETProcess.simulator import Cadet
from cadetrdm import Options

from process import setup_process, plot_results

options = Options()
options.peak_shaving_cycles = 3
options.enable_peak_shaving = False

process = setup_process(options)

process.feed_duration.time = 40
t_cycle = 9 * 60
process.cycle_time = options.peak_shaving_cycles * t_cycle
process.recycle_off_output_state.time = (options.peak_shaving_cycles - 1) * t_cycle

process_simulator = Cadet()

simulation_results = process_simulator.simulate(process)
fig, axs = plot_results(simulation_results)
glue("clr_outlet", fig, display=False)

```

```{glue:figure} clr_outlet
:name: clr_outlet
:scale: 50%

**Left:** Concentration at column outlet.
**Right:** Concentration at system outlet.
```

(clr_optimization)=
## Optimization of CLR

Variables
- Feed duration
- Delay Reversal
- Delay injection
- TODO: check variables
- TODO: add linear constraints

(clr_single)=
### Single-objective optimization

Here we do some single-objective optimization.

```{code-cell} ipython3
:tags: [remove-cell]

soo_chrom, ax, soo_table, soo_obj = create_figure_and_table(
    studies_root,
    "clr",
    "single-objective",
    variable_units=variable_units,
)
glue("clr_soo_chrom", soo_chrom, display=False)
```

{numref}`clr_soo_objectives` shows objective function values.

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
display(Markdown(soo_obj))
```

{numref}`clr_soo_kpi` summarizes results.

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
display(Markdown(soo_table))
```

{numref}`clr_soo_chrom` shows chromatogram of best value.

```{glue:figure} clr_soo_chrom
:name: clr_soo_chrom
:scale: 100%

Optimal chromatogram of single-objective optimization of CLR process.
```

(clr_multi)=
## Multi-objective optimization

Here we do some multi-objective optimization.

```{code-cell} ipython3
:tags: [remove-cell]

moo_chrom, ax, moo_table, moo_obj = create_figure_and_table(
    studies_root,
    "clr",
    "multi-objective",
    variable_units=variable_units,
)
glue("clr_moo_chrom", moo_chrom, display=False)
```

{numref}`clr_moo_objectives` shows objective function values.

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
display(Markdown(moo_obj))
```

{numref}`clr_moo_kpi` summarizes results.

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
display(Markdown(moo_table))
```

{numref}`clr_moo_chrom` shows optimal chromatograms.

```{glue:figure} clr_moo_chrom
:name: clr_moo_chrom
:scale: 100%

Optimal chromatogram of multi-objective optimization of CLR process.
```
