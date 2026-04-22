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
%config InlineBackend.figure_format = 'retina'

# Import the study module
diss_root = Path(Repo(search_parent_directories=True).working_dir)
study_root = diss_root / "studies" / "parameter_estimation"
sys.path.insert(0, str(study_root / "parameter_estimation"))

from utils import (
    final_parameters_branch, load_all_parameters, parameters_branch_e7_film_diffusion
)
parameters_all = load_all_parameters(final_parameters_branch)

from comparison_plots import embed_figure_in_directive, plot_meta_score
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
:scale: 50%

Calibration curve for conductivity sensor.
```

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
e1_objectives = embed_figure_in_directive(
    study_root,
    parameters_all["e1"]["branch_name"],
    "figures/objectives.png",
    "e1_objectives",
    "Evaluated objective values per optimization variable in experiment `E1`.",
)
display(Markdown(e1_objectives))
```

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
e2_objectives = embed_figure_in_directive(
    study_root,
    parameters_all["e2"]["branch_name"],
    "figures/objectives.png",
    "e2_objectives",
    "Evaluated objective values per optimization variable in experiment `E2`.",
)
display(Markdown(e2_objectives))
```

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
e3_objectives = embed_figure_in_directive(
    study_root,
    parameters_all["e3"]["branch_name"],
    "figures/objectives.png",
    "e3_objectives",
    "Evaluated objective values per optimization variable in experiment `E3`.",
)
display(Markdown(e3_objectives))
```

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
e4_objectives = embed_figure_in_directive(
    study_root,
    parameters_all["e4"]["branch_name"],
    "figures/objectives.png",
    "e4_objectives",
    "Evaluated objective values per optimization variable in experiment `E4`.",
)
display(Markdown(e4_objectives))
```

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
e5_objectives = embed_figure_in_directive(
    study_root,
    parameters_all["e5"]["branch_name"],
    "figures/objectives.png",
    "e5_objectives",
    "Evaluated objective values per optimization variable in experiment `E5`.",
)
display(Markdown(e5_objectives))
```

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
e6_objectives = embed_figure_in_directive(
    study_root,
    parameters_all["e6"]["branch_name"],
    "figures/objectives.png",
    "e6_objectives",
    "Evaluated objective values per optimization variable in experiment `E6`.",
)
display(Markdown(e6_objectives))
```

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
e7_objectives = embed_figure_in_directive(
    study_root,
    parameters_branch_e7_film_diffusion,
    "figures/objectives.png",
    "e7_objectives_film_diffusion",
    "Evaluated objective values per optimization variable in experiment `E7`.",
)
display(Markdown(e7_objectives))
```

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
e7_objectives = embed_figure_in_directive(
    study_root,
    parameters_all["e7_lrmp"]["branch_name"],
    "figures/objectives.png",
    "e7_objectives",
    "Evaluated objective values per optimization variable in experiment `E7`, assuming non-limiting film diffusion.",
)
display(Markdown(e7_objectives))
```

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
e9_objectives = embed_figure_in_directive(
    study_root,
    parameters_all["e9_lrmp_4_cv"]["branch_name"],
    "figures/objectives.png",
    "e9_objectives",
    "Evaluated objective values per optimization variable in experiment `E9`, assuming non-limiting film diffusion and rapid equilibrium.",
)
display(Markdown(e9_objectives))
```

```{code-cell} ipython3
:tags: [remove-cell]

fig, axs = plot_meta_score(
    study_root,
    parameters_all["e9_lrmp_4_cv"]["branch_name"],
)

glue("fig_e9_meta_scores", fig, display=False)
```

```{glue:figure} fig_e9_meta_scores
:name: fig_e9_meta_scores
:scale: 100%

Sum of evaluated objective values per optimization variable in experiment `E9`, assuming non-limiting film diffusion and rapid equilibrium.
```
