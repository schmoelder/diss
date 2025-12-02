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
    simulate_and_plot,
    fractionate_results,
    embed_table_in_directive,
    setup_so_results_table,
)

study = setup_study(studies_root, "flip_flop")
cases = setup_cases(study)
```

(flip_flop)=
# Flip-flop chromatography

Flip-flop chromatography, also known as flip-flow or two-way chromatography, refers to an operation mode in which the flow direction through the column is periodically reversed during the separation process.
The operating mode was first proposed by Martin et al. (1979) as a method suitable for separating mixtures containing both highly adsorptive and fast-eluting components {cite}`Martin1979FlipflopChromatography`.
Bailly and Tondeur later highlighted its effectiveness in improving resolution while reducing peak tailing and eluent consumption {cite}`Bailly1981TwowayChromatography`.
Further development was carried out by Colin et al. {cite}`Colin1991FlipFlopElution`.

The fundamental principle is to inject the feed mixture at one end of the column and allow the early-eluting components to exit at the opposite end.
Once these fast-eluting components have been withdrawn, the flow is reversed, and the remaining, more strongly retained components are eluted in the opposite direction.
This operating concept aims to enhance both the resolution and efficiency of separations, particularly in cases involving mixtures with components of very different adsorption behaviors {cite}`SchmidtTraub2020`.

As illustrated in {ref}`flip-flop_bulk`, this cycle is repeated with successive injections and flow reversals, resulting in an alternating product collection scheme.

(flip-flop_process)=
## Process model

As mentioned above, flip-flop chromatography is best suited for scenarios in which components exhibit very different adsorption behavior.
For this purpose, a linear isotherm with parameters listed in {numref}`flip_flop_parameters` will be used for this study.

```{table} Parameters of column geometry, mass transport and binding of the model molecules ($i \in \{A, B\}$).
:name: flip_flop_parameters
:align: center

| Catalog     | Symbol            | Description          | Value   | Unit                           |
| ----------- | ----------------- | -------------------- | ------- | ------------------------------ |
| **Binding** | $k_{\text{eq},i}$ | Equilibrium constant | [1, 20] | $\text{m}^{3}~\text{mol}^{-1}$ |
```

To model the flip-flop operating mode in **CADET-Process**, two {class}`Inlets <CADETProcess.processModel.Inlet>`, a column model (e.g., {class}`~CADETProcess.processModel.LumpedRateModelWithPores`), and an {class}`~CADETProcess.processModel.Outlet` are connected.

```{figure} ./figures/flow_sheet.png
:name: flip-flop_flow_sheet

Flow sheet for the flip-flop process.
```

To model the injection, {class}`Events <CADETProcess.dynamicEvents.Event>` are introduced to modify the {attr}`~CADETProcess.processModel.Inlet.flow_rate` attribute of the {class}`~CADETProcess.processModel.Inlet` unit operations.
To reduce the number of event times that need to be specified, event dependencies are defined to ensure that either feed or eluent is always flowing through the column.
Moreover, after a given $\Delta t_{reversal}$, the {attr}`~CADETProcess.processModel.LumpedRateModelWithPores.flow_direction` attribute of the {class}`~CADETProcess.processModel.LumpedRateModelWithPores` is set to $-1$, indicating a flow reversal.
It is important to note that, by convention, in **CADET-Process** a full cycle requires that all parameters repeat.
Consequently, a second injection is then executed, while the flow is still reversed.
To ensure full elution of the strongly bound component, the injection is delayed by $\Delta t_{delay}$.

```{figure} ./figures/event_dependencies.png
Events of flip-flop process with event dependencies.
```

```{code-cell} ipython3
:tags: [remove-cell]

from CADETProcess.simulator import Cadet

from process import setup_process, plot_results

process = setup_process()

feed_duration = 60
process.feed_duration.time = feed_duration

delay_flip = 325
process.delay_flip.time = delay_flip

delay_injection = 190
process.delay_injection.time = delay_injection

cycle_time = 2*(feed_duration + delay_flip + delay_injection)
process.cycle_time = cycle_time

process.flow_sheet.column.solution_recorder.write_solution_bulk = True

process_simulator = Cadet()
process_simulator.n_cycles = 1

simulation_results = process_simulator.simulate(process)
fig_flip_flop_bulk, _ = plot_results(simulation_results, n_times=12)
glue("flip-flop_bulk", fig_flip_flop_bulk, display=False)
```

```{glue:figure} flip-flop_bulk
:name: flip-flop_bulk
:scale: 50%

**Left:** Concentration profile at the inllet of the column. **Center**: Bulk concentration at different times. The flow direction is indicated by the arrow. **Right:** concentration profile at the system outlet. @TODO: Add note about time scale (or axis); Also offset to better visualize injection
```

(flip-flop_evaluation)=
## Process evaluation

After simulation, the {class}`~CADETProcess.simulationResults.SimulationResults` can be analyzed to determine optimal fractionation times using the {mod}`~CADETProcess.fractionation` module.

(flip-flop_optimization)=
## Process optimization

Variables
- Feed duration
- Delay Reversal
- Delay injection

For this purpose, an {class}`~CADETProcess.optimization.OptimizationProblem` is formulated to maximize process performance.

(flip_flop_single)=
### Single-objective optimization

Here we do some single-objective optimization.

```{code-cell} ipython3
:tags: [remove-cell]

so = cases["single-objective"]
so_problem, _ = load_optimization_config(so)
so_results = load_optimization_results(so)

simulation_results = simulate_results(so_problem, so_results.x[0])
fractionator = fractionate_results(so_problem, simulation_results)
so_flip_flop_fig, ax = fractionator.plot_fraction_signal()

glue("so_flip_flop_fig", so_flip_flop_fig, display=False)

so_flip_flop_table = setup_so_results_table(so_results, fractionator)
```

```{glue:figure} so_flip_flop_fig
:name: so_flip_flop_chromatogram
:scale: 50%

Optimal chromatogram of single-objective optimization of flip flop process.
```

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
display(Markdown(so_flip_flop_table))
```

{numref}`so_flip_flop_kpi` shows the optimized variable some values.

### Multi-objective

## Summary
Despite its potential, the flip-flop mode has seen limited adoption—possibly due to concerns about column design, complexity, or the mechanical stability of packing materials under repeated flow reversals.
Alternatives worth considering include the use of pre-columns (@TODO: ref to serial columns), or gradient elution (@TODO: ref to gradient elution).
