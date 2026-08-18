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
    plot_soo_objective_figures,
    resize_sparse_chromatogram_figure,
)
```

```{code-cell} ipython3
:tags: [remove-cell]

operating_mode = "batch-elution"
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

(batch_elution_auto-cycle-time_soo)=
# Single-objective optimization of a binary Langmuir separation problem

In the following, a more realistic scenario is considered: competitive Langmuir binding with finite capacity and mass-transfer limitations.
Unlike the previous idealized case, no closed-form reference optimum is available for this system; the result is therefore assessed directly on the KPI values.
The required purity is reduced to $95\%$ to reflect practical constraints.
The problem is summarized in {numref}`batch-elution_auto-cycle_soo_overview`.

```{code-cell} ipython3
:tags: [remove-cell]

case = cases.get(f"{operating_mode}_standard_auto-cycle-time_single-objective")
overview = setup_overview(case)

(
    (soo_fig_obj, _, soo_fig_obj_caption),
    (soo_fig_chrom, _, soo_fig_chrom_caption),
    soo_table,
    soo_results,
    _,
    _,
) = process_soo_results(
    case,
    return_results=True,
)
soo_fig_obj_parts, _, soo_fig_obj_groups = plot_soo_objective_figures(case, soo_results)
plt.close(soo_fig_obj)

for i, fig in enumerate(soo_fig_obj_parts, start=1):
    glue(f"soo_fig_obj_{i}", fig, display=False)
glue("soo_fig_obj_caption", soo_fig_obj_caption)
soo_fig_obj_directives = create_figure_directives(
    "soo_fig_obj",
    "batch-elution_auto-cycle_soo_fig_obj",
    soo_fig_obj_caption,
    soo_fig_obj_groups,
)

resize_sparse_chromatogram_figure(soo_fig_chrom)
glue("soo_fig_chrom", soo_fig_chrom, display=False)
glue("soo_fig_chrom_caption", soo_fig_chrom_caption)
```

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
display(Markdown(overview))
```

{numref}`batch-elution_auto-cycle_soo_fig_obj` shows the objective function values as a function of the feed duration, with a clear maximum.
{numref}`batch-elution_auto-cycle_soo_kpi` summarizes the results.
The required purity is met, with a small residual deviation attributable to the finite resolution of the fractionation algorithm; tightening its tolerances would reduce this at the cost of computational speed.
Overall recovery is lower than in the idealized case due to the larger waste fraction, as shown in {numref}`batch-elution_auto-cycle_soo_fig_chrom`.
The chromatogram reveals both the characteristic "overshoot" of competitive nonlinear binding and incomplete separation from dispersive effects, which together create broader overlap regions that must be discarded as waste.
Despite this added complexity, the optimizer identifies a well-defined operating point, confirming that the framework handles the added complexity without loss of convergence quality.

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
display(Markdown(soo_fig_obj_directives))
```

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
display(Markdown(soo_table))
```

```{glue:figure} soo_fig_chrom
:name: batch-elution_auto-cycle_soo_fig_chrom

{glue:text}`soo_fig_chrom_caption`
```
