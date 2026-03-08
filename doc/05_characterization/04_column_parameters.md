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
sys.path.insert(0, str(diss_root / "studies" / "parameter_estimation" / "parameter_estimation" ))

from utils import (
    final_parameters_branch, load_all_parameters, parameters_branch_e7_film_diffusion
)
parameters_all = load_all_parameters(final_parameters_branch)

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

After characterizing the periphery of the chromatography system, the column parameters need to be determined.
The column length and diameter are provided by the manufacturer, as well as the particle size (see {numref}`column_geometry`).

```{table} Column geometry
:name: column_geometry
:align: center

| Parameter         | Value  | Unit           |
| ----------------- | ------ | -------------- |
| Column volume     | 4.7    | $\text{mL}$     |
| Column length     | 0.1    | $\text{m}$     |
| Particle diameter | 34     | $\text{µm}$ |
```

To determine the missing parameters, additional experiments were performed (see {numref}`tab_experiments`):

- Experiment `E5` used Blue Dextran, a molecule too large to penetrate pores, to determine bed porosity.
- Experiment `E6` employed acetone injection to determine particle porosity.
- Experiment `E7` involved lysozyme injection under non-binding conditions (i.e. high salt concentration) to determine particle porosity and film diffusion coefficients.

```{code-cell} ipython3
:tags: [remove-cell]

from comparison_plots import (
    create_column_table,
    embed_figure_in_directive,
    plot_comparison_with_column,
)
fig, *_ = plot_comparison_with_column(
    parameters_all["e5"],
    parameters_all["e6"],
    parameters_all["e7_lrmp"],
)
glue("fig_comparison_with_column", fig, display=False)
tab_column_parameters = create_column_table(parameters_all["e9_lrmp_4_cv"])
```

A {class}`~CADETProcess.processModel.LumpedRateModelWithPores` was used for experiment `E5`, with the film diffusion coefficient of Blue Dextran set to $0~\text{m}~\text{s}^{-1}$ to model size exclusion.
While experiment `E5` is often used to determine the axial dispersion coefficient, the value obtained for Blue Dextran was unexpectedly higher than that for acetone, despite Blue Dextran being approximately 35,000 times larger.
This discrepancy may be partially attributed to partial pore penetration and nonspecific interactions {cite}`Heymann2022`.
As a result, only the bed porosity was used for further simulations, and the axial dispersion coefficient for lysozyme was re-fitted using experiment `E7`.

Experiment `E7` was conducted to investigate protein-specific transport limitations.
The data were fitted using a {class}`~CADETProcess.processModel.LumpedRateModelWithPores` ({numref}`lumped_rate_model_with_pores`).
While axial dispersion exhibits a minimum, though not sharply defined, the film diffusion coefficient could not be determined definitively (see {numref}`e7_objectives_film_diffusion`).
The analysis only indicates that the film diffusion coefficient must exceed $1~\times 10^{-5}~\text{m}~\text{s}^{-1}$.

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
study_root = diss_root / "studies" / "parameter_estimation"
sys.path.insert(0, str(study_root / "parameter_estimation"))

e7_objectives = embed_figure_in_directive(
    study_root,
    parameters_branch_e7_film_diffusion,
    "figures/objectives.png",
    "e7_objectives_film_diffusion",
    "Evaluated objective values per optimization variable in experiment E7.",
)
display(Markdown(e7_objectives))
```

To address this, the data were refitted under the assumption of non-limiting film diffusion.
Since **CADET** does not natively support this condition, a high numerical value of $1~\text{m}~\text{s}^{-1}$ was used to approximate non-limiting film diffusion.
Both fitting approaches resulted in similar particle porosities, and the objectives plot ({numref}`e7_objectives`) now shows a clear minimum for axial dispersion.
To simplify the model and reduce parameter uncertainty, film diffusion was assumed to be non-limiting for all molecules in subsequent analyses.

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
e7_objectives = embed_figure_in_directive(
    study_root,
    parameters_all["e7_lrmp"]["branch_name"],
    "figures/objectives.png",
    "e7_objectives",
    "Evaluated objective values per optimization variable in experiment E7, assuming limiting film diffusion.",
)
display(Markdown(e7_objectives))
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
