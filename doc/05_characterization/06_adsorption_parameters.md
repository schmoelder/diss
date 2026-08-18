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

import matplotlib
from IPython.display import display, Markdown
from git import Repo
from myst_nb import glue
%config InlineBackend.figure_format = 'retina'

# Import the study module
diss_root = Path(Repo(search_parent_directories=True).working_dir)
study_root = diss_root / "studies" / "parameter_estimation"
sys.path.insert(0, str(diss_root / "doc" / "_ext"))
sys.path.insert(0, str(study_root / "parameter_estimation"))

from parameter_branches import final_parameters_branch
from utils import load_all_parameters
parameters_all = load_all_parameters(final_parameters_branch)

from comparison_plots import load_cached_objective_results
from parameter_estimation_figures import (
    OBJECTIVE_COLUMN_WIDTH_IN,
    resize_comparison_figure,
    resize_objective_comparison_figure,
    save_split_objective_figures,
)

optimization_results = load_cached_objective_results(
    study_root,
    parameters_all["e9_lrmp_4_cv"]["branch_name"],
)
save_split_objective_figures(
    optimization_results,
    diss_root / "doc" / "05_characterization" / "figures" / "objectives",
    file_stem="e9_objectives",
    # Shrunk from the shared OBJECTIVE_ROW_HEIGHT_IN (1.5in) just for this
    # figure so it fits on one page together with fig_e9_meta_scores; see
    # doc/05_characterization/06_adsorption_parameters.md figure block below.
    row_height_in=1.4,
)
```

(adsorption_parameters)=
# Estimation of adsorption parameters

Adsorption parameters were estimated using experiment `E9` (see {numref}`tab_experiments`), which comprises four gradient elution runs with slopes of 4, 8, 12, and 16 CV, compared to simulation results.
The objective was to adjust the characteristic charge $\nu$ and the equilibrium constant $K_{\text{eq}}$ to minimize the discrepancy between simulations and experiments.
The steric factor $\sigma$ was not adjusted, as its effects can typically only be observed in breakthrough curves under overloaded conditions {cite}`Osberghaus2012`.
Consequently, it was set to 0.
Rapid equilibrium was assumed throughout the simulations.

A separate simulation was run for each experiment, and the resulting outlet profiles were compared.
Agreement between experiment and simulation was quantified using the NRMSE.
Rather than aggregating all NRMSE values into a single objective, each gradient experiment's NRMSE is handled as a separate objective.
The optimizer generates a set of Pareto-optimal solutions based on these comparisons.
The sum of all NRMSE values serves as a meta score in a multi-criteria decision function to select the final parameter set, weighting each experiment equally regardless of gradient length.
{numref}`tab_lysozyme_parameters` shows the values of the fitted parameters and {numref}`fig_lysozyme` illustrates the results, showing the simulation (colored lines) and experimental data (black dotted line) in close agreement.

```{code-cell} ipython3
:tags: [remove-cell]

from comparison_plots import plot_meta_score, plot_lysozyme
fig, ax_lysozyme, ax_salt = plot_lysozyme(
    parameters_all["e9_lrmp_4_cv"],
    pH=5.0,
    include_pore_diffusion=False,
    is_kinetic=False,
)
resize_comparison_figure(fig, width_in=2 * OBJECTIVE_COLUMN_WIDTH_IN)
glue("fig_lysozyme", fig, display=False)

from comparison_plots import create_lysozyme_table
tab_lysozyme = create_lysozyme_table(parameters_all["e9_lrmp_4_cv"])

binding_model_parameters = parameters_all["e9_lrmp_4_cv"]["column"]["binding_model"]

glue("k_eq", round(binding_model_parameters["adsorption_rate"]["Lysozyme"], 2))
glue("nu", round(binding_model_parameters["characteristic_charge"]["Lysozyme"], 2))

fig_validation, ax_lysozyme, ax_salt = plot_lysozyme(
    parameters_all["e9_lrmp_4_cv"],
    pH=5.0,
    include_pore_diffusion=False,
    is_kinetic=False,
    use_validation=True,
)
resize_comparison_figure(fig_validation, width_in=2 * OBJECTIVE_COLUMN_WIDTH_IN)
glue("fig_lysozyme_validation", fig_validation, display=False)
```

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
display(Markdown(tab_lysozyme))
```

