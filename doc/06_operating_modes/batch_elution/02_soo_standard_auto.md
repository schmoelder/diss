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
  timeout: 1200
---

% Create custom role for inserting raw latex
```{role} raw-latex(raw)
:format: latex
```

```{code-cell} ipython3
:tags: [remove-cell]

%matplotlib inline
%config InlineBackend.figure_format = 'retina'

print("update 2")

import importlib
from pathlib import Path
import sys

from IPython.display import display, Markdown
from git import Repo
import matplotlib.pyplot as plt
from myst_nb import glue

# Import the study module
diss_root = Path(Repo(search_parent_directories=True).working_dir)
study_root = diss_root / "studies" / "operating_modes"
sys.path.insert(0, str(study_root))

# Setup cases for operating mode
from operating_modes.main import setup_process
from operating_modes.post_processing import (
    get_cases_by_operating_mode,
    process_soo_results,
    process_moo_results,
    setup_overview,
)
```

```{code-cell} ipython3
:tags: [remove-cell]

operating_mode = "batch-elution"
case_module = importlib.import_module(
    f"operating_modes.{operating_mode.lower().replace('-', '_')}"
)
cases = get_cases_by_operating_mode(
    operating_mode,
    index_by_name=True,
    work_dir=study_root,
    ignore_failed=True,
)
```

(batch_elution_auto-cycle-time_soo)=
# Single-objective optimization of a binary Langmuir separation problem

In the following, a more realistic scenario is considered, accounting for transport-limiting effects and a finite binding capacity.
Additionally, the required purity is reduced to $95\%$.
The problem is summarized in {numref}`batch-elution_auto-cycle_soo_overview`.

```{code-cell} ipython3
:tags: [remove-cell]

case = cases.get(f"{operating_mode}_standard_auto-cycle-time_single-objective")
overview = setup_overview(case)

(
    (soo_fig_obj, _, soo_fig_obj_caption),
    (soo_fig_chrom, _, soo_fig_chrom_caption),
    soo_table,
) = process_soo_results(
    case,
    load_kwargs={"allow_commit_hash_mismatch": True},
)
glue("soo_fig_obj", soo_fig_obj, display=False)
glue("soo_fig_obj_caption", soo_fig_obj_caption)

glue("soo_fig_chrom", soo_fig_chrom, display=False)
glue("soo_fig_chrom_caption", soo_fig_chrom_caption)
```

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
display(Markdown(overview))
```

{numref}`batch-elution_auto-cycle_soo_fig_obj` again shows the evaluated objective function values as a function of the feed duration, with a clear maximum.

```{glue:figure} soo_fig_obj
:name: batch-elution_auto-cycle_soo_fig_obj
:scale: 100%

{glue:text}`soo_fig_obj_caption`
```

{numref}`batch-elution_auto-cycle_soo_kpi` summarizes the results.
The required purity is nearly met, with the remaining discrepancy caused by the fractionation optimizer's tolerances which could be tightened at the expense of computational speed.
Overall recovery decreases due to the larger waste fraction, as shown in {numref}`batch-elution_auto-cycle_soo_fig_chrom`.
The chromatogram reveals both the characteristic "overshoot" of a competitive nonlinear binding model and the incomplete separation of components due to dispersive effects, contributing to the larger waste fraction as compared to the idealized study.

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
display(Markdown(soo_table))
```

```{glue:figure} soo_fig_chrom
:name: batch-elution_auto-cycle_soo_fig_chrom
:scale: 100%

{glue:text}`soo_fig_chrom_caption`
```
