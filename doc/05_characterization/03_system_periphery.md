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
%config InlineBackend.figure_format = 'retina'

# Import the study module
diss_root = Path(Repo(search_parent_directories=True).working_dir)
study_root = diss_root / "studies" / "parameter_estimation"
sys.path.insert(0, str(diss_root / "doc" / "_ext"))
sys.path.insert(0, str(study_root / "parameter_estimation" ))

from parameter_branches import final_parameters_branch
from utils import load_all_parameters
parameters_all = load_all_parameters(final_parameters_branch)

from comparison_plots import load_cached_objective_results
from parameter_estimation_figures import (
    resize_comparison_figure,
    save_split_objective_figures,
)

appendix_objectives_dir = diss_root / "doc" / "99_appendix" / "figures" / "objectives"
for experiment_id in ("e1", "e2", "e3", "e4"):
    optimization_results = load_cached_objective_results(
        study_root,
        parameters_all[experiment_id]["branch_name"],
    )
    save_split_objective_figures(
        optimization_results,
        appendix_objectives_dir,
        file_stem=f"{experiment_id}_objectives",
    )
```

(system_periphery)=
# Characterization of system periphery

The objective of this chapter is to characterize the periphery of the chromatography system by dividing it into individual parts and investigating each part using tracer experiments.
For this purpose, individual sections of the system can be bypassed by physically reconfiguring the tubing connections, as detailed in {numref}`tab_experiments`.

The experimental protocol consists of:

- Experiments `E1` and `E2`: Acetone injections to determine void volumes of pre- and post-column tubing
- Experiment `E3`: Salt pulse to measure void volume between conductivity and UV sensors
- Experiment `E4`: Salt step to characterize mixer behavior and pre-column tubing effects

```{code-cell} ipython3
:tags: [remove-cell]

from comparison_plots import plot_comparison_without_column
fig, *_ = plot_comparison_without_column(parameters_all["e4"])
resize_comparison_figure(fig)
glue("fig_comparison_without_column", fig, display=False)

from comparison_plots import create_system_table
tab_system_periphery = create_system_table(parameters_all["e4"])
```

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
display(Markdown(tab_system_periphery))
```

{numref}`tab_system_periphery` presents the fitted parameter values.
The determined tubing length and volume are in the same order of magnitude as those in the Knauer system.
However, the axial dispersion coefficients exceed those reported by Kumar et al. ($\approx 10^{-6}~\text{m}^2~\text{s}^{-1}$, on an ÄKTA AVANT 25) {cite}`Kumar2022`, indicating potential additional mixing effects in the Knauer system.
Despite this, the simulation results are in good agreement with the reference experiments ({numref}`fig_comparison_without_column`).
Given the small tubing volume, the overall impact of dispersion on the final chromatograms is likely minimal.
The model accurately captures the time offset, which is the primary goal of the periphery characterization.

```{glue:figure} fig_comparison_without_column
:name: fig_comparison_without_column
:scale: 100%

Comparison of simulation results using estimated parameters (solid lines) with reference experiments E1--4 (dotted lines) for system periphery experiments.
```