```{glue:figure} fig_lysozyme
:name: fig_lysozyme

Comparison of experimental data with simulation results at pH 5 for 4, 8, 12, and 16 CV gradients.
```

To further validate the model, two additional gradient experiments using 6 and 14 CV were conducted, independent of the parameter estimation process.
{numref}`fig_lysozyme_validation` demonstrates that the estimated parameters yield simulations remaining in very good agreement with the experimental data.

```{glue:figure} fig_lysozyme_validation
:name: fig_lysozyme_validation

Comparison of experimental data with simulation results at pH 5 for 6 and 14 CV gradients.
```

In addition to experimental validation, the estimated parameters were compared with values reported in the literature.
Osberghaus et al. and Ladiwala et al. both determined isotherm parameters at pH 5 on a *Sepharose* column, albeit a fast-flow variant, whereas here a high-performance column was used {cite}`Osberghaus2012, Ladiwala2005`.
Osberghaus et al. report a characteristic charge for Lysozyme of 5.07, while Ladiwala et al. report 5.6.
The value determined in this study, {glue:text}`nu`, aligns very well with Ladiwala et al., though it is slightly higher than the value reported by Osberghaus et al.
For the equilibrium constant, {glue:text}`k_eq` $\text{m}_\text{l}^3~\text{m}_\text{s}^{-3}$ is again close to Ladiwala et al. (0.0763 $\text{m}_\text{l}^3~\text{m}_\text{s}^{-3}$), but lower than the value measured by Osberghaus et al. (0.118 $\text{m}_\text{l}^3~\text{m}_\text{s}^{-3}$).
Given the complexity of the determination procedure and the fact that these studies were conducted in independent laboratories, this represents very good agreement.
While the values are generally close, the differences can be explained by factors such as varying approaches to determining the specific capacity.

The summed NRMSE yields a well-defined combined optimum at {glue:text}`nu`, providing a clear and unambiguous parameter estimate (see {numref}`fig_e9_meta_scores`).
Beyond this, the multi-objective formulation provides an additional diagnostic capability: when each gradient experiment's NRMSE is treated as a separate objective, the individual optima for $\nu$ consistently fall between 5.9 and 6.3, and those for $k_\text{eq}$ between 0.05 and 0.06 $\text{m}_\text{l}^3~\text{m}_\text{s}^{-3}$ (see {numref}`e9_objectives`), a discrepancy that scalar aggregation obscures entirely.
Notably, the combined optimum for $k_\text{eq}$ lies above the range of all individual optima, meaning the aggregated objective converges to a value that no single experiment would independently suggest.
If the model were perfectly consistent across all gradient slopes, the individual and combined optima would coincide and the Pareto front would collapse to a single point.
The spread observed instead indicates that the model cannot simultaneously satisfy all experiments equally well, pointing to gradient-dependent effects not captured by the current model structure.

```{code-cell} ipython3
:tags: [remove-cell]

fig, axs = plot_meta_score(
    study_root,
    parameters_all["e9_lrmp_4_cv"]["branch_name"],
)
axs[1].set_ylabel('')
axs[1].tick_params(labelleft=False)
for ax in axs:
    # The submodule plots this on a log y-axis, which for this data's sub-decade
    # range yields sparse, oddly-formatted ticks (e.g. "2 x 10^-1"). Switch to
    # linear to match the plain decimal ticks used in fig_e9_objectives (5.11).
    ax.set_yscale("linear")
    ax.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(nbins=5, min_n_ticks=4))
    ax.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(nbins=4, min_n_ticks=3))
resize_objective_comparison_figure(fig, ncols=2, nrows=1)
fig.subplots_adjust(wspace=0.6)
glue("fig_e9_meta_scores", fig, display=False)
```

```{glue:figure} fig_e9_meta_scores
:name: fig_e9_meta_scores

Sum of evaluated objective values per optimization variable in experiment `E9`, assuming non-limiting film diffusion and rapid equilibrium.
Darker shades represent individuals evaluated in later generations.
```

```{figure} figures/objectives/e9_objectives.png
:name: e9_objectives

Evaluated objective values per optimization variable in experiment `E9`, assuming non-limiting film diffusion and rapid equilibrium.
Darker shades represent individuals evaluated in later generations.
```
