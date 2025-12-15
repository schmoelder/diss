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

from utils import final_parameters_branch, load_all_parameters
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
- Experiment `E7` involved lysozyme injection under non-binding conditions (*i.e.* high salt concentration) to determine particle porosity and film diffusion coefficients.

```{code-cell} ipython3
:tags: [remove-cell]

from comparison_plots import plot_comparison_with_column, create_column_table
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

Acetone, due to its small size, can penetrate deeper into pores than larger molecules like lysozyme, resulting in an apparently larger particle porosity for small molecules.
However, current models cannot account for component-specific porosities without introducing inconsistencies.
Thus, only the particle porosity fitted using the non-binding tracer (experiment `E7`) was considered for subsequent analysis.

Experiment `E7` was also used to investigate protein-specific transport limitations.
A {class}`~CADETProcess.processModel.LumpedRateModelWithPores` ({numref}`lumped_rate_model_with_pores`) was fitted to the data, but a definitive value for the film diffusion coefficient could not be determined ({numref}`e7_objectives_film_diffusion`).
To address this, the data was refitted assuming non-limiting film diffusion.
Since **CADET** does not natively support non-limiting film diffusion, a high numerical value of $1~\text{m}~\text{s}^{-1}$ was used to effectively model this condition.
Both fitting approaches yielded similar particle porosities.
To simplify the model and reduce parameter uncertainty, film diffusion was subsequently assumed to be non-limiting for all molecules.

The estimated parameters are summarized in {numref}`tab_column_parameters`.
Good agreement between simulation and experimental data was generally observed.
{numref}`fig_comparison_with_column` compares simulation results with reference experiments.

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

Comparison of simulation results (solid lines) with corresponding reference experiments (dashed)
```
