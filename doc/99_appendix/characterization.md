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
study_root = diss_root / "studies" / "parameter_estimation"
sys.path.insert(0, str(diss_root / "doc" / "_ext"))
sys.path.insert(0, str(study_root / "parameter_estimation"))

from parameter_branches import final_parameters_branch
from utils import load_all_parameters
parameters_all = load_all_parameters(final_parameters_branch)
```

(characterization_appendix)=
# Characterization

{numref}`fig_conductivity` shows the calibration curve used to convert the measured conductivity to salt concentration, as described in {numref}`conductivity_calibration`.

```{code-cell} ipython3
:tags: [remove-cell]

from e0 import plot
from parameter_estimation_figures import resize_comparison_figure
from thesis_figure_styles import (
    CHARACTERIZATION_SINGLE_OBJECTIVE_HEIGHT_IN,
    CHARACTERIZATION_SINGLE_OBJECTIVE_WIDTH_IN,
)

fig, ax = plot()
ax.lines[0].set_markersize(4)
# e0.plot() sizes its own fonts for an 8x6in canvas; rescale to the
# thesis' font_medium/font_small (10pt/8pt) convention for a resized figure
# (see CADETProcess.plotting.figure_layouts["1_col"]) instead of shrinking a
# figure authored at fixed point sizes, which left everything oversized.
ax.set_xlabel(ax.get_xlabel(), fontsize=10)
ax.set_ylabel(r"$c_{\mathrm{salt}}~/~\mathrm{mM}$", fontsize=10)
ax.tick_params(labelsize=8)
ax.texts[0].set_fontsize(8)
ax.texts[0].set_bbox(None)
resize_comparison_figure(
    fig,
    width_in=CHARACTERIZATION_SINGLE_OBJECTIVE_WIDTH_IN,
    height_in=CHARACTERIZATION_SINGLE_OBJECTIVE_HEIGHT_IN,
)
glue("fig_conductivity", fig, display=False)
```

```{glue:figure} fig_conductivity
:name: fig_conductivity

Calibration curve for conductivity sensor.
```

Figures {numref}`e1_objectives` through {numref}`e6_objectives` show the objective function values evaluated during parameter estimation for experiments `E1`–`E6`.
Darker shades represent individuals evaluated in later generations.

```{figure} figures/objectives/e1_objectives.png
:name: e1_objectives
:width: 59%

Evaluated objective values per optimization variable in experiment `E1`.
```

```{figure} figures/objectives/e2_objectives.png
:name: e2_objectives
:width: 59%

Evaluated objective values per optimization variable in experiment `E2`.
```

```{figure} figures/objectives/e3_objectives.png
:name: e3_objectives
:width: 59%

Evaluated objective values per optimization variable in experiment `E3`.
```

```{figure} figures/objectives/e4_objectives.png
:name: e4_objectives
:width: 59%

Evaluated objective values per optimization variable in experiment `E4`.
```

```{figure} figures/objectives/e5_objectives.png
:name: e5_objectives
:width: 59%

Evaluated objective values per optimization variable in experiment `E5`.
```

```{figure} figures/objectives/e6_objectives.png
:name: e6_objectives
:width: 59%

Evaluated objective values per optimization variable in experiment `E6`.
```
