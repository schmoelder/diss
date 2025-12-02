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
studies_root = diss_root / "studies" / "operating_modes"
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

study = setup_study(studies_root, "clr")
cases = setup_cases(study)
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
### Single-objective optimization

Here we do some single-objective optimization.

```{code-cell} ipython3
:tags: [remove-cell]

so = cases["single-objective_peak_shaving"]
so_problem, _ = load_optimization_config(so)
so_results = load_optimization_results(so)

simulation_results = simulate_results(so_problem, so_results.x[0])
fractionator = fractionate_results(so_problem, simulation_results)
so_clr_ps_fig, ax = fractionator.plot_fraction_signal()

glue("so_clr_ps_fig", so_clr_ps_fig, display=False)

so_clr_ps_table = setup_so_results_table(so_results, fractionator)
```

```{glue:figure} so_clr_ps_fig
:name: so_clr_ps_chromatogram
:scale: 50%

Optimal chromatogram of single-objective optimization of clr process with peak shaving.
```

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
display(Markdown(so_clr_ps_table))
```

{numref}`so_clr_ps_kpi` shows some values. @TODO: fix name for peak-shaving table


Discuss: Not really robust in practice. Maybe better when combined with model predictive control.
