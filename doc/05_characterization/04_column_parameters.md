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

from git import Repo
from IPython.display import display, Markdown
import numpy as np
from myst_nb import glue
%config InlineBackend.figure_format = 'retina'

# Import the study module
diss_root = Path(Repo(search_parent_directories=True).working_dir)
sys.path.insert(0, str(diss_root / "doc" / "_ext"))
sys.path.insert(0, str(diss_root / "studies" / "parameter_estimation" / "parameter_estimation" ))

from parameter_branches import final_parameters_branch
from utils import (
    load_all_parameters, parameters_branch_e7_film_diffusion
)
parameters_all = load_all_parameters(final_parameters_branch)

from comparison_plots import load_cached_objective_results
from parameter_estimation_figures import (
    resize_comparison_figure,
    save_split_objective_figures,
)

appendix_objectives_dir = diss_root / "doc" / "99_appendix" / "figures" / "objectives"
for experiment_id in ("e5", "e6"):
    optimization_results = load_cached_objective_results(
        diss_root / "studies" / "parameter_estimation",
        parameters_all[experiment_id]["branch_name"],
    )
    save_split_objective_figures(
        optimization_results,
        appendix_objectives_dir,
        file_stem=f"{experiment_id}_objectives",
    )

e7_objectives_dir = diss_root / "doc" / "05_characterization" / "figures" / "objectives"
for branch_name, file_stem in (
    (parameters_branch_e7_film_diffusion, "e7_objectives_film_diffusion"),
    (parameters_all["e7_lrmp"]["branch_name"], "e7_objectives"),
):
    optimization_results = load_cached_objective_results(
        diss_root / "studies" / "parameter_estimation",
        branch_name,
    )
    save_split_objective_figures(
        optimization_results,
        e7_objectives_dir,
        file_stem=file_stem,
    )

d_ax_blue_dextran = parameters_all["e5"]["column"]["axial_dispersion"]["Blue Dextran"]
d_ax_blue_dextran = np.format_float_scientific(
    d_ax_blue_dextran, precision=3, unique=False, trim='k', exp_digits=1
)
glue("d_ax_blue_dextran", rf"${d_ax_blue_dextran}~\text{{m}}^{{2}}~\text{{s}}^{{-1}}$")

d_ax_acetone = parameters_all["e5"]["column"]["axial_dispersion"]["Acetone"]
d_ax_acetone = np.format_float_scientific(
    d_ax_acetone, precision=3, unique=False, trim='k', exp_digits=1
)
glue("d_ax_acetone", rf"${d_ax_acetone}~\text{{m}}^{{2}}~\text{{s}}^{{-1}}$")
```

(column_parameters)=
# Estimation of column parameters

After characterizing the periphery of the chromatography system, the column parameters were then determined.
The column geometry and particle size are provided by the manufacturer (see {numref}`column_geometry`).

```{table} Column geometry
:name: column_geometry
:align: center

| Parameter         | Value  | Unit          |
| ----------------- | ------ | ------------- |
| Column volume     | 4.7    | $\text{mL}$   |
| Column length     | 0.1    | $\text{m}$    |
| Particle diameter | 34     | $\mu\text{m}$ |
```

To estimate some of the remaining column parameters, additional experiments were performed (see {numref}`tab_experiments`):

- Experiment `E5` used Blue Dextran, a molecule too large to penetrate pores, to determine bed porosity.
- Experiment `E6` employed acetone injection to determine particle porosity.
- Experiment `E7` involved lysozyme injection under non-binding conditions (i.e. high salt concentration) to determine particle porosity and film diffusion coefficients.

```{code-cell} ipython3
:tags: [remove-cell]

from comparison_plots import (
    create_column_table,
    plot_comparison_with_column,
)
fig, *_ = plot_comparison_with_column(
    parameters_all["e5"],
    parameters_all["e6"],
    parameters_all["e7_lrmp"],
)
resize_comparison_figure(fig)
glue("fig_comparison_with_column", fig, display=False)
tab_column_parameters = create_column_table(parameters_all["e9_lrmp_4_cv"])
```

A {class}`~CADETProcess.processModel.LumpedRateModelWithPores` was used for experiment `E5`, with the film diffusion coefficient of Blue Dextran set to $0~\text{m}~\text{s}^{-1}$ to effectively model size exclusion.
While experiment `E5` is often used to determine the axial dispersion coefficient, the value obtained for Blue Dextran was unexpectedly higher than that for acetone, despite Blue Dextran being approximately 35,000 times larger.
This discrepancy may be partially attributed to partial pore penetration and nonspecific interactions {cite}`Heymann2022`.
As a result, only the bed porosity was used for further simulations, and the axial dispersion coefficient for lysozyme was re-fitted using experiment `E7`.

Experiment `E7` was conducted to investigate protein-specific transport limitations.
The data were fitted using a {class}`~CADETProcess.processModel.LumpedRateModelWithPores` ({numref}`lumped_rate_model_with_pores`).
{numref}`e7_objectives_film_diffusion` plots the objective function value against each optimization variable: while axial dispersion and particle porosity both exhibit minima, the film diffusion coefficient converged toward large values without a clear optimum, indicating that it could not be determined definitively.
The only conclusion that could be drawn was that the film diffusion coefficient must exceed $1~\times 10^{-5}~\text{m}~\text{s}^{-1}$, suggesting that film diffusion is not rate-limiting under the experimental conditions.

```{figure} figures/objectives/e7_objectives_film_diffusion.png
:name: e7_objectives_film_diffusion
:scale: 100%

Objective function values per optimization variable for experiment E7.
```

The data were therefore refitted under the assumption of non-limiting film diffusion.
Since CADET does not natively support this condition, a high numerical value of $1~\text{m}~\text{s}^{-1}$ was used as an approximation.
{numref}`e7_objectives` shows the resulting objective landscape: the minima for both axial dispersion and particle porosity are now more sharply defined.
Both fitting approaches resulted in similar particle porosities, and film diffusion was assumed to be non-limiting for all molecules in subsequent analyses.

```{figure} figures/objectives/e7_objectives.png
:name: e7_objectives
:scale: 100%

Objective function values per optimization variable for experiment E7, assuming non-limiting film diffusion.
```

Additionally, a slightly smaller particle porosity was determined, consistent with the larger size of the protein compared to acetone (used in `E6`).
Acetone, due to its small size, penetrates deeper into the pores than larger molecules like lysozyme, resulting in an apparently higher particle porosity for small molecules.
However, current models cannot account for component-specific porosities without introducing inconsistencies.
Thus, only the particle porosity fitted using the non-binding tracer (experiment `E7`) was considered for further analysis.
All estimated parameters are summarized in {numref}`tab_column_parameters`.
{numref}`fig_comparison_with_column` compares simulation results with reference experiments, showing generally good agreement between simulation and experimental data.

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
display(Markdown(tab_column_parameters))
```

```{glue:figure} fig_comparison_with_column
:name: fig_comparison_with_column
:scale: 100%

Comparison of simulation results using estimated parameters (solid lines) with reference experiments (dotted lines) for column parameter experiments.
```
