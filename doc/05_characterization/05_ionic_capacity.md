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
from myst_nb import glue
%config InlineBackend.figure_format = 'retina'

# Import the study module
diss_root = Path(Repo(search_parent_directories=True).working_dir)
sys.path.insert(0, str(diss_root / "studies" / "parameter_estimation" / "parameter_estimation" ))

from utils import final_parameters_branch, load_all_parameters
parameters_all = load_all_parameters(final_parameters_branch)
```

(ionic_capacity)=
# Estimation of the ionic capacity of the resin

To determine the ionic capacity of the resin, a titration experiment is conducted as follows: the column is first flushed with water, then equilibrated with $20~\text{CV}$ of acetic acid at pH 3.
During this step, the protons ($\ce{H+}$) from the acetic acid exchange with the resin’s bound counter-ions, displacing them into the effluent.
After equilibration, the column is flushed with $10~\text{CV}$ of water to remove any unbound acetic acid and displaced ions.
Finally, the resin is titrated with a $\ce{NaOH}$ solution to quantify the number of bound protons, thereby determining the resin’s ionic capacity.

The amount of $\ce{NaOH}$ consumed is determined by analyzing the breakthrough curve via conductivity measurement ({numref}`fig_resin_titration`).
The breakthrough time point, $t_{\text{bt, 10}}$, is defined as the time at which $10\%$ of the breakthrough occurs.
Using the flow rate $Q$, the volume and concentration of $\ce{NaOH}$, the amount of exchanged sodium ions, $n_{\ce{Na}^+}$, is calculated as:

$$
n_{\ce{Na}^+} = V_{\ce{NaOH}} \cdot c_{\ce{NaOH}} = Q \cdot t_{\text{bt, 10}} \cdot c_{\ce{NaOH}}
$$

It is assumed that the number of sodium ions equals the total capacity of the column.
The volume-specific ionic capacity, $\Lambda$, is then calculated by dividing the exchanged sodium ions by the solid volume of the resin:

$$
\Lambda = \frac{n_{\ce{Na}^+}}{V_{\text{C}} \cdot (1 - \varepsilon_{\text{total}})}
$$

The total porosity, $\varepsilon_{\text{total}}$, is determined using the column porosity $\varepsilon_c$ and the particle porosity $\varepsilon_p$, which are estimated from the previous tracer experiments.
It is given as the sum of the interstitial volume $V_{\text{int}}$ and pore volume $V_{\text{pore}}$, divided by the column volume $V_C$:

$$
\varepsilon_{\text{total}} = \frac{V_{\text{int}} + V_{\text{pore}}}{V_C} = \varepsilon_c + (1 - \varepsilon_c) \cdot \varepsilon_p
$$

```{code-cell} ipython3
:tags: [remove-cell]

from comparison_plots import plot_resin_titration
fig, *_ = plot_resin_titration(plot_single=True)
glue("fig_resin_titration", fig, display=False)

# @TODO: use proper values when rerunning
# glue("system_dead_volume", round(parameters_all["e8"]["system_dead_volume"]*1e6, 2))
# glue("V_NaOH_used", round(parameters_all["e8"]["V_NaOH_used"]*1e6, 2))
# glue("V_NaOH", round(parameters_all["e8"]["V_NaOH"]*1e6, 2))
glue("system_dead_volume", round(5.322519797764502e-06*1e6, 2))
glue("V_NaOH_used", round(4.738833333333333e-05*1e6, 2))
glue("V_NaOH", round(4.2065813535568824e-05*1e6, 2))

total_capacity_mol = parameters_all["e8"]["total_capacity"]
glue("total_capacity_mmol", round(total_capacity_mol*1000, 2))

manufacturer_capacity = total_capacity_mol / 4.7e-6
glue("manufacturer_capacity", round(manufacturer_capacity/1000, 2))

from e8 import calculate_specific_capacity

bed_porosity = parameters_all["e5"]["column"]["bed_porosity"]

# Acetone
particle_porosity_acetone = parameters_all["e6"]["column"]["particle_porosity"]
total_porosity_acetone = bed_porosity + (1 - bed_porosity) * particle_porosity_acetone
lambda_acetone = calculate_specific_capacity(4.7e-6, total_porosity_acetone, total_capacity_mol)
glue("lambda_acetone", round(lambda_acetone, 2))

# Lysozyme
particle_porosity_lysozyme = parameters_all["e7_lrmp"]["column"]["particle_porosity"]
total_porosity_lysozyme = bed_porosity + (1 - bed_porosity) * particle_porosity_lysozyme
lambda_lysozyme = calculate_specific_capacity(4.7e-6, total_porosity_lysozyme, total_capacity_mol)
glue("lambda_lysozyme", round(lambda_lysozyme, 2))
```

```{glue:figure} fig_resin_titration
:name: fig_resin_titration
:scale: 100%

Breakthrough curve of $\ce{NaOH}$ for resin capacity titration. Dashed line indicating time point of $10\%$ breakthrough used for determination of volume.
```

The volume of $\ce{NaOH}$ used was determined to be {glue:text}`V_NaOH_used` mL.
To accurately determine the capacity, the void volume of the system including both the periphery and the column void volume must be accounted for.
For this correction, the particle porosity determined using acetone was used, as lysozyme cannot penetrate all pores.
The total system dead volume was {glue:text}`system_dead_volume` mL.
This results in a total capacity of {glue:text}`total_capacity_mmol` mmol.
When normalized by the total column volume, the capacity is {glue:text}`manufacturer_capacity` $\text{mmol}~\text{mL}_{\text{packed bed}}^{-1}$, which is consistent with the manufacturer's specification.

Given that lysozyme is large and may not penetrate all pores, and considering that ligands may not be uniformly distributed throughout the pore depth, the exact accessible capacity cannot be precisely determined.
To avoid assumptions about pore accessibility, the total capacity is assumed constant.
For further calculations, the capacity is normalized by the corresponding apparent solid phase volume.
This results in a specific capacity of {glue:text}`lambda_lysozyme` mol m$_{\text{s}}^{-3}$ when considering lysozyme.
For reference, normalization using acetone's apparent porosity would yield a specific capacity of {glue:text}`lambda_acetone` mol m$_{\text{s}}^{-3}$.
