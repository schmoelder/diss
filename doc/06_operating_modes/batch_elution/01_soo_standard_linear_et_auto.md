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
sys.path.insert(0, str(study_root))
sys.path.insert(0, str(diss_root / "doc" / "_ext"))

# Setup cases for operating mode
from operating_modes.main import setup_process
from operating_modes.post_processing import (
    get_cases_by_operating_mode,
    process_soo_results,
    process_moo_results,
    setup_overview,
)
from operating_mode_figures import create_figure_directives, plot_soo_objective_figures
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
```

(batch_elution_linear_et_auto-cycle-time_soo)=
# Single-objective optimization of an idealized system

To validate the framework, an idealized scenario is evaluated for which the optimal operating conditions can be derived analytically: the binary model system with linear binding and equilibrium theory assumptions.
Using the total dead time $t_{0,t} = L_c / u = 195.4~\text{s}$ and the phase ratio $F = (1 - \varepsilon^t) / \varepsilon^t = 0.389$, the retention times of components A and B follow from {eq}`retention_time_linear`:

$$t_{\text{R},A} = t_{0,t}(1 + F \cdot a_A) = 347.4~\text{s}, \qquad t_{\text{R},B} = t_{0,t}(1 + F \cdot a_B) = 423.4~\text{s}.$$

For touching-band separation, where the trailing edge of component A just meets the leading edge of component B at the column outlet, the optimal feed duration equals the difference in retention times:

$$t_{\text{feed}} = t_{\text{R},B} - t_{\text{R},A} = 76.0~\text{s}.$$

The corresponding optimal cycle time, defined as the window from the first elution of component A to the last elution of component B under stacked injections, is $t_{\text{cycle}} = 2 \cdot t_{\text{feed}} = 152.0~\text{s}$.
These values serve as the known reference optimum against which the optimizer's result can be verified.
Here, the process is optimized by varying the feed duration using a single objective function with equal weights for all KPIs {eq}`weighted_objective`.
While perfect purity is theoretically achievable in this idealized system without physical dispersion, the targeted purity is set to $99.9\%$ to account for numerical artifacts.
The problem is summarized in {numref}`batch-elution_linear_et_auto-cycle_soo_overview`.

```{code-cell} ipython3
:tags: [remove-cell]

case = cases.get(f"{operating_mode}_standard_linear_et_auto-cycle-time_single-objective")
overview = setup_overview(case)

(
    (soo_fig_obj, _, soo_fig_obj_caption),
    (soo_fig_chrom, _, soo_fig_chrom_caption),
    soo_table,
    soo_results,
    simulation_results,
    fractionator,
) = process_soo_results(
    case,
    load_kwargs={"allow_commit_hash_mismatch": True},
    return_results=True,
)
soo_fig_obj_parts, _, soo_fig_obj_groups = plot_soo_objective_figures(case, soo_results)
plt.close(soo_fig_obj)

for i, fig in enumerate(soo_fig_obj_parts, start=1):
    glue(f"soo_fig_obj_{i}", fig, display=False)
glue("soo_fig_obj_caption", soo_fig_obj_caption)
soo_fig_obj_directives = create_figure_directives(
    "soo_fig_obj",
    "batch-elution_linear_et_auto-cycle_soo_fig_obj",
    soo_fig_obj_caption,
    soo_fig_obj_groups,
)

glue("soo_fig_chrom", soo_fig_chrom, display=False)
glue("soo_fig_chrom_caption", soo_fig_chrom_caption)

from operating_modes.post_processing import format_mm_ss

feed_duration = rf"${format_mm_ss(soo_results.x[0])}~\text{{min}}$"
glue("feed_duration", feed_duration)

cycle_time_expected = rf"${format_mm_ss(2*soo_results.x[0])}~\text{{min}}$"
glue("cycle_time_expected", cycle_time_expected)

cycle_time = rf"${format_mm_ss(fractionator.cycle_time)}~\text{{min}}$"
glue("cycle_time", cycle_time)
```

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
display(Markdown(overview))
```

The cycle time, required for KPI calculation, is determined from the simulated chromatogram: it spans from the first time point at which component A appears at the column outlet to the last time point at which component B is present, consistent with the theoretical definition above.
To ensure complete elution, each simulation is initialized with a sufficiently large cycle time; the elution window is then identified using a $0.1\%$ concentration threshold.

<!-- @Note: It is currently not possible to use inline glue with LaEeX/Math formatting.  -->
```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---

display(Markdown(rf"""
{{numref}}`batch-elution_linear_et_auto-cycle_soo_fig_obj` shows the objective function values as a function of the feed duration, with a clear maximum at {feed_duration}.
{{numref}}`batch-elution_linear_et_auto-cycle_soo_kpi` summarizes the results.
Although the required purity is met, the yield is slightly below $100\%$ due to numerical dispersion, which causes artificial band broadening and creates small overlap regions between the component peaks.
The fractionation algorithm identifies these overlapping regions as waste, reducing the overall yield.
Band broadening also affects the determined cycle time: {cycle_time} versus the expected {cycle_time_expected}, as illustrated in the corresponding chromatogram ({{numref}}`batch-elution_linear_et_auto-cycle_soo_fig_chrom`).
These small deviations are consistent with the numerical dispersion discussed in {{numref}}`batch_elution_validation`; the recovered feed duration matches the analytical optimum, confirming that the optimizer correctly identifies the expected operating point.
"""))
```

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
:name: batch-elution_linear_et_auto-cycle_soo_fig_chrom
:scale: 100%

{glue:text}`soo_fig_chrom_caption`
```
