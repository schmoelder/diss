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

from utils import final_parameters_branch, load_all_parameters
parameters_all = load_all_parameters(final_parameters_branch)
```

(adsorption_parameters)=
# Estimation of adsorption parameters

Adsorption parameters are estimated using four experiments with gradient slopes of 4, 8, 12, and 16 CV, which are compared to simulation results.
The objective is to adjust the characteristic charge $\nu$ and the equilibrium constant $k_{\text{eq}}$ to minimize the discrepancy between simulations and experiments.
The steric factor $\sigma$ is not adjusted, as its effects are typically observed in breakthrough curves {cite}`Osberghaus2012`.
Rapid equilibrium is assumed throughout the simulations.

A separate simulation is run for each experiment, and the resulting outlet profiles are compared.
Agreement between experiment and simulation is quantified using the normalized root mean squared error (NRMSE).
The optimizer generates a set of Pareto-optimal solutions based on these comparisons.
The sum of all NRMSE values is used as a meta-score in a multi-criteria decision function, effectively converting the problem from single-objective to multi-objective optimization and weighting each experiment equally, independent of gradient length.
The parameter set with the best decision function score is selected as the final model parameters for the fully characterized system.
{numref}`tab_lysozyme_parameters` shows the values of the fitted parameters.

```{code-cell} ipython3
:tags: [remove-cell]

from comparison_plots import plot_lysozyme
fig, ax_lysozyme, ax_salt = plot_lysozyme(
    parameters_all["e9_lrmp_4_cv"],
    pH=5.0,
    include_pore_diffusion=False,
    is_kinetic=False,
)
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
glue("fig_lysozyme_validation", fig_validation, display=False)
print("update")
```

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
display(Markdown(tab_lysozyme))
```

{numref}`fig_lysozyme` illustrates the results, showing the simulation (colored lines) and experimental data (black dotted line) in close agreement.

```{glue:figure} fig_lysozyme
:name: fig_lysozyme
:scale: 50%

Comparison of experimental data with simulation results at pH 5 for 4, 8, 12, and 16 CV gradients.
```

To further validate the model, two additional gradient experiments using 6 and 14 column volumes (CV) were conducted, independent of the parameter estimation process.
{numref}`fig_lysozyme_validation` demonstrates that the estimated parameters yield simulations remaining in very good agreement with the experimental data.

```{glue:figure} fig_lysozyme_validation
:name: fig_lysozyme_validation
:scale: 50%

Comparison of experimental data with simulation results at pH 5 for 6, and 14 CV gradients.
```

Osberghaus et al. and Ladiwala et al. both determined isotherm parameters at pH 5 on a *Sepharose* column, albeit a fast-flow variant, whereas here a high-performance column was used {cite}`Osberghaus2012, Ladiwala2005`.
Osberghaus et al. report a characteristic charge for Lysozyme of 5.07, while Ladiwala et al. report 5.6.
The value determined in this study, {glue:text}`nu`, aligns very well with Ladiwala et al., though it is slightly higher than the value reported by Osberghaus.
For the equilibrium constant, {glue:text}`k_eq` $\text{m}_\text{l}^3~\text{m}_\text{s}^{-3}$ is again close to Ladiwala et al. (0.0763 $\text{m}_\text{l}^3~\text{m}_\text{s}^{-3}$), but lower than the value measured by Osberghaus et al. (0.118 $\text{m}_\text{l}^3~\text{m}_\text{s}^{-3}$).

Considering the complexity of the determination procedure and the fact that these studies were conducted in independent laboratories, this can be considered a sucessfull replication.
While the values are generally close, the differences can be explained by factors such as varying approaches to determining the specific capacity.
As noted, the choice of particle porosity affects the volume-specific capacity used in the model equations.
