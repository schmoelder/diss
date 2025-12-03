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

# Import the study module
diss_root = Path(Repo(search_parent_directories=True).working_dir)
sys.path.insert(0, str(diss_root / "studies" / "parameter_estimation" / "parameter_estimation" ))

from utils import final_parameters_branch, load_all_parameters
parameters_all = load_all_parameters(final_parameters_branch)
```

(ionic_capacity)=
# Estimation of the ionic capacity of the resin

To determine the ionic capacity of the resin, a titration experiment is conducted as follows:
The column is first flushed with water, then equilibrated with $20~\text{CV}$ of acetic acid at pH 3, during which acetic acid exchanges counter-ions with $n_{\ce{H}^+}$ protons.
After equilibration, the column is flushed with $10~\text{CV}$ of water to remove unbound acetic acid.
Finally, the resin is titrated with a $\ce{NaOH}$ solution.

The amount of $\ce{NaOH}$ consumed is determined by analyzing the breakthrough curve via conductivity measurement ({numref}`fig_resin_titration`).
The breakthrough time point, $t_{\text{bt 10}}$, is defined as the time at which $10\%$ of the breakthrough occurs.
Using the flow rate $Q$, the volume and concentration of $\ce{NaOH}$, the amount of exchanged sodium ions, $n_{\ce{Na}^+}$, is calculated as:

$$
n_{\ce{Na}^+} = V_{\ce{NaOH}} \cdot c_{\ce{NaOH}} = Q \cdot t_{\text{bt, 10}} \cdot c_{\ce{NaOH}}
$$

It is assumed that the number of sodium ions is equal to the total capacity of the column.
The volume specific ionic capacity $\Lambda$ is then calculated by dividing the exchanged sodium ions by the solid volume of the resin:

$$
\Lambda = \frac{n_{\ce{Na}^+}}{V_{\text{c}} \cdot (1 - \varepsilon_{\text{total}})}
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
print("update")

bed_porosity = parameters_all["e8"]["column"]["bed_porosity"]
particle_porosity = parameters_all["e8"]["column"]["particle_porosity"]
total_porosity = bed_porosity + (1 - bed_porosity) * particle_porosity
glue("total_porosity", round(total_porosity, 2))

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
lambda_ = calculate_specific_capacity(4.7e-6, total_porosity, total_capacity_mol)
glue("lambda", round(lambda_, 2))
```

```{glue:figure} fig_resin_titration
:name: fig_resin_titration
:scale: 100%

Breakthrough curve of $\ce{NaOH} for resin capacity titration. Dashed line indicating time point of $10\%$ breakthrough used for determination volume.
```

The volume of $\ce{NaOH}$ used was determined to be {glue:text}`V_NaOH_used` mL.
To accurately determine the capacity, the void volume of the system including both the periphery and the column void volume must be accounted for.
For this correction, the particle porosity determined using acetone was used, as lysozyme cannot penetrate all pores.
The total system dead volume was {glue:text}`system_dead_volume` mL.
This results in a total capacity of {glue:text}`total_capacity_mmol` mmol.
When normalized by the total column volume, the capacity is {glue:text}`manufacturer_capacity` $\text{mmol}~\text{mL}_{\text{packed bed}}^{-1}$, which is consistent with the manufacturer's specification.
For further calculations, the capacity is normalized by the solid phase volume, yielding a specific capacity of {glue:text}`lambda` $\text{mol}~\text{m}_{\text{s}}^{-3}$.
