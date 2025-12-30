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
study = setup_study(studies_root, "batch_elution")

variable_units={
    r"\Delta t_{\text{cycle}}": r"\text{s}",
    r"\Delta t_{\text{feed}}": r"\text{s}",
}
from et_simulator import compare_cadet_with_et, convert_binding_to_linear, convert_column_to_lrm
```

(batch_elution_study)=
# Batch Elution Chromatography

A basic chromatographic batch-elution setup comprises `feed` and `eluent` reservoirs, a pump to deliver the required flow rate against the column's pressure drop, a valve to switch between feed and eluent, the column itself, and one or more valves for fraction collection.
In **CADET-Process**, this setup is modeled by connecting two {class}`Inlets <CADETProcess.processModel.Inlet>` and a column model (e.g., {class}`~CADETProcess.processModel.LumpedRateModelWithPores`).
In addition, an {class}`~CADETProcess.processModel.Outlet` is added to the {class}`~CADETProcess.processModel.FlowSheet`.
This allows optimal fractionation times to be identified through chromatogram analysis (see {numref}`fractionation`), eliminating the need for predefined fractionation points and demonstrating a key advantage of model-based design.
The flow sheet is demonstrated in {numref}`batch_elution_flow_sheet`.

```{figure} ./figures/flow_sheet.png
:name: batch_elution_flow_sheet

Flow sheet for the batch elution process.
```

To model the injection, {class}`Events <CADETProcess.dymamicEvents.Event>` are introduced to modify the {attr}`~CADETProcess.processModel.Inlet.flow_rate` attribute of the {class}`~CADETProcess.processModel.Inlet` unit operations.
To reduce the degrees of freedom that need to be explicitly specified, event dependencies are added to ensure that either feed or eluent is always flowing through the column.
The events and durations are depicted in {numref}`batch_elution_events`.

```{figure} ./figures/event_dependencies.png
:name: batch_elution_events

Events of batch elution process with event dependencies.
```

{numref}`fig_batch_elution` compares the concentration profile of the ideal model at the column outlet, demonstrating good agreement between the simulation results and equilibrium theory.

```{code-cell} ipython3
:tags: [remove-cell]

from CADETProcess.modelBuilder import BatchElution

from process import setup_process

process = setup_process()

column_lrm = convert_column_to_lrm(process.flow_sheet.column)
column_lrm.binding_model = convert_binding_to_linear(column_lrm.binding_model)

c_feed = process.flow_sheet.feed.c[:, 0]
flow_rate = process.feed_on.state

batch_process = BatchElution(
    column_lrm,
    c_feed,
    flow_rate,
    feed_duration=60,
    cycle_time=600,
)

fig_batch_elution, ax = compare_cadet_with_et(batch_process)
glue("fig_batch_elution", fig_batch_elution, display=False)
```

```{glue:figure} fig_batch_elution
:name: fig_batch_elution
:scale: 100%

Comparison of the batch elution simulation chromatogram (solid line) with the analytical equilibrium theory solution (dashed line), assuming a linear binding model and neglecting axial dispersion and other transport-limiting effects.
```

To optimize the batch elution process, the decision variables are
- Feed duration, $\Delta t_{\text{feed}} \in [10, 300]\,\text{s}$
- Cycle time, $\Delta t_{\text{cycle}} \in [10, 600]\,\text{s}$

In addition, the linear constraint

$$
\Delta t_{\text{cycle}} \ge \Delta t_{\text{feed}}
$$
is imposed.

(batch_elution_single)=
## Single-objective optimization

Here we do some single-objective optimization.
Very interesting

```{code-cell} ipython3
:tags: [remove-cell]

soo_chrom, ax, soo_table, soo_obj = create_figure_and_table(
    studies_root,
    "batch_elution",
    "single-objective",
    variable_units=variable_units,
)
glue("batch_elution_soo_chrom", soo_chrom, display=False)
```

{numref}`batch_elution_soo_objectives` shows objective function values.

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
display(Markdown(soo_obj))
```

{numref}`batch_elution_soo_kpi` summarizes results.

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
display(Markdown(soo_table))
```

{numref}`batch_elution_soo_chrom` shows chromatogram of best value.

```{glue:figure} batch_elution_soo_chrom
:name: batch_elution_soo_chrom
:scale: 100%

Optimal chromatogram of single-objective optimization of batch elution process.
```

(batch_elution_multi)=
## Multi-objective optimization

Here we do some multi-objective optimization.

```{code-cell} ipython3
:tags: [remove-cell]

moo_chrom, ax, moo_table, moo_obj = create_figure_and_table(
    studies_root,
    "batch_elution",
    "multi-objective",
    variable_units=variable_units,
)
glue("batch_elution_moo_chrom", moo_chrom, display=False)
```

{numref}`batch_elution_moo_objectives` shows objective function values.

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
display(Markdown(moo_obj))
```

{numref}`batch_elution_moo_kpi` summarizes results.

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
display(Markdown(moo_table))
```

{numref}`batch_elution_moo_chrom` shows optimal chromatograms.

```{glue:figure} batch_elution_moo_chrom
:name: batch_elution_moo_chrom
:scale: 100%

Optimal chromatogram of multi-objective optimization of batch elution process.
```
