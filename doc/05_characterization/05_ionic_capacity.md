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

prior_branch_name = "2025-07-15_10-41-03_main_9699531" @TODO: Check final results
```

(ionic_capacity)=
# Estimation of the ionic capacity of the resin

To determine the ionic capacity of the resin, a titration experiment is conducted.
In this experiment, the column is first flushed with water, followed by equilibration with $20~CV$ of acetic acid at $pH 3$.
During equilibration, the acetic acid exchanges counter-ions with $n_{\text{H}^+}$ protons.
Next, the column is flushed with water for 10 CV to remove loosely bound acetic acid.
Finally, the resin is titrated with a NaOH solution.
The NaOH concentration is determined via pH measurement, and the NaOH volume is calculated from the increase in conductivity over time.
The amount of exchanged sodium ions, $n_{\text{Na}^+}$, is then determined using the NaOH volume and concentration:

$$
n_{\text{Na}^+} = V_{\text{NaOH}} \cdot c_{\text{NaOH}}
$$

The total ionic capacity is calculated by dividing the exchanged sodium ions by the solid volume of the resin:

$$
\Lambda = \frac{n_{\text{Na}^+}}{V_c \cdot (1 - \varepsilon_{\text{total}})}
$$

The total porosity, $\varepsilon_{\text{total}}$, is determined using the column porosity $\varepsilon_c$and the particle porosity $\varepsilon_p$, which are estimated from tracer experiments used for model calibration.
It is given as the sum of the interstitial volume $V_{\text{int}}$ and pore volume $V_{\text{pore}}$, divided by the column volume $V_C$:

$$
\varepsilon_{\text{total}} = \frac{V_{\text{int}} + V_{\text{pore}}}{V_C} = \varepsilon_c + (1 - \varepsilon_c) \cdot \varepsilon_p
$$

@TODO: Add plot

```{code-cell} ipython3
:tags: [remove-cell]

from utils import load_parameters
from comparison_plots import plot_resin_titration

parameters = load_parameters(prior_branch_name)
fig, *_ = plot_resin_titration(plot_single=True)
glue("fig_resin_titration", fig, display=False)
```

```{glue:figure} fig_resin_titration
:name: fig_resin_titration
:figwidth: 300px

Comparison of simulation results with corresponding reference experiments. @TODO: Add color description.
```

@TODO: Discuss "reduced" capacity for large protein.
