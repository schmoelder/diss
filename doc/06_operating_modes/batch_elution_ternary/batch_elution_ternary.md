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

%config InlineBackend.figure_format = 'retina'
%matplotlib inline

from pathlib import Path
import sys

from IPython.display import display, Markdown
from git import Repo
import matplotlib.pyplot as plt
from myst_nb import glue

# Import the study module
diss_root = Path(Repo(search_parent_directories=True).working_dir)
studies_root = diss_root / "studies" / "operating_modes"
sys.path.insert(0, str(studies_root))

from run_all import create_figure_and_table, setup_study
study = setup_study(studies_root, "batch_elution_ternary")

variable_units={
    r"\Delta t_{\text{cycle}}": r"\text{s}",
    r"\Delta t_{\text{feed}}": r"\text{s}",
}
```

(batch_elution_ternary_study)=
# Ternary Batch Elution Chromatography

(batch_elution_ternary_single)=
## Single-objective optimization

Here we do some single-objective optimization.

```{code-cell} ipython3
:tags: [remove-cell]

soo_chrom, ax, soo_table, soo_obj = create_figure_and_table(
    studies_root,
    "batch_elution_ternary",
    "single-objective",
    variable_units=variable_units,
)
glue("batch_elution_ternary_soo_chrom", soo_chrom, display=False)
```

{numref}`batch_elution_ternary_soo_objectives` shows objective function values.

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
display(Markdown(soo_obj))
```

{numref}`batch_elution_ternary_soo_kpi` summarizes results.

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
display(Markdown(soo_table))
```

{numref}`batch_elution_ternary_soo_chrom` shows chromatogram of best value.

```{glue:figure} batch_elution_ternary_soo_chrom
:name: batch_elution_ternary_soo_chrom
:scale: 100%

Optimal chromatogram of single-objective optimization of ternary batch elution process.
```

(batch_elution_ternary_multi)=
## Multi-objective optimization

Here we do some multi-objective optimization.

```{code-cell} ipython3
:tags: [remove-cell]

moo_chrom, ax, moo_table, moo_obj = create_figure_and_table(
    studies_root,
    "batch_elution_ternary",
    "multi-objective",
    variable_units=variable_units,
)
glue("batch_elution_ternary_moo_chrom", moo_chrom, display=False)
```

{numref}`batch_elution_ternary_moo_objectives` shows objective function values.

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
display(Markdown(moo_obj))
```

{numref}`batch_elution_ternary_moo_kpi` summarizes results.

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
display(Markdown(moo_table))
```

{numref}`batch_elution_ternary_moo_chrom` shows optimal chromatograms.

```{glue:figure} batch_elution_ternary_moo_chrom
:name: batch_elution_ternary_moo_chrom
:scale: 100%

Optimal chromatogram of multi-objective optimization of ternary batch elution process.
```
