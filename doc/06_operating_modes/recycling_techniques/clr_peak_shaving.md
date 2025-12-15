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

variable_units = {
    r"\Delta t_{\text{cycle}}": r"\text{s}",
    r"\Delta t_{\text{feed}}": r"\text{s}",
    r"t_{\text{recycle, off}}": r"\text{s}",
    r"t_{\text{recycle, start A, 1}}": r"\text{s}",
    r"t_{\text{recycle, end A, 1}}": r"\text{s}",
    r"t_{\text{recycle, start B, 1}}": r"\text{s}",
    r"t_{\text{recycle, end B, 1}}": r"\text{s}",
}
```

(clr_peak_shaving)=
# Closed-loop recycling with peak shaving

The disadvantage of the CLR process is an increased dispersion due to multiple passes through the pump and additional piping.

To improve the overall process performance, the CLR process is often combined with peak shaving.
In this process, the initial and final regions of the chromatogram with sufficient purity are "shaved off" during each cycle.
Peak shaving can reduce the number of recycling cycles required, since a decreasing amount of components must be pumped across the column.

```{figure} ./figures/clr_peak_shaving_events.png
:name: clr_peak_shaving_events

Events for closed-loop recycling process with peak shaving.
```

```{code-cell} ipython3
:tags: [remove-cell]

from CADETProcess.simulator import Cadet
from cadetrdm import Options

from process import setup_process, plot_results

options = Options()
options.enable_peak_shaving = True
options.peak_shaving_cycles = 3

process = setup_process(options)

process.feed_duration.time = 40
t_cycle = 9 * 60
process.cycle_time = options.peak_shaving_cycles * t_cycle
process.recycle_off_output_state.time = (options.peak_shaving_cycles - 1) * t_cycle

process.start_a_output_state_0.time = 4.5 * 60
process.end_a_output_state_0.time = 5.3 * 60
# 1 B
process.start_b_output_state_0.time = 7.0 * 60
process.end_b_output_state_0.time = 9.0 * 60
# 2 A
process.start_a_output_state_1.time = 10.0 * 60
process.end_a_output_state_1.time = 11.5 * 60
# 2 B
process.start_b_output_state_1.time = 13.0 * 60
process.end_b_output_state_1.time = 14.5 * 60

process_simulator = Cadet()

simulation_results = process_simulator.simulate(process)
fig, axs = plot_results(simulation_results)
glue("clr_peak_shaving", fig, display=False)

```

```{glue:figure} clr_peak_shaving
:name: clr_peak_shaving
:scale: 50%

**Left:** Concentration at column outlet.
**Right:** Concentration at system outlet.
```

(clr_peak_shaving_optimization)=
## Optimization of CLR with peak shaving

Variables
- Feed duration
- Delay Reversal
- Delay injection
- peak shaving times
- TODO: check variables
- TODO: add linear constraints

(clr_peak_shaving_single)=
## Single-objective optimization

Here we do some single-objective optimization.

```{code-cell} ipython3
:tags: [remove-cell]

soo_chrom, ax, soo_table, soo_obj = create_figure_and_table(
    studies_root,
    "clr",
    "single-objective_peak_shaving",
    variable_units=variable_units,
)
glue("clr_ps_soo_chrom", soo_chrom, display=False)
```

{numref}`clr_ps_soo_objectives` shows objective function values.

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
display(Markdown(soo_obj))
```

{numref}`clr_ps_soo_kpi` summarizes results.

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
display(Markdown(soo_table))
```

{numref}`clr_ps_soo_chrom` shows chromatogram of best value.

```{glue:figure} clr_ps_soo_chrom
:name: clr_ps_soo_chrom
:scale: 100%

Optimal chromatogram of single-objective optimization of CLR process with peak shaving.
```

(clr_ps_multi)=
## Multi-objective optimization

Here we do some multi-objective optimization.

```{code-cell} ipython3
:tags: [remove-cell]

moo_chrom, ax, moo_table, moo_obj = create_figure_and_table(
    studies_root,
    "clr",
    "multi-objective_peak_shaving",
    variable_units=variable_units,
)
glue("clr_ps_moo_chrom", moo_chrom, display=False)
```

{numref}`clr_ps_moo_objectives` shows objective function values.

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
display(Markdown(moo_obj))
```

{numref}`clr_ps_moo_kpi` summarizes results.

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
display(Markdown(moo_table))
```

{numref}`clr_ps_moo_chrom` shows optimal chromatograms.

```{glue:figure} clr_ps_moo_chrom
:name: clr_ps_moo_chrom
:scale: 100%

Optimal chromatogram of multi-objective optimization of CLR process with peak shaving.
```

Discuss: Not really robust in practice. Maybe better when combined with model predictive control.
