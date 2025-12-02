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

| Parameter       | Value  | Unit |
| --------------- | ------ | ---- |
| Column volume   | 4.7    | mL   |
| Column length   | 0.1    | m    |
| Particle radius | 17     | µm   |
```

To determine the missing parameters, additional experiments were performed (see {numref}`tab_experiments`).

- Experiment `E5` used Blue Dextran, a molecule too large to penetrate pores, to determine bed porosity.
- Experiment `E6` employed acetone injection to determine both particle porosity and axial dispersion.
- Experiment `E7` involved lysozyme injection under non-binding conditions (*i.e.* high salt concentration) to determine particle porosity and film diffusion coefficients.

To determine bed porosity, a {class}`~CADETProcess.processModel.LumpedRateModelWithPores` was used with the film diffusion coefficient set to $0~\text{m}~\text{s}^{-1}$, effectively modeling size exclusion.
The transport of acetone and salt molecules was assumed non-limiting, using a value of $1~\text{m}~\text{s}^{-1}$ in the models.

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
md_text = f"""In addition to bed porosity, often times the Blue Dextran experiment is used to also determine the axial dispersion coefficient.
However, the value obtained by fitting the for Blue Dextran ({d_ax_blue_dextran}) was higher than for acetone ({d_ax_acetone}).
This is counterintuitive since Blue Dextran is approximately 35,000 times larger.
This might be partially explained by partial pore penetration of Blue Dextran and a tendency for unspecific interactions {{cite}}`Heymann2022`.
Consequently, only the bed porosity was used for further simulations and axial dispersion for Lysozyme was re-fitted in experiment `E7`."""

display(Markdown(md_text))
```

aha

Due to its small size, acetone can penetrate deeper into pores than larger molecules like lysozyme.
This results in an apparently larger particle porosity for small molecules.
However, current models cannot account for component-specific porosities as this may lead to inconsistencies.
Therefore, only the particle porosity fitted using the non-binding tracer (experiment `E7`) was considered.

To investigate whether pore diffusion is limiting, both a {class}`~CADETProcess.processModel.GeneralRateModel` and a {class}`~CADETProcess.processModel.LumpedRateModelWithPores` were fitted to experiment `E7` data.
Both models determined similar particle porosities.
However, definitive values for either film diffusion or pore diffusion coefficients could not be obtained (see {numref}`e7_objectives_film_diffusion`).
The LRMP was selected for the remainder of this work as it contains only one transport-limiting parameter (see {numref}`lumped_rate_model_with_pores`).
This simplification provides a more robust modeling approach while maintaining adequate predictive capability.

Good agreement between simulation and experimental reference data was generally observed.
The estimated parameters are presented in {numref}`tab_column_parameters`.

```{code-cell} ipython3
:tags: [remove-cell]

from comparison_plots import plot_comparison_with_column, create_column_table
fig, *_ = plot_comparison_with_column(
    parameters_all["e5"],
    parameters_all["e6"],
    parameters_all["e7_lrmp"],
)
glue("fig_comparison_with_column", fig, display=False)
table = create_column_table(parameters_all["e9_lrmp_4_cv"])
```

```{glue:figure} fig_comparison_with_column
:name: fig_comparison_with_column
:scale: 50%

Comparison of simulation results with corresponding reference experiments. Blue: `E5`, red: `E6`, orange: `E7`.
```

{numref}`fig_comparison_with_column` shows three different simulation results with their corresponding experimental measurements are depicted.

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
display(Markdown(table))
```
