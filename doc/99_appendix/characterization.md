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

```{code-cell} ipython3
:tags: [remove-cell]

from e0 import plot
fig, ax = plot()
glue("fig_conductivity", fig, display=False)
```

```{glue:figure} fig_conductivity
:name: fig_conductivity
:scale: 100%

Calibration curve for conductivity sensor.
```

```{figure} figures/objectives/e1_objectives.png
:name: e1_objectives
:scale: 100%

Evaluated objective values per optimization variable in experiment `E1`.
```

```{figure} figures/objectives/e2_objectives.png
:name: e2_objectives
:scale: 100%

Evaluated objective values per optimization variable in experiment `E2`.
```

```{figure} figures/objectives/e3_objectives.png
:name: e3_objectives
:scale: 100%

Evaluated objective values per optimization variable in experiment `E3`.
```

```{figure} figures/objectives/e4_objectives.png
:name: e4_objectives
:scale: 100%

Evaluated objective values per optimization variable in experiment `E4`.
```

```{figure} figures/objectives/e5_objectives.png
:name: e5_objectives
:scale: 100%

Evaluated objective values per optimization variable in experiment `E5`.
```

```{figure} figures/objectives/e6_objectives.png
:name: e6_objectives
:scale: 100%

Evaluated objective values per optimization variable in experiment `E6`.
```
