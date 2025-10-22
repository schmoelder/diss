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
sys.path.insert(0, str(diss_root / "studies" / "parameter_estimation" / "parameter_estimation" ))

prior_branch_name = "2025-07-13_16-08-00_main_0860834"  # After E7 (LRMP)
```

(column_parameters)=
# Estimation of column parameters

After characterizing the periphery of the chromatography system, the column parameters need to be determined.
The column length and diameter are provided by the manufacturer, as well as the particle size (see {numref}`column_geometry`).

```{table} Column geometry
:name: column_geometry
:align: center

| Parameter       | Value    | Unit    |
| --------------- | -------- | ------- |
| Column length   | $0.1$    | $m$     |
| Column diameter | $0.0077$ | $m$     |
| Particle radius | $38$     | $\mu m$ |
```

To determine the missing parameters, additional experiments were performed (see {numref}`tab_experiments`).
- Experiment `E5` used Blue Dextran, a molecule too large to penetrate pores, to determine bed porosity.
- Experiment `E6` employed acetone injection to determine both particle porosity and axial dispersion.
- Experiment `E7` involved lysozyme injection under non-binding conditions (*i.e.* high salt concentration) to determine particle porosity and film diffusion coefficients.

To determine bed porosity, a {class}`~CADETProcess.processModel.LumpedRateModelWithPores` was used with the film diffusion coefficient set to $0$, effectively modeling size exclusion.
The transport of acetone and salt molecules was assumed non-limiting, using a value of $1 \text{ m} \cdot \text{s}^{-1}$ in the models.

In addition to bed porosity, often times the Blue Dextran experiment is used to also determine the axial dispersion coefficient.
While this parameter is generally component-specific, it is not always possible to determine the value for each component.
This is reasonable assumption since it also accounts for muleddy diffusion
However, the value obtained by fitting the for Blue Dextran (~1e-7) was higher than for acetone (1e-8).
This is counterintuitive since Blue Dextran is approximately 35,000 times larger.
This might be partially explained by partial pore penetration of Blue Dextran and its tendency to "stick" [@TODO: citation needed].
Different approaches were used to fit the tailing of the Blue Dextran peak.
Accounting for this tailing shifted the estimated parameters (axial dispersion and column porosity).
To minimize the influence of peak tailing on parameter estimation, only the front of the peak was used for the inverse fit.

Consequently, axial dispersion was re-fitted in experiment `E6`, and the acetone value was also assumed for lysozyme.

Due to its small size, acetone can penetrate deeper into pores than larger molecules like lysozyme.
This results in an apparently larger particle porosity for small molecules.
However, current models cannot account for component-specific porosities as this may lead to inconsistencies.
Therefore, only the particle porosity fitted using the non-binding tracer (experiment `E7`) was considered.

To investigate whether pore diffusion is limiting, both a {class}`~CADETProcess.processModel.GeneralRateModel` and a {class}`~CADETProcess.processModel.LumpedRateModelWithPores` were fitted to experiment `E7` data.
Both models determined similar particle porosities.
However, definitive values for either film diffusion or pore diffusion coefficients could not be obtained [@TODO: refer to figure in Appendix].
The LRMP was selected for the remainder of this work as it contains only one transport-limiting parameter (see {numref}`lumped_rate_model_with_pores`).
This simplification provides a more robust modeling approach while maintaining adequate predictive capability.

Good agreement between simulation and experimental reference data was generally observed.
The estimated parameters are presented in {numref}`tab_column`.

```{code-cell} ipython3
:tags: [remove-cell]

from utils import load_all_parameters
from comparison_plots import plot_comparison_with_column, create_column_table

parameters = load_all_parameters(prior_branch_name)
fig, *_ = plot_comparison_with_column(
    parameters["e5"],
    parameters["e6"],
    parameters["e7_lrmp"],
)
glue("fig_comparison_with_column", fig, display=False)
table = create_column_table(parameters)
```

```{glue:figure} fig_comparison_with_column
:name: fig_comparison_with_column
:figwidth: 300px

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
