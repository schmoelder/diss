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

%config InlineBackend.figure_format = 'retina'
%matplotlib inline

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
study = setup_study(studies_root, "flip_flop")

variable_units={
    r"\Delta t_{\text{feed}}": r"\text{s}",
    r"\Delta t_{\text{delay, flip}}": r"\text{s}",
    r"\Delta t_{\text{delay, inject}}": r"\text{s}",
}
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

As illustrated in {ref}`flip_flop_bulk`, this cycle is repeated with successive injections and flow reversals, resulting in an alternating product collection scheme.

(flip_flop_process)=
## Process model

As mentioned above, flip-flop chromatography is best suited for scenarios in which components exhibit very different adsorption behavior.
For this purpose, a linear isotherm with parameters listed in {numref}`flip_flop_parameters` will be used for this study.
@TODO: That's not true anymore. We use it to demonstrate, but not to optimize

```{table} Parameters of column geometry, mass transport and binding of the model molecules ($i \in \{A, B\}$).
:name: flip_flop_parameters
:align: center

| Catalog     | Symbol            | Description          | Value   | Unit                           |
| ----------- | ----------------- | -------------------- | ------- | ------------------------------ |
| **Binding** | $k_{\text{eq},i}$ | Equilibrium constant | [1, 20] | $\text{m}^{3}~\text{mol}^{-1}$ |
```

To model the flip-flop operating mode in **CADET-Process**, two {class}`Inlets <CADETProcess.processModel.Inlet>`, a column model (e.g., {class}`~CADETProcess.processModel.LumpedRateModelWithPores`), and an {class}`~CADETProcess.processModel.Outlet` are connected.

```{figure} ./figures/flow_sheet.png
:name: flip_flop_flow_sheet

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
glue("flip_flop_bulk", fig_flip_flop_bulk, display=False)
```

```{glue:figure} flip_flop_bulk
:name: flip_flop_bulk
:scale: 50%

**Left:** Concentration profile at the inllet of the column. **Center**: Bulk concentration at different times. The flow direction is indicated by the arrow. **Right:** concentration profile at the system outlet. @TODO: Add note about time scale (or axis); Also offset to better visualize injection
```

After simulation, the {class}`~CADETProcess.simulationResults.SimulationResults` can be analyzed to determine optimal fractionation times using the {mod}`~CADETProcess.fractionation` module.

(flip_flop_optimization)=
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

soo_chrom, ax, soo_table, soo_obj = create_figure_and_table(
    studies_root,
    "flip_flop",
    "single-objective",
    variable_units=variable_units,
)
glue("flip_flop_soo_chrom", soo_chrom, display=False)
```

{numref}`flip_flop_soo_objectives` shows objective function values.

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
display(Markdown(soo_obj))
```

{numref}`flip_flop_soo_kpi` summarizes results.

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
display(Markdown(soo_table))
```

{numref}`flip_flop_soo_chrom` shows chromatogram of best value.

```{glue:figure} flip_flop_soo_chrom
:name: flip_flop_soo_chrom
:scale: 100%

Optimal chromatogram of single-objective optimization of flip-flop process.
```

(flip_flop_multi)=
## Multi-objective optimization

Here we do some multi-objective optimization.

```{code-cell} ipython3
:tags: [remove-cell]

moo_chrom, ax, moo_table, moo_obj = create_figure_and_table(
    studies_root,
    "flip_flop",
    "multi-objective",
    variable_units=variable_units,
)
glue("flip_flop_moo_chrom", moo_chrom, display=False)
```

{numref}`flip_flop_moo_objectives` shows objective function values.

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
display(Markdown(moo_obj))
```

{numref}`flip_flop_moo_kpi` summarizes results.

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
display(Markdown(moo_table))
```

{numref}`flip_flop_moo_chrom` shows optimal chromatograms.

```{glue:figure} flip_flop_moo_chrom
:name: flip_flop_moo_chrom
:scale: 100%

Optimal chromatogram of multi-objective optimization of flip-flop process.
```

## Summary
Despite its potential, the flip-flop mode has seen limited adoption—possibly due to concerns about column design, complexity, or the mechanical stability of packing materials under repeated flow reversals.
Alternatives worth considering include the use of pre-columns (@TODO: ref to serial columns), or gradient elution (@TODO: ref to gradient elution).
